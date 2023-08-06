import logging
from PySide2 import QtCore, QtWidgets

from famegui.ui_dialog_newagent import Ui_DialogNewAgent
from famegui import models


class AttributeTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, field: models.SchemaAgentTypeField):
        self._field = field
        QtWidgets.QTreeWidgetItem.__init__(
            self, parent, [self._field.name, ""])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

        if self._field.type.is_mandatory:
            font = self.font(0)
            font.setBold(True)
            self.setFont(0, font)

    def setData(self, column, role, value):
        """ Override QTreeWidgetItem.setData() """
        if (role == QtCore.Qt.EditRole):
            if self._field.type.is_compatible_value(value):
                logging.info("ok: {}".format(value))
            else:
                logging.info("bad: {}".format(value))

        QtWidgets.QTreeWidgetItem.setData(self, column, role, value)


class DialogNewAgent(QtWidgets.QDialog):

    def __init__(self, schema: models.Schema, parent=None):
        QtWidgets.QDialog.__init__(self, parent=None)
        self._ui = Ui_DialogNewAgent()
        self._ui.setupUi(self)
        self._schema = schema
        # init
        self.setWindowTitle(self.tr("New agent"))
        self._ui.comboBoxType.addItems(self._schema.agent_types.keys())
        # tree view
        self._ui.treeFields.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self._ui.treeFields.setRootIsDecorated(False)
        self._ui.treeFields.setColumnCount(2)
        self._ui.treeFields.setHeaderLabels(["Field", "Value"])
        self._ui.treeFields.setColumnWidth(0, 200)
        self._ui.treeFields.setAlternatingRowColors(True)
        self._fill_input_fields_table()
        # connect slots
        self._ui.comboBoxType.currentTextChanged.connect(
            self._fill_input_fields_table)

    def _fill_input_fields_table(self):
        self._ui.treeFields.clear()

        current_agent_type = self._ui.comboBoxType.currentText()
        for f in self._schema.agent_types[current_agent_type].fields.values():
            item = AttributeTreeItem(self._ui.treeFields, f)

    def make_new_agent(self, agent_id) -> models.Agent:
        agent_type = self._ui.comboBoxType.currentText()
        return models.Agent(agent_id, agent_type)
