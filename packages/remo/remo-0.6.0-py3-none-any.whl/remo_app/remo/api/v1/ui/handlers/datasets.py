import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response

from remo_app.remo.models import Dataset, DatasetStatistics, DatasetImage, DatasetSettings

MAXIMUM_THUMBNAILS_COUNT = 4

logger = logging.getLogger('remo_app')


class DatasetSettingsKeys:
    keep_classes_order_constant = 'keep_classes_order_constant'


class DatasetSerializer(serializers.ModelSerializer):
    image_thumbnails = SerializerMethodField()
    owner = SerializerMethodField()
    is_readonly = SerializerMethodField()
    quantity = SerializerMethodField()

    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'owner', 'is_archived', 'image_thumbnails', 'quantity', 'size_in_bytes',
            'created_at', 'updated_at', 'license', 'is_public', 'is_readonly'
        )

    def get_quantity(self, obj):
        return DatasetImage.objects.filter(dataset=obj).count()

    def get_image_thumbnails(self, obj):
        queryset = obj.dataset_images.all()
        return [img.image_object.preview.url for img in queryset[:MAXIMUM_THUMBNAILS_COUNT]]

    def get_owner(self, obj):
        result = ''
        if obj.user:
            result = obj.user.get_full_name().strip()
        return result if result else 'Unknown'

    def get_is_readonly(self, instance):
        return False
        # TODO: share dataset
        # user = self.context['request'].user
        # if user == instance.user:
        #     return False
        # # TODO: check later in instance.users_shared
        # return True


class DatasetDetailsSerializer(DatasetSerializer):
    top3_classes = SerializerMethodField()
    total_classes = SerializerMethodField()
    settings = SerializerMethodField()

    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'owner', 'is_archived', 'image_thumbnails', 'quantity', 'size_in_bytes',
            'created_at', 'updated_at', 'license', 'is_public', 'users_shared', 'top3_classes',
            'total_classes', 'is_readonly', 'settings'
        )

    def get_top3_classes(self, instance):
        stats = DatasetStatistics.objects.filter(dataset=instance).first()
        if not stats or not stats.statistics:
            return []
        return stats.statistics.get('top3_classes', [])

    def get_total_classes(self, instance):
        stats = DatasetStatistics.objects.filter(dataset=instance).first()
        if not stats or not stats.statistics:
            return 0
        return stats.statistics.get('total_classes', 0)

    def get_settings(self, instance):
        ds = DatasetSettings.objects.filter(dataset=instance).first()
        if ds:
            return ds.settings

        return {
            DatasetSettingsKeys.keep_classes_order_constant: False
        }


class Datasets(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    filter_backends = (DjangoFilterBackend,)
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()
    filter_fields = ('is_archived', 'is_public')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
        # TODO: share dataset
        # return qs.filter(Q(user=self.request.user) | Q(is_public=True))

    @action(['get'], detail=True, url_path='details')
    def details(self, request, pk=None):
        dataset = self.get_queryset().get(id=pk)
        return Response(DatasetDetailsSerializer(dataset, context={'request': request}).data)

    @action(['get'], detail=True, url_path='config')
    def config(self, request, pk=None):
        ds = DatasetSettings.objects.filter(dataset_id=pk).first()
        if ds:
            return Response(ds.settings)

        default = {
            DatasetSettingsKeys.keep_classes_order_constant: False
        }
        return Response(default)

    @action(['post'], detail=True, url_path='update-config')
    def update_config(self, request, pk=None):
        keep_classes_order_constant = request.data.get(DatasetSettingsKeys.keep_classes_order_constant, None)
        ds, _ = DatasetSettings.objects.get_or_create(dataset_id=pk)
        if ds.settings is None:
            ds.settings = {}

        if isinstance(keep_classes_order_constant, bool):
            ds.settings[DatasetSettingsKeys.keep_classes_order_constant] = keep_classes_order_constant
            ds.save()
        return Response(ds.settings)
