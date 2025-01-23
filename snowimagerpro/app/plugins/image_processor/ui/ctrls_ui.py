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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDoubleSpinBox,
    QGridLayout, QGroupBox, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(367, 861)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.title = QLabel(Form)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setAutoFillBackground(False)
        self.title.setStyleSheet(u"background-color:  transparent;")
        self.title.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)

        self.verticalLayout.addWidget(self.title)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.btn_undistort_images = QPushButton(Form)
        self.btn_undistort_images.setObjectName(u"btn_undistort_images")
        self.btn_undistort_images.setFlat(True)

        self.gridLayout.addWidget(self.btn_undistort_images, 9, 0, 1, 4)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.cb_peview_on_load = QCheckBox(self.groupBox_4)
        self.cb_peview_on_load.setObjectName(u"cb_peview_on_load")

        self.verticalLayout_3.addWidget(self.cb_peview_on_load)

        self.cb_preview_dark = QCheckBox(self.groupBox_4)
        self.cb_preview_dark.setObjectName(u"cb_preview_dark")

        self.verticalLayout_3.addWidget(self.cb_preview_dark)


        self.gridLayout.addWidget(self.groupBox_4, 22, 0, 1, 1)

        self.btn_show_processed = QPushButton(Form)
        self.btn_show_processed.setObjectName(u"btn_show_processed")
        self.btn_show_processed.setMinimumSize(QSize(0, 0))
        self.btn_show_processed.setFlat(True)

        self.gridLayout.addWidget(self.btn_show_processed, 10, 0, 1, 4)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 18, 0, 1, 3)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBox_5 = QCheckBox(self.groupBox_2)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout_4.addWidget(self.checkBox_5)

        self.cb_show_output = QCheckBox(self.groupBox_2)
        self.cb_show_output.setObjectName(u"cb_show_output")
        self.cb_show_output.setEnabled(False)
        self.cb_show_output.setChecked(False)

        self.verticalLayout_4.addWidget(self.cb_show_output)


        self.gridLayout.addWidget(self.groupBox_2, 23, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(2, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 19, 3, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 21, 0, 1, 3)

        self.btn_save = QPushButton(Form)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(0, 0))
        self.btn_save.setFlat(True)

        self.gridLayout.addWidget(self.btn_save, 16, 0, 1, 4)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.sb_overlap_y = QDoubleSpinBox(self.groupBox_3)
        self.sb_overlap_y.setObjectName(u"sb_overlap_y")
        self.sb_overlap_y.setDecimals(0)
        self.sb_overlap_y.setMaximum(10000.000000000000000)

        self.gridLayout_4.addWidget(self.sb_overlap_y, 2, 1, 1, 1)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)

        self.sb_overlap_x = QDoubleSpinBox(self.groupBox_3)
        self.sb_overlap_x.setObjectName(u"sb_overlap_x")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sb_overlap_x.sizePolicy().hasHeightForWidth())
        self.sb_overlap_x.setSizePolicy(sizePolicy1)
        self.sb_overlap_x.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.sb_overlap_x.setDecimals(0)
        self.sb_overlap_x.setMaximum(10000.000000000000000)

        self.gridLayout_4.addWidget(self.sb_overlap_x, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 2)

        self.gridLayout_4.setColumnStretch(1, 1)

        self.gridLayout.addWidget(self.groupBox_3, 23, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_5, 15, 0, 1, 3)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cb_preview_ref = QCheckBox(self.groupBox)
        self.cb_preview_ref.setObjectName(u"cb_preview_ref")
        self.cb_preview_ref.setChecked(True)

        self.verticalLayout_2.addWidget(self.cb_preview_ref)

        self.btn_debug = QCheckBox(self.groupBox)
        self.btn_debug.setObjectName(u"btn_debug")

        self.verticalLayout_2.addWidget(self.btn_debug)


        self.gridLayout.addWidget(self.groupBox, 22, 1, 1, 2)

        self.btn_write_metadata = QPushButton(Form)
        self.btn_write_metadata.setObjectName(u"btn_write_metadata")
        self.btn_write_metadata.setEnabled(False)
        self.btn_write_metadata.setFlat(True)

        self.gridLayout.addWidget(self.btn_write_metadata, 17, 0, 1, 4)

        self.output_folder = QPlainTextEdit(Form)
        self.output_folder.setObjectName(u"output_folder")
        self.output_folder.setMaximumSize(QSize(16777215, 50))
        self.output_folder.setTabChangesFocus(True)

        self.gridLayout.addWidget(self.output_folder, 19, 0, 1, 2)

        self.btn_stitch = QPushButton(Form)
        self.btn_stitch.setObjectName(u"btn_stitch")
        sizePolicy.setHeightForWidth(self.btn_stitch.sizePolicy().hasHeightForWidth())
        self.btn_stitch.setSizePolicy(sizePolicy)
        self.btn_stitch.setMinimumSize(QSize(0, 0))
        self.btn_stitch.setFlat(True)

        self.gridLayout.addWidget(self.btn_stitch, 14, 0, 1, 4)

        self.btn_close_views = QPushButton(Form)
        self.btn_close_views.setObjectName(u"btn_close_views")
        self.btn_close_views.setMinimumSize(QSize(0, 0))
        self.btn_close_views.setFlat(True)

        self.gridLayout.addWidget(self.btn_close_views, 12, 0, 1, 4)

        self.btn_set_filepath_out = QToolButton(Form)
        self.btn_set_filepath_out.setObjectName(u"btn_set_filepath_out")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_set_filepath_out.sizePolicy().hasHeightForWidth())
        self.btn_set_filepath_out.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_set_filepath_out, 19, 2, 1, 1)

        self.btn_refl_calib = QPushButton(Form)
        self.btn_refl_calib.setObjectName(u"btn_refl_calib")
        self.btn_refl_calib.setFlat(True)

        self.gridLayout.addWidget(self.btn_refl_calib, 8, 0, 1, 4)

        self.btn_ffc = QPushButton(Form)
        self.btn_ffc.setObjectName(u"btn_ffc")
        self.btn_ffc.setMinimumSize(QSize(0, 0))
        self.btn_ffc.setFlat(True)

        self.gridLayout.addWidget(self.btn_ffc, 6, 0, 1, 4)

        self.btn_preview = QPushButton(Form)
        self.btn_preview.setObjectName(u"btn_preview")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_preview.sizePolicy().hasHeightForWidth())
        self.btn_preview.setSizePolicy(sizePolicy4)
        self.btn_preview.setMinimumSize(QSize(0, 0))
        self.btn_preview.setFlat(True)

        self.gridLayout.addWidget(self.btn_preview, 2, 0, 2, 4)

        self.btn_reset = QPushButton(Form)
        self.btn_reset.setObjectName(u"btn_reset")
        self.btn_reset.setEnabled(False)
        self.btn_reset.setFocusPolicy(Qt.TabFocus)
        self.btn_reset.setFlat(True)

        self.gridLayout.addWidget(self.btn_reset, 1, 0, 1, 4)

        self.btn_load = QPushButton(Form)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setMinimumSize(QSize(0, 0))
        self.btn_load.setSizeIncrement(QSize(0, 50))
        self.btn_load.setFocusPolicy(Qt.TabFocus)
        self.btn_load.setFlat(True)

        self.gridLayout.addWidget(self.btn_load, 0, 0, 1, 4)

        self.gridLayout.setColumnStretch(0, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(2, 1)
        QWidget.setTabOrder(self.btn_load, self.btn_reset)
        QWidget.setTabOrder(self.btn_reset, self.btn_preview)
        QWidget.setTabOrder(self.btn_preview, self.btn_ffc)
        QWidget.setTabOrder(self.btn_ffc, self.btn_refl_calib)
        QWidget.setTabOrder(self.btn_refl_calib, self.btn_undistort_images)
        QWidget.setTabOrder(self.btn_undistort_images, self.btn_show_processed)
        QWidget.setTabOrder(self.btn_show_processed, self.btn_close_views)
        QWidget.setTabOrder(self.btn_close_views, self.btn_stitch)
        QWidget.setTabOrder(self.btn_stitch, self.btn_save)
        QWidget.setTabOrder(self.btn_save, self.btn_write_metadata)
        QWidget.setTabOrder(self.btn_write_metadata, self.output_folder)
        QWidget.setTabOrder(self.output_folder, self.btn_set_filepath_out)
        QWidget.setTabOrder(self.btn_set_filepath_out, self.cb_peview_on_load)
        QWidget.setTabOrder(self.cb_peview_on_load, self.cb_preview_dark)
        QWidget.setTabOrder(self.cb_preview_dark, self.cb_preview_ref)
        QWidget.setTabOrder(self.cb_preview_ref, self.btn_debug)
        QWidget.setTabOrder(self.btn_debug, self.sb_overlap_x)
        QWidget.setTabOrder(self.sb_overlap_x, self.sb_overlap_y)
        QWidget.setTabOrder(self.sb_overlap_y, self.checkBox_5)
        QWidget.setTabOrder(self.checkBox_5, self.cb_show_output)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title.setText(QCoreApplication.translate("Form", u"image_processor ", None))
        self.btn_undistort_images.setText(QCoreApplication.translate("Form", u"Undistort images", None))
        self.groupBox_4.setTitle("")
        self.cb_peview_on_load.setText(QCoreApplication.translate("Form", u"Auto preview", None))
        self.cb_preview_dark.setText(QCoreApplication.translate("Form", u"Show dark", None))
        self.btn_show_processed.setText(QCoreApplication.translate("Form", u"Show processed", None))
        self.groupBox_2.setTitle("")
        self.checkBox_5.setText(QCoreApplication.translate("Form", u"Smooth", None))
        self.cb_show_output.setText(QCoreApplication.translate("Form", u"Ouput", None))
        self.btn_save.setText(QCoreApplication.translate("Form", u"Save as H5", None))
        self.groupBox_3.setTitle("")
        self.label.setText(QCoreApplication.translate("Form", u"OverlapX", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"OverlapY", None))
        self.sb_overlap_x.setPrefix("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Stitch parameters", None))
        self.groupBox.setTitle("")
        self.cb_preview_ref.setText(QCoreApplication.translate("Form", u"reference", None))
        self.btn_debug.setText(QCoreApplication.translate("Form", u"DEBUG", None))
        self.btn_write_metadata.setText(QCoreApplication.translate("Form", u"Write changed metadata", None))
        self.btn_stitch.setText(QCoreApplication.translate("Form", u"Stitch", None))
        self.btn_close_views.setText(QCoreApplication.translate("Form", u"Close all", None))
        self.btn_set_filepath_out.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_refl_calib.setText(QCoreApplication.translate("Form", u"Reflectance calibration", None))
        self.btn_ffc.setText(QCoreApplication.translate("Form", u"Flat-field correction", None))
        self.btn_preview.setText(QCoreApplication.translate("Form", u"Preview", None))
        self.btn_reset.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.btn_load.setText(QCoreApplication.translate("Form", u"Load selected", None))
    # retranslateUi

