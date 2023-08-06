import logging
import os
import sys
import shutil
import coloredlogs
import traceback

from PySide2 import QtCore, QtWidgets
from famegui.mainwindow import MainWindow
from famegui.usersettings import UserSettings
from famegui.appworkingdir import AppWorkingDir
from famegui import __version__


def _tr(text):
    return QtCore.QCoreApplication.translate("app", text)


_APP_NAME = "FAME Gui"
_APP_VERSION = __version__


def _setup_logs():
    format = "%(asctime)s %(levelname)s %(message)s"
    coloredlogs.install(level='INFO', fmt=format)


def _init_working_dir_location() -> AppWorkingDir:
    logging.debug("initializing working dir")

    s = UserSettings()
    if s.working_dir is None:
        QtWidgets.QMessageBox.information(
            None,
            _tr("{} working directory").format(_APP_NAME),
            _tr("The {} working directory is not defined for this user account.\n\n"
                "This directory will be used as the root location for all the files required or referenced by the application.\n\n"
                "Click OK to configure the path to the FAME working directory.").format(_APP_NAME)
        )
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            _tr("Select {} working directory").format(_APP_NAME),
            "",
            QtWidgets.QFileDialog.ShowDirsOnly)
        if len(dir_path) == 0:
            raise RuntimeError(
                "can't start the application without a valid working directory")
        s.set_working_dir(dir_path)

    logging.info("working directory: {}".format(s.working_dir))
    return AppWorkingDir(s.working_dir)


def _init_schemas_dir(work_dir: AppWorkingDir):
    logging.debug("initializing schemas dir")

    schemas_dir = work_dir.schemas_dir
    if os.path.isdir(work_dir.schemas_dir):
        if len(work_dir.list_existing_schema_names()) > 0:
            return
    else:
        logging.info("creating directory {}".format(schemas_dir))
        os.mkdir(schemas_dir)

    # copy the default schema
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_schema_path = os.path.join(
        script_dir, "data", "schema-AMIRIS-2020-10-23.yaml")
    logging.info("copying default schema file '{}' to {}".format(
        default_schema_path, schemas_dir))
    try:
        shutil.copy(default_schema_path, schemas_dir)
    except Exception as e:
        raise RuntimeError(
            "failed to copy default schema file to {}".format(schemas_dir)) from e


def _init_scenarios_dir(work_dir: AppWorkingDir):
    logging.debug("initializing scenarios dir")

    scenarios_dir = work_dir.scenarios_dir
    if not os.path.isdir(scenarios_dir):
        logging.info("creating directory {}".format(scenarios_dir))
        os.mkdir(scenarios_dir)


def _init_working_dir() -> AppWorkingDir:
    work_dir = _init_working_dir_location()
    _init_schemas_dir(work_dir)
    _init_scenarios_dir(work_dir)
    return work_dir


_main_wnd = None


def _excepthook(exc_type, exc_value, exc_tb):
    if isinstance(exc_value, ValueError):
        logging.error("{}".format(exc_value))
    else:
        logging.error("Exception: {}\n".format(
            exc_value).join(traceback.format_tb(exc_tb)))

    msg = _tr("Error: {}.").format(exc_value)
    if exc_value.__cause__:
        msg += _tr("\n\nDetails: {}").format(exc_value.__cause__)
    QtWidgets.QMessageBox.critical(_main_wnd, _tr("Error"), msg)


def run():
    _setup_logs()
    sys.excepthook = _excepthook

    app = QtWidgets.QApplication([])

    app.setOrganizationDomain("dlr.de")
    app.setOrganizationName("DLR")
    app.setApplicationName(_APP_NAME)
    app.setApplicationVersion(_APP_VERSION)
    app.setApplicationDisplayName("{} (version {})".format(
        app.applicationName(), app.applicationVersion()))

    work_dir = _init_working_dir()

    logging.debug("creating main window")
    _main_wnd = MainWindow(work_dir)
    _main_wnd.resize(1200, 1000)
    _main_wnd.show()

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        logging.debug(
            "processing command line argument '{}'".format(file_path))
        _main_wnd.load_scenario_file(file_path)

    logging.debug("running the application")
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
    logging.info("exiting the application")
