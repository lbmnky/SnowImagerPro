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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 623)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)

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
        self.title.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.title)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.btn_write_to_new_db = QPushButton(Form)
        self.btn_write_to_new_db.setObjectName(u"btn_write_to_new_db")

        self.gridLayout.addWidget(self.btn_write_to_new_db, 17, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_5, 4, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 6)
        self.checkBox_autosave = QCheckBox(Form)
        self.checkBox_autosave.setObjectName(u"checkBox_autosave")
        self.checkBox_autosave.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout.addWidget(self.checkBox_autosave)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 14, 0, 1, 1)

        self.btn_remove_image_from_db = QPushButton(Form)
        self.btn_remove_image_from_db.setObjectName(u"btn_remove_image_from_db")

        self.gridLayout.addWidget(self.btn_remove_image_from_db, 3, 0, 1, 1)

        self.btn_write_to_curr_db = QPushButton(Form)
        self.btn_write_to_curr_db.setObjectName(u"btn_write_to_curr_db")

        self.gridLayout.addWidget(self.btn_write_to_curr_db, 13, 0, 1, 1)

        self.btn_delete_db = QPushButton(Form)
        self.btn_delete_db.setObjectName(u"btn_delete_db")

        self.gridLayout.addWidget(self.btn_delete_db, 19, 0, 1, 1)

        self.btn_add_image_to_db = QPushButton(Form)
        self.btn_add_image_to_db.setObjectName(u"btn_add_image_to_db")

        self.gridLayout.addWidget(self.btn_add_image_to_db, 2, 0, 1, 1)

        self.btn_add_db = QPushButton(Form)
        self.btn_add_db.setObjectName(u"btn_add_db")

        self.gridLayout.addWidget(self.btn_add_db, 10, 0, 1, 1)

        self.pb_paste_metadata = QPushButton(Form)
        self.pb_paste_metadata.setObjectName(u"pb_paste_metadata")

        self.gridLayout.addWidget(self.pb_paste_metadata, 7, 0, 1, 1)

        self.pb_autolink_images = QPushButton(Form)
        self.pb_autolink_images.setObjectName(u"pb_autolink_images")
        self.pb_autolink_images.setEnabled(False)

        self.gridLayout.addWidget(self.pb_autolink_images, 8, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 9, 0, 1, 1)

        self.pb_copy_metadata = QPushButton(Form)
        self.pb_copy_metadata.setObjectName(u"pb_copy_metadata")

        self.gridLayout.addWidget(self.pb_copy_metadata, 6, 0, 1, 1)

        self.btn_remove_db = QPushButton(Form)
        self.btn_remove_db.setObjectName(u"btn_remove_db")

        self.gridLayout.addWidget(self.btn_remove_db, 18, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 20, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        QWidget.setTabOrder(self.btn_add_image_to_db, self.btn_remove_image_from_db)
        QWidget.setTabOrder(self.btn_remove_image_from_db, self.pb_copy_metadata)
        QWidget.setTabOrder(self.pb_copy_metadata, self.pb_paste_metadata)
        QWidget.setTabOrder(self.pb_paste_metadata, self.pb_autolink_images)
        QWidget.setTabOrder(self.pb_autolink_images, self.btn_add_db)
        QWidget.setTabOrder(self.btn_add_db, self.btn_write_to_curr_db)
        QWidget.setTabOrder(self.btn_write_to_curr_db, self.btn_write_to_new_db)
        QWidget.setTabOrder(self.btn_write_to_new_db, self.btn_remove_db)
        QWidget.setTabOrder(self.btn_remove_db, self.btn_delete_db)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title.setText(QCoreApplication.translate("Form", u"db_explorer ", None))
        self.btn_write_to_new_db.setText(QCoreApplication.translate("Form", u"Save a copy ...", None))
        self.checkBox_autosave.setText(QCoreApplication.translate("Form", u"Autosave", None))
        self.btn_remove_image_from_db.setText(QCoreApplication.translate("Form", u"remove image(s) from db", None))
        self.btn_write_to_curr_db.setText(QCoreApplication.translate("Form", u"Save database", None))
        self.btn_delete_db.setText(QCoreApplication.translate("Form", u"DELETE database", None))
        self.btn_add_image_to_db.setText(QCoreApplication.translate("Form", u"Add image(s) to db", None))
        self.btn_add_db.setText(QCoreApplication.translate("Form", u"Add/create database", None))
        self.pb_paste_metadata.setText(QCoreApplication.translate("Form", u"Paste metadata", None))
        self.pb_autolink_images.setText(QCoreApplication.translate("Form", u"Auto-link images (experimental)", None))
        self.pb_copy_metadata.setText(QCoreApplication.translate("Form", u"Copy metadata ...", None))
        self.btn_remove_db.setText(QCoreApplication.translate("Form", u"remove database", None))
    # retranslateUi

