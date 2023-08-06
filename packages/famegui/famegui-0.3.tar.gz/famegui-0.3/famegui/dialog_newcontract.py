from PySide2.QtWidgets import QDialog, QDialogButtonBox

from famegui.ui_dialog_newcontract import Ui_DialogNewContract

from famegui import models


class DialogNewContract(QDialog):

    def __init__(self, sender_id: int, receiver_id: int, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_DialogNewContract()
        self._ui.setupUi(self)
        self._sender_id = sender_id
        self._receiver_id = receiver_id

        self.setWindowTitle(self.tr("New contract"))
        self._ui.labelDescr.setText(self.tr(
            '<html><head/><body><p>Details of the <span style=" font-weight:600;">new contract</span> between <b>agent #{}</b> and <b>agent #{}</b>:</p></body></html>').format(sender_id, receiver_id))
        self._ui.lineEditProductName.textChanged.connect(
            self._update_ok_button_status)
        self._update_ok_button_status()

    def make_new_contract(self) -> models.Contract:
        return models.Contract(
            self._sender_id,
            self._receiver_id,
            self._ui.lineEditProductName.text()
        )

    def _update_ok_button_status(self):
        all_fields_ok = self._ui.lineEditProductName.text() != ""
        self._ui.buttonBox.button(
            QDialogButtonBox.Ok).setEnabled(all_fields_ok)
