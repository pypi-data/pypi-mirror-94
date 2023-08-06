# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_newagent.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogNewAgent(object):
    def setupUi(self, NewAgentDialog):
        if not NewAgentDialog.objectName():
            NewAgentDialog.setObjectName(u"NewAgentDialog")
        NewAgentDialog.resize(374, 396)
        NewAgentDialog.setMinimumSize(QSize(300, 350))
        self.verticalLayout = QVBoxLayout(NewAgentDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(NewAgentDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxType = QComboBox(NewAgentDialog)
        self.comboBoxType.setObjectName(u"comboBoxType")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxType.sizePolicy().hasHeightForWidth())
        self.comboBoxType.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.comboBoxType)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeFields = QTreeWidget(NewAgentDialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeFields.setHeaderItem(__qtreewidgetitem)
        self.treeFields.setObjectName(u"treeFields")
        self.treeFields.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.treeFields)

        self.buttonBox = QDialogButtonBox(NewAgentDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewAgentDialog)
        self.buttonBox.accepted.connect(NewAgentDialog.accept)
        self.buttonBox.rejected.connect(NewAgentDialog.reject)

        QMetaObject.connectSlotsByName(NewAgentDialog)
    # setupUi

    def retranslateUi(self, NewAgentDialog):
        NewAgentDialog.setWindowTitle(QCoreApplication.translate("DialogNewAgent", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("DialogNewAgent", u"New agent type :", None))
    # retranslateUi

