import logging
import yaml


def must_load_file(file_path: str):
    """ Helper function to load the content of a YAML file """
    logging.debug("loading yaml file {}".format(file_path))
    try:
        with open(file_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(
            "failed to load yaml file '{}'".format(file_path)) from e


def save_to_file(dict, file_path: str):
    """ Helper function to save some content to a YAML file """
    logging.debug("saving yaml to file {}".format(file_path))
    try:
        with open(file_path, "w") as f:
            return yaml.dump(dict, f)
    except Exception as e:
        raise RuntimeError(
            "failed to write data to yaml file '{}'".format(file_path)) from e


def must_get_str_key(dict, key: str):
    """ Helper function to extract a YAML string key with a user friendly error message on failure """
    v = dict.get(key)
    if v is None:
        raise ValueError("key '{}' is missing".format(key))
    return v


def get_str_key_or(dict, key: str, default_value: str):
    """ Helper function to extract a YAML string key if it exists, or return the given default value otherwise """
    v = dict.get(key)
    return default_value if v is None else v


def must_get_int_key(dict, key: str):
    """ Helper function to extract a YAML int key with a user friendly error message on failure """
    v = must_get_str_key(dict, key)
    if not type(v) is int:
        raise ValueError(
            "invalid value '{}' for key '{}': must be an integer".format(v, key))
    return v
