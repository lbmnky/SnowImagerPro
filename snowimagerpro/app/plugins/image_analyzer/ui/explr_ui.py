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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QListView,
    QSizePolicy, QToolButton, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(934, 670)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.le_data_directory = QLineEdit(Form)
        self.le_data_directory.setObjectName(u"le_data_directory")

        self.gridLayout.addWidget(self.le_data_directory, 1, 0, 1, 1)

        self.btn_change_data_dir = QToolButton(Form)
        self.btn_change_data_dir.setObjectName(u"btn_change_data_dir")

        self.gridLayout.addWidget(self.btn_change_data_dir, 1, 1, 1, 1)

        self.treeWidget = QTreeWidget(Form)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"comment");
        __qtreewidgetitem.setText(0, u"filename");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setEditTriggers(QAbstractItemView.SelectedClicked)
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.header().setDefaultSectionSize(600)
        self.treeWidget.header().setProperty(u"showSortIndicator", False)

        self.gridLayout.addWidget(self.treeWidget, 2, 0, 1, 2)

        self.cb_change_db = QComboBox(Form)
        self.cb_change_db.setObjectName(u"cb_change_db")

        self.gridLayout.addWidget(self.cb_change_db, 0, 0, 1, 2)

        self.listView_2 = QListView(Form)
        self.listView_2.setObjectName(u"listView_2")

        self.gridLayout.addWidget(self.listView_2, 4, 0, 1, 2)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_change_data_dir.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Results from current post-processing", None))
    # retranslateUi

