import os
import logging
import typing

from PySide2 import QtCore


class UserSettings:
    """ Class to load and save user settings on the local host """

    def __init__(self):
        self._settings = QtCore.QSettings("FAME", "famegui")

    _KEY_WORKING_DIR = "working_directory"

    @property
    def working_dir(self):
        dir_path = self._settings.value(self._KEY_WORKING_DIR)
        if dir_path is None:
            logging.warn("path to working dir is not defined")
        elif not os.path.isdir(dir_path):
            logging.warning(
                "deleting invalid path to working dir: {}".format(dir_path))
            self._settings.remove(self._KEY_WORKING_DIR)
            dir_path = None
        return dir_path

    def set_working_dir(self, path: str):
        path = os.path.abspath(path)
        logging.info("configuring new working dir: {}".format(path))
        if not os.path.isdir(path):
            raise ValueError(
                "Can't use '{}' as new working directory: invalid path.".format(path))
        return self._settings.setValue(self._KEY_WORKING_DIR, path)
