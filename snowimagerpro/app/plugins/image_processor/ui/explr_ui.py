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
    QGridLayout, QHeaderView, QLabel, QListWidget,
    QListWidgetItem, QSizePolicy, QSplitter, QTextEdit,
    QTreeView, QVBoxLayout, QWidget)

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
        self.comboBox_2 = QComboBox(self.frame)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMaximumSize(QSize(200, 16777215))
        self.comboBox_2.setFrame(False)

        self.gridLayout.addWidget(self.comboBox_2, 0, 2, 1, 1)

        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(True)

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 2)

        self.treeView = QTreeView(self.frame)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setDragDropMode(QAbstractItemView.DragOnly)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeView.setHeaderHidden(True)
        self.treeView.setExpandsOnDoubleClick(False)

        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 3)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.show_meta = QTextEdit(self.frame)
        self.show_meta.setObjectName(u"show_meta")
        self.show_meta.setStyleSheet(u"background-color: rgb(61, 65, 76);")
        self.show_meta.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.show_meta)

        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 2)
        self.splitter.addWidget(self.frame)
        self.frame_2 = QFrame(self.splitter)
        self.frame_2.setObjectName(u"frame_2")
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
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

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        QWidget.setTabOrder(self.comboBox, self.comboBox_2)
        QWidget.setTabOrder(self.comboBox_2, self.treeView)
        QWidget.setTabOrder(self.treeView, self.show_meta)
        QWidget.setTabOrder(self.show_meta, self.listWidget_nogrid_images)
        QWidget.setTabOrder(self.listWidget_nogrid_images, self.listWidget_grid_images)
        QWidget.setTabOrder(self.listWidget_grid_images, self.listWidget_ref_images)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Image", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Ref", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"With grid", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Use boxes to show connection between images", None))
    # retranslateUi

