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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(302, 878)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_5)

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
        self.btn_load_img = QPushButton(Form)
        self.btn_load_img.setObjectName(u"btn_load_img")

        self.gridLayout.addWidget(self.btn_load_img, 7, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 14, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 13, 0, 1, 1)

        self.btn_add_db = QPushButton(Form)
        self.btn_add_db.setObjectName(u"btn_add_db")

        self.gridLayout.addWidget(self.btn_add_db, 2, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_4, 10, 0, 1, 1)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 100))
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.doubleSpinBox_2 = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")

        self.gridLayout_2.addWidget(self.doubleSpinBox_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 11, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 17, 0, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 100))
        self.groupBox.setSizeIncrement(QSize(0, 0))
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")

        self.gridLayout_3.addWidget(self.doubleSpinBox, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 8, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_6, 6, 0, 1, 1)

        self.btn_calc_SSA = QPushButton(Form)
        self.btn_calc_SSA.setObjectName(u"btn_calc_SSA")

        self.gridLayout.addWidget(self.btn_calc_SSA, 9, 0, 1, 1)

        self.btn_add_h5 = QPushButton(Form)
        self.btn_add_h5.setObjectName(u"btn_add_h5")

        self.gridLayout.addWidget(self.btn_add_h5, 3, 0, 1, 1)

        self.btn_rmv_h5 = QPushButton(Form)
        self.btn_rmv_h5.setObjectName(u"btn_rmv_h5")

        self.gridLayout.addWidget(self.btn_rmv_h5, 4, 0, 1, 1)

        self.btn_prnt_rep = QPushButton(Form)
        self.btn_prnt_rep.setObjectName(u"btn_prnt_rep")

        self.gridLayout.addWidget(self.btn_prnt_rep, 15, 0, 1, 1)

        self.btn_calc_rho = QPushButton(Form)
        self.btn_calc_rho.setObjectName(u"btn_calc_rho")

        self.gridLayout.addWidget(self.btn_calc_rho, 12, 0, 1, 1)

        self.btn_rmv_db = QPushButton(Form)
        self.btn_rmv_db.setObjectName(u"btn_rmv_db")

        self.gridLayout.addWidget(self.btn_rmv_db, 5, 0, 1, 1)

        self.btn_close_views = QPushButton(Form)
        self.btn_close_views.setObjectName(u"btn_close_views")

        self.gridLayout.addWidget(self.btn_close_views, 16, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        QWidget.setTabOrder(self.btn_add_db, self.btn_add_h5)
        QWidget.setTabOrder(self.btn_add_h5, self.btn_rmv_h5)
        QWidget.setTabOrder(self.btn_rmv_h5, self.btn_rmv_db)
        QWidget.setTabOrder(self.btn_rmv_db, self.btn_load_img)
        QWidget.setTabOrder(self.btn_load_img, self.doubleSpinBox)
        QWidget.setTabOrder(self.doubleSpinBox, self.btn_calc_SSA)
        QWidget.setTabOrder(self.btn_calc_SSA, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.btn_calc_rho)
        QWidget.setTabOrder(self.btn_calc_rho, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.btn_prnt_rep)
        QWidget.setTabOrder(self.btn_prnt_rep, self.btn_close_views)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title.setText(QCoreApplication.translate("Form", u"image_analyzer ", None))
        self.btn_load_img.setText(QCoreApplication.translate("Form", u"Load data", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Save output as ...", None))
        self.btn_add_db.setText(QCoreApplication.translate("Form", u"Add database", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"density parameters", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"SSA parameters", None))
        self.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btn_calc_SSA.setText(QCoreApplication.translate("Form", u"Calculate SSA", None))
        self.btn_add_h5.setText(QCoreApplication.translate("Form", u"Add H5 to database", None))
        self.btn_rmv_h5.setText(QCoreApplication.translate("Form", u"Remove H5 from database", None))
        self.btn_prnt_rep.setText(QCoreApplication.translate("Form", u"Print report", None))
        self.btn_calc_rho.setText(QCoreApplication.translate("Form", u"Calculate density profile", None))
        self.btn_rmv_db.setText(QCoreApplication.translate("Form", u"Remove database", None))
        self.btn_close_views.setText(QCoreApplication.translate("Form", u"Close all", None))
    # retranslateUi

