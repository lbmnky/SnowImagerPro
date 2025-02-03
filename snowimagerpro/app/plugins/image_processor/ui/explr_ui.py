# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'explr.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QListWidget, QListWidgetItem, QSizePolicy, QSplitter,
    QTabWidget, QTextEdit, QTreeView, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(591, 661)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setLineWidth(2)
        self.splitter.setMidLineWidth(1)
        self.splitter.setOrientation(Qt.Vertical)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(True)

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 2)

        self.comboBox_2 = QComboBox(self.frame)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMaximumSize(QSize(200, 16777215))
        self.comboBox_2.setFrame(False)

        self.gridLayout.addWidget(self.comboBox_2, 0, 2, 1, 1)

        self.treeView = QTreeView(self.frame)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setDragDropMode(QAbstractItemView.DragOnly)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeView.setHeaderHidden(True)
        self.treeView.setExpandsOnDoubleClick(False)

        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 3)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 100))
        self.frame_3.setStyleSheet(u"background-color: rgb(61, 65, 76);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tabWidgetMetaExif = QTabWidget(self.frame_3)
        self.tabWidgetMetaExif.setObjectName(u"tabWidgetMetaExif")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.show_meta = QTextEdit(self.tab_1)
        self.show_meta.setObjectName(u"show_meta")
        self.show_meta.setStyleSheet(u"background-color: rgb(61, 65, 76);")
        self.show_meta.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.show_meta)

        self.tabWidgetMetaExif.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.show_exif = QTextEdit(self.tab_2)
        self.show_exif.setObjectName(u"show_exif")

        self.horizontalLayout_6.addWidget(self.show_exif)

        self.tabWidgetMetaExif.addTab(self.tab_2, "")

        self.horizontalLayout_4.addWidget(self.tabWidgetMetaExif)


        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 3)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalLayout_2.setStretch(0, 5)
        self.splitter.addWidget(self.frame)
        self.frame_2 = QFrame(self.splitter)
        self.frame_2.setObjectName(u"frame_2")
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.listWidget_nogrid_images = QListWidget(self.frame_2)
        self.listWidget_nogrid_images.setObjectName(u"listWidget_nogrid_images")
        self.listWidget_nogrid_images.setDragDropMode(QAbstractItemView.DropOnly)
        self.listWidget_nogrid_images.setSelectionMode(QAbstractItemView.SingleSelection)

        self.gridLayout_2.addWidget(self.listWidget_nogrid_images, 1, 0, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)

        self.listWidget_ref_images = QListWidget(self.frame_2)
        self.listWidget_ref_images.setObjectName(u"listWidget_ref_images")

        self.gridLayout_2.addWidget(self.listWidget_ref_images, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.listWidget_grid_images = QListWidget(self.frame_2)
        self.listWidget_grid_images.setObjectName(u"listWidget_grid_images")

        self.gridLayout_2.addWidget(self.listWidget_grid_images, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.splitter.addWidget(self.frame_2)

        self.verticalLayout.addWidget(self.splitter)

        QWidget.setTabOrder(self.comboBox, self.comboBox_2)
        QWidget.setTabOrder(self.comboBox_2, self.treeView)
        QWidget.setTabOrder(self.treeView, self.listWidget_nogrid_images)
        QWidget.setTabOrder(self.listWidget_nogrid_images, self.listWidget_grid_images)
        QWidget.setTabOrder(self.listWidget_grid_images, self.listWidget_ref_images)

        self.retranslateUi(Form)

        self.tabWidgetMetaExif.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidgetMetaExif.setTabText(self.tabWidgetMetaExif.indexOf(self.tab_1), QCoreApplication.translate("Form", u"Metadata", None))
        self.tabWidgetMetaExif.setTabText(self.tabWidgetMetaExif.indexOf(self.tab_2), QCoreApplication.translate("Form", u"EXIF", None))
        self.label.setText(QCoreApplication.translate("Form", u"Image", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Ref", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"With grid", None))
    # retranslateUi

