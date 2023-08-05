import csv
import io
import logging
import os
from typing import List

from remo_app.remo.api.constants import TaskType, AnnotationSetType
from remo_app.remo.models import AnnotationSet, Task, Class, DatasetImage
from remo_app.remo.models.annotation import NewAnnotation
from remo_app.remo.use_cases.annotation.open_images import OpenImagesBase
from remo_app.remo.utils import utils
from remo_app.remo.utils.progress_info import ProgressInfo
from .annotation import AnnotationImageClassification
from .base import DatasetImageMapping
from .utils import get_base_image_name

logger = logging.getLogger('remo_app')


class PlainCsvImageClassification(OpenImagesBase):
    task = TaskType.image_classification

    # required fields
    file_name = 'file_name'
    class_name = 'class_name'

    file_name_variations = {
        'image',
        'image_id',
        'image id',
        'file_name',
        'filename',
        'file',
        'file name',
        'file_path',
        'path',
        'file path',
    }

    class_name_variations = {
        'class',
        'label',
        'name',
        'class_name',
        'class name',
        'label_name',
        'label name',
        'category',
        'classes',
    }

    variations = {
        file_name: file_name_variations,
        class_name: class_name_variations,
    }

    @classmethod
    def is_applicable(cls, path, fp):
        if utils.is_system_file(path):
            return False

        _, ext = os.path.splitext(path)
        if ext not in ('.csv', '.txt'):
            return False

        pos = fp.tell()
        fp.seek(0)
        csv_reader = csv.reader(fp, delimiter=',')
        header = None
        while not header:
            header = next(csv_reader)
        fp.seek(pos)

        header = cls.read_header(header)
        n = len(cls.variations)
        return len(header) == n and len(set(header.values())) == n

    @classmethod
    def match_field_name(cls, name):
        for field_name, field_variations in cls.variations.items():
            if name.lower() in field_variations:
                return field_name

    @classmethod
    def read_header(cls, cols):
        ids = {}
        for idx, col in enumerate(cols):
            field = cls.match_field_name(col)
            if field:
                ids[field] = idx
        return ids

    def parse_filename(self, header: dict, row: List[str]) -> str:
        try:
            return get_base_image_name(row[header[self.file_name]])
        except ValueError:
            return ''

    def parse_class_name(self, header: dict, row: List[str]) -> List[str]:
        try:
            category_ids = row[header[self.class_name]]
            category_ids = category_ids.split(';')
        except ValueError:
            category_ids = ['N/A']

        return [self.get_category(category_id, default=category_id) for category_id in category_ids]

    def retrieve_annotations(self, images_mapping: dict = None, dataset_id=None):
        pos = self.data_fp.tell()
        self.data_fp.seek(0)
        csv_reader = csv.reader(self.data_fp, delimiter=',')
        rows_number = sum(1 for line in csv_reader) - 1
        self.data_fp.seek(0)

        # logger.info(f'Retrieving annotations: {self.__class__.__name__}')

        progress = ProgressInfo(rows_number, items='annotation objs')

        header = None
        while not header:
            header = next(csv_reader)
        header = self.read_header(header)

        annotation = None
        rows_skipped = 0
        for row in csv_reader:
            progress.report(rows_skipped=rows_skipped)
            image_name = self.parse_filename(header, row)
            if not image_name:
                rows_skipped += 1
                logger.error(f'Failed parse image name from row {row}')
                continue

            db_image_id, image_name = self.get_image_id(image_name, images_mapping)
            if db_image_id is None:
                rows_skipped += 1
                self.add_error(f'Cannot find image in db {image_name}')
                continue

            if not annotation:
                annotation = AnnotationImageClassification(image_name, image_name=image_name)
            elif annotation.source_image_id != image_name:
                yield annotation
                annotation = AnnotationImageClassification(image_name, image_name=image_name)

            label_names = self.parse_class_name(header, row)
            class_names, err = self.decode_class(label_names)
            self.add_error(err)

            if not class_names:
                rows_skipped += 1
                logger.error(f'Failed parse class name from row {row}')
                continue

            for class_name in class_names:
                annotation.add_class(class_name, 1)

        self.data_fp.seek(pos)

        if annotation:
            yield annotation

    def fetch_images_mapping(self, dataset_id):
        return DatasetImageMapping(dataset_id)

    def save_annotations(
        self, dataset_id, user_id, images_mapping: dict, annotation_set_id=None, skip_new_classes=False
    ) -> int:
        """
        Save annotations to database
        :param dataset_id: Dataset id
        :param user_id: User id for creating annotation sets
        :param images_mapping: mapping {internal_image_id: DatasetImage_database_id}
        :return: count of saved annotations
        """
        classes_mapping = dict(Class.objects.values_list('name', 'id'))
        annotation_set = self.get_or_create_annotation_set(
            dataset_id, user_id, annotation_set_id=annotation_set_id
        )

        # logger.info(f'Started annotation upload on Dataset {dataset_id} for task: {self.task}')
        return sum(
            self.save_single_annotation(
                annotation, images_mapping, classes_mapping, annotation_set.id, skip_new_classes
            )
            for annotation in self.retrieve_annotations(images_mapping, dataset_id)
        )

    def get_or_create_annotation_set(self, dataset_id, user_id, annotation_set_id=None):
        if annotation_set_id:
            return AnnotationSet.objects.get(id=annotation_set_id)

        task = Task.objects.get(type=self.task.name)
        annotation_set = AnnotationSet.objects.filter(dataset_id=dataset_id, task=task).first()
        if not annotation_set:
            annotation_set = AnnotationSet.objects.create(
                name=f'{self.task.value}',
                type=AnnotationSetType.image.value,
                task=task,
                user_id=user_id,
                dataset_id=dataset_id,
            )

        return annotation_set

    def save_single_annotation(
        self, annotation, images_mapping, classes_mapping, annotation_set_id, skip_new_classes=False
    ):
        db_image_id, image_name = self.get_image_id(annotation.source_image_id, images_mapping)
        if db_image_id is None:
            self.add_error(f'Cannot find image in db {annotation.image_name}')
            return 0

        annotation.write_to_db(db_image_id, annotation_set_id, classes_mapping, skip_new_classes)
        return 1

    def export_annotations(
        self,
        annotation_set,
        export_coordinates='pixel',
        full_path=False,
        export_classes=False,
        export_without_annotations=False,
        filter_by_tags=None
    ):
        """
        Exports annotations in CSV format
        """

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['file_name', 'classes'])

        annotated = set()

        for annotation in NewAnnotation.objects.filter(annotation_set=annotation_set):
            if not annotation.has_annotation():
                continue
            annotated.add(annotation.image.id)
            if filter_by_tags and not filter_by_tags.intersection(annotation.tags):
                continue

            encoded = self.encode_classes(annotation.classes)
            writer.writerow([self.get_file_name(annotation.image, full_path), "; ".join(encoded)])

        if export_without_annotations:
            for img in DatasetImage.objects.filter(dataset=annotation_set.dataset).all():
                if img.id not in annotated:
                    writer.writerow([self.get_file_name(img, full_path), ''])

        return output.getvalue()

    def get_file_name(self, img: DatasetImage, full_path=False):
        file_name = img.original_name
        if full_path and img.image_object.local_image:
            file_name = img.image_object.local_image
        return file_name
