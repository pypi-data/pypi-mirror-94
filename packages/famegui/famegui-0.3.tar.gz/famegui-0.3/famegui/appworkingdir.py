import os
import logging
import typing


class AppWorkingDir:
    """ Class used to find and access the files from the FAME GUI working directory """

    _SCHEMAS_DIR_NAME = "schemas"
    _SCENARIOS_DIR_NAME = "scenarios"

    def __init__(self, root_dir: str):
        self._root_dir = os.path.abspath(root_dir)

    @property
    def root_dir(self) -> str:
        return self._root_dir

    @property
    def schemas_dir(self):
        return os.path.join(self._root_dir, self._SCHEMAS_DIR_NAME)

    @property
    def scenarios_dir(self):
        return os.path.join(self._root_dir, self._SCENARIOS_DIR_NAME)

    def ensure_child_path(self, path: str) -> str:
        abs_path = os.path.join(self._root_dir, path)
        if not abs_path.startswith(self._root_dir):
            raise ValueError(
                "invalid working directory path '{}'".format(abs_path))
        return abs_path

    def find_existing_child_file(self, path: str) -> str:
        abs_path = self.ensure_child_path(path)
        return abs_path if os.path.isfile(abs_path) else None

    def find_schema_file_path_from_name(self, schema_name: str):
        abs_path = self.find_existing_child_file(schema_name)
        if abs_path is None:
            logging.warning("invalid schema name '{}': could not find a matching schema file in '{}'".format(
                schema_name, self.schemas_dir))
            return None
        return abs_path

    def list_existing_schema_names(self) -> typing.List[str]:
        logging.debug("listing yaml files in {}".format(self.schemas_dir))
        result = []
        for filename in os.listdir(self.schemas_dir):
            if filename.endswith(".yaml"):
                # always return a relative path in UNIX style
                result.append(
                    "./{}/{}".format(self._SCHEMAS_DIR_NAME, filename))
            else:
                logging.warn("ignoring file '{}' in {}".format(
                    filename, self.schemas_dir))
        return result
