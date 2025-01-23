# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ctrls.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 657)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.title = QLabel(Form)
        self.title.setObjectName(u"title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setStyleSheet(u"background-color: transparent;")
        self.title.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)

        self.verticalLayout.addWidget(self.title)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.btn_close_views = QPushButton(Form)
        self.btn_close_views.setObjectName(u"btn_close_views")

        self.gridLayout.addWidget(self.btn_close_views, 7, 0, 1, 1)

        self.btn_add_def_dir = QPushButton(Form)
        self.btn_add_def_dir.setObjectName(u"btn_add_def_dir")

        self.gridLayout.addWidget(self.btn_add_def_dir, 5, 0, 1, 1)

        self.btn_load = QPushButton(Form)
        self.btn_load.setObjectName(u"btn_load")

        self.gridLayout.addWidget(self.btn_load, 4, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 8, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.btn_rmv_def_dir = QPushButton(Form)
        self.btn_rmv_def_dir.setObjectName(u"btn_rmv_def_dir")

        self.gridLayout.addWidget(self.btn_rmv_def_dir, 6, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        QWidget.setTabOrder(self.btn_load, self.btn_close_views)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title.setText(QCoreApplication.translate("Form", u"image_inspector ", None))
        self.btn_close_views.setText(QCoreApplication.translate("Form", u"Close all", None))
        self.btn_add_def_dir.setText(QCoreApplication.translate("Form", u"Add default directory", None))
        self.btn_load.setText(QCoreApplication.translate("Form", u"Load", None))
        self.btn_rmv_def_dir.setText(QCoreApplication.translate("Form", u"Remove default directory", None))
    # retranslateUi

