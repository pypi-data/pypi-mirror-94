"""Utility functions."""

from dtool_lookup_server import (
    mongo,
    MONGO_COLLECTION,
)

from dtool_lookup_server.utils import (
    get_user_obj,
    preprocess_query_base_uris,
)

VALID_MONGO_QUERY_KEYS = (
    "base_uris",
)

try:
    # Python 2.
    ALLOWED_TYPES = (str, int, float, bool, unicode)
except NameError:
    # Python 3.
    ALLOWED_TYPES = (str, int, float, bool)


def filter_dict_to_mongo_query(filters):
    """Return mongo query from filters dict."""
    base_uri_subquery = None
    if len(filters["base_uris"]) == 1:
        base_uri_subquery = str(filters["base_uris"][0])
    else:
        base_uris = [str(b) for b in filters["base_uris"]]
        base_uri_subquery = {"$in": base_uris}

    return {"base_uri": base_uri_subquery}


def _extract_valid_keys(ds_info):
    ds_valid_keys = set()

    # Some old datasets may not have any annotations.
    if "annotations" not in ds_info:
        return ds_valid_keys

    for key, value in ds_info["annotations"].items():
        if type(value) not in ALLOWED_TYPES:
            continue
        ds_valid_keys.add(key)
    return ds_valid_keys


def _extract_keys_of_interest(filters):
    keys_of_interest = set()
    if "annotation_keys" in filters:
        keys_of_interest.update(filters["annotation_keys"])
    if "annotations" in filters:
        keys_of_interest.update(filters["annotations"].keys())
    return keys_of_interest


def _exclude_dataset_info_filter(ds_info, filters):
    "There is probably a more clever way to do this using the mongo query language."  # NOQA

    # Create set of valid keys in dataset.
    ds_valid_keys = _extract_valid_keys(ds_info)

    # Dataset without a valid key are ignored.
    if len(ds_valid_keys) == 0:
        return True

    # All keys of interest must be present on the dataset for it to be
    # recognised.
    keys_of_interest = _extract_keys_of_interest(filters)
    ds_valid_keys = _extract_valid_keys(ds_info)
    if len(keys_of_interest.difference(ds_valid_keys)) > 0:
        return True

    # If the "annotations" filter is on check that the key/value pair is
    # present, if not skip the dataset.
    skip = False
    if "annotations" in filters:
        for ann_key, ann_value in filters["annotations"].items():
            if ann_key not in ds_valid_keys:
                skip = True
                break
            if ds_info["annotations"][ann_key] != ann_value:
                skip = True
                break

    return skip


def get_annotation_key_info_by_user(username, filters):
    """Return dictionary with annotation keys and numbers of datasets
    given that key and any filters passed into the function.

    :param username: username
    :param filters: dictionary with filters
    :returns: dictionary where keys are annotation keys and values
              are the numbers of datasets with that key given the
              filter provided
    """
    # Validate the user; raises AuthenticationError if invalid.
    get_user_obj(username)

    filters = preprocess_query_base_uris(username, filters)
    mongo_query = filter_dict_to_mongo_query(filters)

    # If there are no base URI the user has not got permissions to view any
    # datasets.
    if len(filters["base_uris"]) == 0:
        return {}

    cx = mongo.db[MONGO_COLLECTION].find(
        mongo_query,
        {
            "annotations": True,
        }
    )

    # There is probably a more clever way to do this using the
    # mongo query language.
    annotation_key_info = {}
    for ds in cx:
        if _exclude_dataset_info_filter(ds, filters):
            continue

        # Add the key information.
        for key in _extract_valid_keys(ds):
            annotation_key_info[key] = annotation_key_info.get(key, 0) + 1

    return annotation_key_info


def get_annotation_value_info_by_user(username, filters):
    """Return dictionary with annotation keys and dictionaries of values and
    numbers of datasets for those values given that any filters passed into the
    function.

    :param username: username
    :param filters: dictionary with filters
    :returns: dictionary where keys are annotation keys and values
              are dictionaries with the values and the the numbers of datasets
              for those values given the filters provided
    """
    filters = preprocess_query_base_uris(username, filters)
    mongo_query = filter_dict_to_mongo_query(filters)

    # If there are no base URI the user has not got permissions to view any
    # datasets.
    if len(filters["base_uris"]) == 0:
        return {}

    cx = mongo.db[MONGO_COLLECTION].find(
        mongo_query,
        {
            "annotations": True,
        }
    )

    # There is probably a more clever way to do this using the
    # mongo query language.
    annotation_value_info = {}
    for ds in cx:
        if _exclude_dataset_info_filter(ds, filters):
            continue

        for key in _extract_keys_of_interest(filters):
            value = ds["annotations"][key]
            value_dict = annotation_value_info.get(key, {})
            value_dict[value] = value_dict.get(value, 0) + 1
            annotation_value_info[key] = value_dict

    return annotation_value_info


def get_num_datasets_by_user(username, filters):
    """Return number of datasets given the filters passed into the function.

    :param username: username
    :param filters: dictionary with filters
    :returns: number of datasets
    """
    filters = preprocess_query_base_uris(username, filters)
    mongo_query = filter_dict_to_mongo_query(filters)

    # If there are no base URI the user has not got permissions to view any
    # datasets.
    if len(filters["base_uris"]) == 0:
        return 0

    cx = mongo.db[MONGO_COLLECTION].find(
        mongo_query,
        {
            "annotations": True,
        }
    )

    # There is probably a more clever way to do this using the
    # mongo query language.
    num_datasets = 0
    for ds in cx:
        if _exclude_dataset_info_filter(ds, filters):
            continue
        num_datasets += 1

        # All keys_of_interest must be present on the dataset for it to be
        # recognised.
        keys_of_interest = _extract_keys_of_interest(filters)
        ds_valid_keys = _extract_valid_keys(ds)
        if len(keys_of_interest.difference(ds_valid_keys)) > 0:
            continue

    return num_datasets


def get_datasets_by_user(username, filters):
    """Return datasets given the filters passed into the function.

    :param username: username
    :param filters: dictionary with filters
    :returns: list of dictionaries with information about the datasets
    """
    filters = preprocess_query_base_uris(username, filters)
    mongo_query = filter_dict_to_mongo_query(filters)

    # If there are no base URI the user has not got permissions to view any
    # datasets.
    if len(filters["base_uris"]) == 0:
        return []

    cx = mongo.db[MONGO_COLLECTION].find(
        mongo_query,
        {
            "_id": False,
            "readme": False,
            "manifest": False,
        }
    )

    # There is probably a more clever way to do this using the
    # mongo query language.
    datasets = []
    for ds in cx:
        if _exclude_dataset_info_filter(ds, filters):
            continue
        datasets.append(ds)

    return datasets
