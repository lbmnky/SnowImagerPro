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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QSizePolicy, QSpacerItem, QSplitter, QToolButton,
    QVBoxLayout, QWidget)

from pyqtgraph import ImageView
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(830, 673)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Vertical)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_chang_data_dir = QToolButton(self.frame)
        self.btn_chang_data_dir.setObjectName(u"btn_chang_data_dir")

        self.gridLayout_3.addWidget(self.btn_chang_data_dir, 1, 1, 1, 1)

        self.le_data_directory = QLineEdit(self.frame)
        self.le_data_directory.setObjectName(u"le_data_directory")
        self.le_data_directory.setEnabled(False)

        self.gridLayout_3.addWidget(self.le_data_directory, 1, 0, 1, 1)

        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_3.addWidget(self.comboBox, 0, 0, 1, 2)

        self.listView = QListView(self.frame)
        self.listView.setObjectName(u"listView")
        self.listView.setFocusPolicy(Qt.StrongFocus)
        self.listView.setFrameShape(QFrame.NoFrame)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setDragEnabled(True)
        self.listView.setDragDropMode(QAbstractItemView.InternalMove)
        self.listView.setDefaultDropAction(Qt.MoveAction)
        self.listView.setAlternatingRowColors(False)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout_3.addWidget(self.listView, 2, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.splitter.addWidget(self.frame)
        self.frame_2 = QFrame(self.splitter)
        self.frame_2.setObjectName(u"frame_2")
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.cb_update_coords_pix = QCheckBox(self.frame_2)
        self.cb_update_coords_pix.setObjectName(u"cb_update_coords_pix")
        self.cb_update_coords_pix.setLayoutDirection(Qt.RightToLeft)
        self.cb_update_coords_pix.setTristate(True)

        self.gridLayout.addWidget(self.cb_update_coords_pix, 2, 6, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.cb_update_ROIs = QCheckBox(self.frame_2)
        self.cb_update_ROIs.setObjectName(u"cb_update_ROIs")
        self.cb_update_ROIs.setLayoutDirection(Qt.RightToLeft)
        self.cb_update_ROIs.setTristate(True)

        self.gridLayout.addWidget(self.cb_update_ROIs, 2, 4, 1, 1)

        self.le_filepath = QLineEdit(self.frame_2)
        self.le_filepath.setObjectName(u"le_filepath")
        self.le_filepath.setReadOnly(True)

        self.gridLayout.addWidget(self.le_filepath, 2, 1, 1, 3)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.graphWidget = ImageView(self.frame_3)
        self.graphWidget.setObjectName(u"graphWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy2)
        self.graphWidget.setMinimumSize(QSize(50, 50))

        self.horizontalLayout_2.addWidget(self.graphWidget)


        self.gridLayout.addWidget(self.frame_3, 4, 2, 3, 5)

        self.verticalSpacer_3 = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 2, 1, 1)

        self.details = QGroupBox(self.frame_2)
        self.details.setObjectName(u"details")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.details.sizePolicy().hasHeightForWidth())
        self.details.setSizePolicy(sizePolicy3)
        self.details.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.gridLayout_2 = QGridLayout(self.details)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, -1, -1, 0)
        self.le_coords_mm = QLineEdit(self.details)
        self.le_coords_mm.setObjectName(u"le_coords_mm")

        self.gridLayout_2.addWidget(self.le_coords_mm, 11, 1, 1, 2)

        self.label_11 = QLabel(self.details)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 12, 0, 1, 1)

        self.label_9 = QLabel(self.details)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_9, 8, 0, 1, 1)

        self.label_10 = QLabel(self.details)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 14, 0, 1, 1)

        self.label_6 = QLabel(self.details)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_2 = QLabel(self.details)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.le_coords_pix = QLineEdit(self.details)
        self.le_coords_pix.setObjectName(u"le_coords_pix")
        self.le_coords_pix.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_coords_pix, 12, 1, 1, 2)

        self.label_4 = QLabel(self.details)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_4, 1, 2, 1, 1)

        self.cb_img_type = QComboBox(self.details)
        self.cb_img_type.setObjectName(u"cb_img_type")
        self.cb_img_type.setEditable(True)

        self.gridLayout_2.addWidget(self.cb_img_type, 2, 0, 1, 1)

        self.le_comment = QLineEdit(self.details)
        self.le_comment.setObjectName(u"le_comment")

        self.gridLayout_2.addWidget(self.le_comment, 14, 1, 1, 2)

        self.cb_ref_group = QComboBox(self.details)
        self.cb_ref_group.setObjectName(u"cb_ref_group")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.cb_ref_group.sizePolicy().hasHeightForWidth())
        self.cb_ref_group.setSizePolicy(sizePolicy4)
        self.cb_ref_group.setEditable(True)

        self.gridLayout_2.addWidget(self.cb_ref_group, 2, 2, 1, 1)

        self.dsb_px2mm = QDoubleSpinBox(self.details)
        self.dsb_px2mm.setObjectName(u"dsb_px2mm")
        self.dsb_px2mm.setDecimals(4)
        self.dsb_px2mm.setSingleStep(0.000100000000000)
        self.dsb_px2mm.setValue(0.315000000000000)

        self.gridLayout_2.addWidget(self.dsb_px2mm, 4, 2, 1, 1)

        self.label_3 = QLabel(self.details)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)

        self.label_5 = QLabel(self.details)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.gridLayout_2.addWidget(self.label_5, 3, 1, 1, 1)

        self.le_date = QLineEdit(self.details)
        self.le_date.setObjectName(u"le_date")
        self.le_date.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_date, 6, 1, 1, 2)

        self.cb_meas_group = QComboBox(self.details)
        self.cb_meas_group.setObjectName(u"cb_meas_group")
        self.cb_meas_group.setFocusPolicy(Qt.WheelFocus)
        self.cb_meas_group.setEditable(True)

        self.gridLayout_2.addWidget(self.cb_meas_group, 4, 0, 1, 1)

        self.label_12 = QLabel(self.details)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 3, 2, 1, 1)

        self.label_7 = QLabel(self.details)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 6, 0, 1, 1)

        self.cb_wavelength = QComboBox(self.details)
        self.cb_wavelength.setObjectName(u"cb_wavelength")
        self.cb_wavelength.setEditable(True)

        self.gridLayout_2.addWidget(self.cb_wavelength, 4, 1, 1, 1)

        self.label_8 = QLabel(self.details)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setLayoutDirection(Qt.LeftToRight)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_8, 11, 0, 1, 1)

        self.cb_location = QComboBox(self.details)
        self.cb_location.setObjectName(u"cb_location")
        self.cb_location.setEditable(True)

        self.gridLayout_2.addWidget(self.cb_location, 8, 1, 1, 2)

        self.cb_drk_group = QComboBox(self.details)
        self.cb_drk_group.setObjectName(u"cb_drk_group")
        self.cb_drk_group.setEditable(True)

        self.gridLayout_2.addWidget(self.cb_drk_group, 2, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 15, 0, 1, 1)

        self.gridLayout_2.setRowStretch(15, 1)

        self.gridLayout.addWidget(self.details, 3, 0, 4, 2)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 7)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 5, 1, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(1, 4)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(6, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.splitter.addWidget(self.frame_2)

        self.verticalLayout_3.addWidget(self.splitter)

        QWidget.setTabOrder(self.comboBox, self.le_data_directory)
        QWidget.setTabOrder(self.le_data_directory, self.btn_chang_data_dir)
        QWidget.setTabOrder(self.btn_chang_data_dir, self.cb_img_type)
        QWidget.setTabOrder(self.cb_img_type, self.cb_drk_group)
        QWidget.setTabOrder(self.cb_drk_group, self.cb_ref_group)
        QWidget.setTabOrder(self.cb_ref_group, self.le_comment)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_chang_data_dir.setText(QCoreApplication.translate("Form", u"...", None))
        self.cb_update_coords_pix.setText(QCoreApplication.translate("Form", u"Coords_pix", None))
        self.label.setText(QCoreApplication.translate("Form", u"filename ", None))
        self.cb_update_ROIs.setText(QCoreApplication.translate("Form", u"ROIs", None))
#if QT_CONFIG(whatsthis)
        self.details.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Change image parameters</span></p><p><br/></p><p>Can be applied to several images simultaneously.</p><p><img src=\":/doc/resources/doc/db_explorer_multiselect_parameter_change.png\"/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.details.setTitle("")
        self.label_11.setText(QCoreApplication.translate("Form", u"Coords pix", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"location", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Comment", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"meas_group", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"img_type", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"ref_group", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"drk_group", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"wavelength", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Pixel 2 mm", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"date", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Coords mm", None))
    # retranslateUi

