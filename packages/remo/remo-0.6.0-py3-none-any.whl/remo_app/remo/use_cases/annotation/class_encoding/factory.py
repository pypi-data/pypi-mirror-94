from .class_encoding import ClassEncodingType, GoogleKnowledgeGraphClassEncoding, WordNetClassEncoding, AbstractClassEncoding, types, CustomClassEncoding

class_encoding_factory = {
    ClassEncodingType.google_knowledge_graph: GoogleKnowledgeGraphClassEncoding(),
    ClassEncodingType.word_net: WordNetClassEncoding(),
}


def get_class_encoding_from_dict(data: dict) -> AbstractClassEncoding:
    if not data:
        return None

    type = data.get('type')
    if not type:
        return None

    if type in types:
        return class_encoding_factory.get(type)

    if type == ClassEncodingType.custom:
        classes = data.get('classes')
        if not classes or not isinstance(classes, dict):
            return None

        return CustomClassEncoding(classes)
