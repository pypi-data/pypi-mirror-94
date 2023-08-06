# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_newcontract.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogNewContract(object):
    def setupUi(self, NewContractDialog):
        if not NewContractDialog.objectName():
            NewContractDialog.setObjectName(u"NewContractDialog")
        NewContractDialog.resize(417, 176)
        self.verticalLayout = QVBoxLayout(NewContractDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelDescr = QLabel(NewContractDialog)
        self.labelDescr.setObjectName(u"labelDescr")
        self.labelDescr.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelDescr)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(NewContractDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditProductName = QLineEdit(NewContractDialog)
        self.lineEditProductName.setObjectName(u"lineEditProductName")
        self.lineEditProductName.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout.addWidget(self.lineEditProductName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(NewContractDialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.spinBoxFirstDelivery = QSpinBox(NewContractDialog)
        self.spinBoxFirstDelivery.setObjectName(u"spinBoxFirstDelivery")
        self.spinBoxFirstDelivery.setMaximumSize(QSize(100, 16777215))
        self.spinBoxFirstDelivery.setMinimum(-1000)
        self.spinBoxFirstDelivery.setMaximum(1000)

        self.horizontalLayout_2.addWidget(self.spinBoxFirstDelivery)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(NewContractDialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.spinBoxDeliveryInterval = QSpinBox(NewContractDialog)
        self.spinBoxDeliveryInterval.setObjectName(u"spinBoxDeliveryInterval")
        self.spinBoxDeliveryInterval.setMaximumSize(QSize(100, 16777215))
        self.spinBoxDeliveryInterval.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBoxDeliveryInterval.setMaximum(36000)

        self.horizontalLayout_3.addWidget(self.spinBoxDeliveryInterval)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.buttonBox = QDialogButtonBox(NewContractDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewContractDialog)
        self.buttonBox.accepted.connect(NewContractDialog.accept)
        self.buttonBox.rejected.connect(NewContractDialog.reject)

        QMetaObject.connectSlotsByName(NewContractDialog)
    # setupUi

    def retranslateUi(self, NewContractDialog):
        NewContractDialog.setWindowTitle(QCoreApplication.translate("DialogNewContract", u"Dialog", None))
        self.labelDescr.setText(QCoreApplication.translate("DialogNewContract", u"<html><head/><body><p>Details of the <span style=\" font-weight:600;\">new contract</span> between agent #XXX and agent #YYY:</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("DialogNewContract", u"Product name:", None))
        self.label_3.setText(QCoreApplication.translate("DialogNewContract", u"First delivery time:", None))
        self.spinBoxFirstDelivery.setSuffix(QCoreApplication.translate("DialogNewContract", u" sec", None))
        self.label_4.setText(QCoreApplication.translate("DialogNewContract", u"Delivery interval in steps:", None))
    # retranslateUi

