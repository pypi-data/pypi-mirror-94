# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import qt_resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1230, 822)
        MainWindow.setTabShape(QTabWidget.Triangular)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(QMainWindow.AllowNestedDocks|QMainWindow.AnimatedDocks|QMainWindow.VerticalTabs)
        self.actionNewProject = QAction(MainWindow)
        self.actionNewProject.setObjectName(u"actionNewProject")
        icon = QIcon()
        icon.addFile(u":/icons/new.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNewProject.setIcon(icon)
        self.actionOpenProject = QAction(MainWindow)
        self.actionOpenProject.setObjectName(u"actionOpenProject")
        icon1 = QIcon()
        icon1.addFile(u":/icons/open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenProject.setIcon(icon1)
        self.actionSaveProject = QAction(MainWindow)
        self.actionSaveProject.setObjectName(u"actionSaveProject")
        icon2 = QIcon()
        icon2.addFile(u":/icons/floppy-disk.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSaveProject.setIcon(icon2)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionHome = QAction(MainWindow)
        self.actionHome.setObjectName(u"actionHome")
        icon3 = QIcon()
        icon3.addFile(u":/icons/home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionHome.setIcon(icon3)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        icon4 = QIcon()
        icon4.addFile(u":/icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon4)
        self.actionCloseProject = QAction(MainWindow)
        self.actionCloseProject.setObjectName(u"actionCloseProject")
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName(u"actionRun")
        icon5 = QIcon()
        icon5.addFile(u":/icons/play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRun.setIcon(icon5)
        self.actionSaveProjectAs = QAction(MainWindow)
        self.actionSaveProjectAs.setObjectName(u"actionSaveProjectAs")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 60))
        self.frame_2.setMaximumSize(QSize(16777215, 80))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.labelUserName = QLabel(self.frame_2)
        self.labelUserName.setObjectName(u"labelUserName")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelUserName.setFont(font)
        self.labelUserName.setTextFormat(Qt.PlainText)

        self.horizontalLayout_4.addWidget(self.labelUserName)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.labelProjectName = QLabel(self.frame_2)
        self.labelProjectName.setObjectName(u"labelProjectName")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.labelProjectName.setFont(font1)
        self.labelProjectName.setTextFormat(Qt.PlainText)

        self.horizontalLayout_3.addWidget(self.labelProjectName)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.graphicsView = QGraphicsView(self.frame)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

        self.horizontalLayout_2.addWidget(self.graphicsView)


        self.verticalLayout.addWidget(self.frame)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.labelZoomFactor = QLabel(self.centralwidget)
        self.labelZoomFactor.setObjectName(u"labelZoomFactor")
        font2 = QFont()
        font2.setPointSize(10)
        self.labelZoomFactor.setFont(font2)

        self.horizontalLayout.addWidget(self.labelZoomFactor)

        self.sliderZoomFactor = QSlider(self.centralwidget)
        self.sliderZoomFactor.setObjectName(u"sliderZoomFactor")
        self.sliderZoomFactor.setMaximumSize(QSize(200, 16777215))
        self.sliderZoomFactor.setMinimum(10)
        self.sliderZoomFactor.setMaximum(200)
        self.sliderZoomFactor.setSingleStep(10)
        self.sliderZoomFactor.setValue(100)
        self.sliderZoomFactor.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.sliderZoomFactor)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1230, 21))
        self.menuok = QMenu(self.menubar)
        self.menuok.setObjectName(u"menuok")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QSize(0, 0))
        self.toolBar.setMaximumSize(QSize(75, 16777215))
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(48, 48))
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        self.dockAttributes = QDockWidget(MainWindow)
        self.dockAttributes.setObjectName(u"dockAttributes")
        self.dockAttributes.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockAttributes.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.treeAttributes = QTreeWidget(self.dockWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeAttributes.setHeaderItem(__qtreewidgetitem)
        self.treeAttributes.setObjectName(u"treeAttributes")
        self.treeAttributes.setMinimumSize(QSize(300, 200))
        self.treeAttributes.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.treeAttributes)

        self.dockAttributes.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockAttributes)
        self.dockProjectStructure = QDockWidget(MainWindow)
        self.dockProjectStructure.setObjectName(u"dockProjectStructure")
        self.dockProjectStructure.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockProjectStructure.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout_5 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lineFilterPattern = QLineEdit(self.dockWidgetContents_3)
        self.lineFilterPattern.setObjectName(u"lineFilterPattern")
        font3 = QFont()
        font3.setPointSize(9)
        self.lineFilterPattern.setFont(font3)

        self.verticalLayout_5.addWidget(self.lineFilterPattern)

        self.treeProjectStructure = QTreeWidget(self.dockWidgetContents_3)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.treeProjectStructure.setHeaderItem(__qtreewidgetitem1)
        self.treeProjectStructure.setObjectName(u"treeProjectStructure")
        self.treeProjectStructure.setMinimumSize(QSize(200, 200))

        self.verticalLayout_5.addWidget(self.treeProjectStructure)

        self.dockProjectStructure.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockProjectStructure)

        self.menubar.addAction(self.menuok.menuAction())
        self.menuok.addAction(self.actionNewProject)
        self.menuok.addAction(self.actionOpenProject)
        self.menuok.addAction(self.actionSaveProject)
        self.menuok.addAction(self.actionSaveProjectAs)
        self.menuok.addAction(self.actionCloseProject)
        self.menuok.addSeparator()
        self.menuok.addAction(self.actionExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionNewProject)
        self.toolBar.addAction(self.actionOpenProject)
        self.toolBar.addAction(self.actionSaveProject)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.actionNewProject.setText(QCoreApplication.translate("MainWindow", u"&New project", None))
#if QT_CONFIG(tooltip)
        self.actionNewProject.setToolTip(QCoreApplication.translate("MainWindow", u"Create new project", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionNewProject.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpenProject.setText(QCoreApplication.translate("MainWindow", u"&Open project", None))
#if QT_CONFIG(tooltip)
        self.actionOpenProject.setToolTip(QCoreApplication.translate("MainWindow", u"Open an existing project", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpenProject.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveProject.setText(QCoreApplication.translate("MainWindow", u"&Save project", None))
#if QT_CONFIG(tooltip)
        self.actionSaveProject.setToolTip(QCoreApplication.translate("MainWindow", u"Save project", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSaveProject.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionHome.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionCloseProject.setText(QCoreApplication.translate("MainWindow", u"Close project", None))
#if QT_CONFIG(tooltip)
        self.actionCloseProject.setToolTip(QCoreApplication.translate("MainWindow", u"Close current project", None))
#endif // QT_CONFIG(tooltip)
        self.actionRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
#if QT_CONFIG(tooltip)
        self.actionRun.setToolTip(QCoreApplication.translate("MainWindow", u"Run", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionRun.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveProjectAs.setText(QCoreApplication.translate("MainWindow", u"Save project as...", None))
#if QT_CONFIG(tooltip)
        self.actionSaveProjectAs.setToolTip(QCoreApplication.translate("MainWindow", u"Save project in a new file", None))
#endif // QT_CONFIG(tooltip)
        self.labelUserName.setText(QCoreApplication.translate("MainWindow", u"User name", None))
        self.labelProjectName.setText(QCoreApplication.translate("MainWindow", u"Project name", None))
        self.labelZoomFactor.setText(QCoreApplication.translate("MainWindow", u"100 %", None))
        self.menuok.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.dockAttributes.setWindowTitle(QCoreApplication.translate("MainWindow", u"Attributes", None))
        self.dockProjectStructure.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project structure", None))
        self.lineFilterPattern.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter agent type...", None))
    # retranslateUi

