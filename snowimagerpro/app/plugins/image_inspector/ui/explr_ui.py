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
    QGridLayout, QGroupBox, QHeaderView, QLabel,
    QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem,
    QSplitter, QTreeView, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(651, 656)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMidLineWidth(1)
        self.splitter.setOrientation(Qt.Vertical)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.treeView = QTreeView(self.frame)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView.header().setStretchLastSection(False)

        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 2)

        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(True)

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.splitter.addWidget(self.frame)
        self.groupBox_2 = QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.listWidget_3 = QListWidget(self.groupBox_2)
        self.listWidget_3.setObjectName(u"listWidget_3")

        self.gridLayout_2.addWidget(self.listWidget_3, 1, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.listWidget = QListWidget(self.groupBox_2)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setDragDropMode(QAbstractItemView.DropOnly)
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.gridLayout_2.addWidget(self.listWidget, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.listWidget_2 = QListWidget(self.groupBox_2)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.gridLayout_2.addWidget(self.listWidget_2, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.splitter.addWidget(self.groupBox_2)

        self.verticalLayout.addWidget(self.splitter)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_2.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Dark", None))
        self.label.setText(QCoreApplication.translate("Form", u"Image", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Ref", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Use boxes to manually assemble images for post-processing", None))
    # retranslateUi

