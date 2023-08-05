def can_user_modify_dataset(user, dataset):
    return not dataset.is_public
    # TODO: share dataset
    # return not dataset.is_public and dataset.user == user or user.is_superuser


def can_user_modify_annotation_set(user, annotation_set):
    # TODO: share dataset
    # is_owner = not annotation_set.dataset.is_public and annotation_set.dataset.user == user
    is_owner = True
    is_admin = user.is_superuser

    return is_owner or is_admin
