import typing

from PySide2 import QtWidgets
from famegui.ui_dialog_scenario_properties import Ui_DialogScenarioProperties


class DialogScenarioProperties(QtWidgets.QDialog):

    def __init__(self, schema_names: typing.List[str], parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_DialogScenarioProperties()
        self._ui.setupUi(self)
        # init
        self.setWindowTitle(self.tr("Scenario properties"))
        self._ui.comboBoxSchemas.addItems(schema_names)

    def selected_schema_name(self) -> str:
        return self._ui.comboBoxSchemas.currentText()
