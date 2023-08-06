# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_scenario_properties.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogScenarioProperties(object):
    def setupUi(self, DialogScenarioProperties):
        if not DialogScenarioProperties.objectName():
            DialogScenarioProperties.setObjectName(u"DialogScenarioProperties")
        DialogScenarioProperties.resize(393, 102)
        self.verticalLayout = QVBoxLayout(DialogScenarioProperties)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(DialogScenarioProperties)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxSchemas = QComboBox(DialogScenarioProperties)
        self.comboBoxSchemas.setObjectName(u"comboBoxSchemas")
        self.comboBoxSchemas.setMinimumSize(QSize(260, 0))

        self.horizontalLayout.addWidget(self.comboBoxSchemas)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(DialogScenarioProperties)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DialogScenarioProperties)
        self.buttonBox.accepted.connect(DialogScenarioProperties.accept)
        self.buttonBox.rejected.connect(DialogScenarioProperties.reject)

        QMetaObject.connectSlotsByName(DialogScenarioProperties)
    # setupUi

    def retranslateUi(self, DialogScenarioProperties):
        self.label.setText(QCoreApplication.translate("DialogScenarioProperties", u"Schema name :", None))
        pass
    # retranslateUi

