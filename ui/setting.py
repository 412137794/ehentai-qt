# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Setting(object):
    def setupUi(self, Setting):
        if not Setting.objectName():
            Setting.setObjectName(u"Setting")
        Setting.resize(616, 530)
        self.gridLayout_2 = QGridLayout(Setting)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(Setting)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_16 = QLabel(Setting)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 12, 0, 1, 1)

        self.label_10 = QLabel(Setting)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 14, 0, 1, 1)

        self.line_7 = QFrame(Setting)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_7, 5, 0, 1, 1)

        self.line_3 = QFrame(Setting)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_3, 9, 0, 1, 1)

        self.preDownNum = QSpinBox(Setting)
        self.preDownNum.setObjectName(u"preDownNum")
        self.preDownNum.setMinimum(1)
        self.preDownNum.setValue(10)

        self.gridLayout_3.addWidget(self.preDownNum, 3, 2, 1, 1)

        self.line_6 = QFrame(Setting)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_6, 13, 2, 1, 1)

        self.label_8 = QLabel(Setting)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 7, 0, 1, 1)

        self.encodeSelect = QComboBox(Setting)
        self.encodeSelect.setObjectName(u"encodeSelect")

        self.gridLayout_3.addWidget(self.encodeSelect, 8, 2, 1, 1)

        self.threadSelect = QComboBox(Setting)
        self.threadSelect.addItem("")
        self.threadSelect.setObjectName(u"threadSelect")

        self.gridLayout_3.addWidget(self.threadSelect, 7, 2, 1, 1)

        self.label_3 = QLabel(Setting)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 8, 0, 1, 1)

        self.logBox = QComboBox(Setting)
        self.logBox.addItem("")
        self.logBox.addItem("")
        self.logBox.addItem("")
        self.logBox.setObjectName(u"logBox")

        self.gridLayout_3.addWidget(self.logBox, 14, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.saveEdit = QLineEdit(Setting)
        self.saveEdit.setObjectName(u"saveEdit")

        self.horizontalLayout_4.addWidget(self.saveEdit)

        self.pushButton = QPushButton(Setting)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 4, 2, 1, 1)

        self.label_6 = QLabel(Setting)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 6, 0, 1, 1)

        self.checkBox = QCheckBox(Setting)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_3.addWidget(self.checkBox, 6, 2, 1, 1)

        self.label = QLabel(Setting)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.NoFrame)

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(Setting)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)

        self.line = QFrame(Setting)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line, 11, 0, 1, 1)

        self.line_4 = QFrame(Setting)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_4, 9, 2, 1, 1)

        self.label_4 = QLabel(Setting)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_19 = QLabel(Setting)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_5.addWidget(self.label_19, 2, 0, 1, 1)

        self.label_17 = QLabel(Setting)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_18 = QLabel(Setting)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_5.addWidget(self.label_18, 1, 0, 1, 1)

        self.downAuto = QCheckBox(Setting)
        self.downAuto.setObjectName(u"downAuto")
        self.downAuto.setChecked(True)

        self.gridLayout_5.addWidget(self.downAuto, 3, 0, 1, 1)

        self.downNoise = QComboBox(Setting)
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.addItem("")
        self.downNoise.setObjectName(u"downNoise")

        self.gridLayout_5.addWidget(self.downNoise, 0, 2, 1, 1)

        self.downModel = QComboBox(Setting)
        self.downModel.addItem("")
        self.downModel.addItem("")
        self.downModel.addItem("")
        self.downModel.addItem("")
        self.downModel.setObjectName(u"downModel")

        self.gridLayout_5.addWidget(self.downModel, 1, 2, 1, 1)

        self.downScale = QDoubleSpinBox(Setting)
        self.downScale.setObjectName(u"downScale")
        self.downScale.setDecimals(1)
        self.downScale.setMaximum(32.000000000000000)
        self.downScale.setSingleStep(0.100000000000000)
        self.downScale.setValue(2.000000000000000)

        self.gridLayout_5.addWidget(self.downScale, 2, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 12, 2, 1, 1)

        self.label_12 = QLabel(Setting)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 10, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.httpProxy = QCheckBox(Setting)
        self.httpProxy.setObjectName(u"httpProxy")

        self.horizontalLayout_5.addWidget(self.httpProxy)

        self.httpEdit = QLineEdit(Setting)
        self.httpEdit.setObjectName(u"httpEdit")

        self.horizontalLayout_5.addWidget(self.httpEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 2, 1, 1)

        self.label_7 = QLabel(Setting)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)

        self.line_8 = QFrame(Setting)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_8, 5, 2, 1, 1)

        self.line_2 = QFrame(Setting)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_2, 11, 2, 1, 1)

        self.label_5 = QLabel(Setting)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 4, 0, 1, 1)

        self.comboBox = QComboBox(Setting)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_3.addWidget(self.comboBox, 1, 2, 1, 1)

        self.line_5 = QFrame(Setting)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_5, 13, 0, 1, 1)

        self.themeBox = QComboBox(Setting)
        self.themeBox.addItem("")
        self.themeBox.addItem("")
        self.themeBox.addItem("")
        self.themeBox.setObjectName(u"themeBox")

        self.gridLayout_3.addWidget(self.themeBox, 0, 2, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.readNoise = QComboBox(Setting)
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.addItem("")
        self.readNoise.setObjectName(u"readNoise")

        self.gridLayout_4.addWidget(self.readNoise, 0, 2, 1, 1)

        self.label_13 = QLabel(Setting)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 0, 0, 1, 1)

        self.readModel = QComboBox(Setting)
        self.readModel.addItem("")
        self.readModel.addItem("")
        self.readModel.addItem("")
        self.readModel.addItem("")
        self.readModel.setObjectName(u"readModel")

        self.gridLayout_4.addWidget(self.readModel, 1, 2, 1, 1)

        self.label_15 = QLabel(Setting)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 2, 0, 1, 1)

        self.label_14 = QLabel(Setting)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 1, 0, 1, 1)

        self.readScale = QDoubleSpinBox(Setting)
        self.readScale.setObjectName(u"readScale")
        self.readScale.setDecimals(1)
        self.readScale.setMaximum(32.000000000000000)
        self.readScale.setSingleStep(0.100000000000000)
        self.readScale.setValue(2.000000000000000)

        self.gridLayout_4.addWidget(self.readScale, 2, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 10, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Setting)
        self.buttonBox.accepted.connect(Setting.SaveSetting)
        self.buttonBox.rejected.connect(Setting.close)
        self.pushButton.clicked.connect(Setting.SelectSavePath)

        QMetaObject.connectSlotsByName(Setting)
    # setupUi

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(QCoreApplication.translate("Setting", u"Form", None))
        self.label_16.setText(QCoreApplication.translate("Setting", u"waifu2x\u4e0b\u8f7d\u6a21\u5f0f", None))
        self.label_10.setText(QCoreApplication.translate("Setting", u"\u65e5\u5fd7\u7b49\u7ea7", None))
        self.label_8.setText(QCoreApplication.translate("Setting", u"waifu2x\u7ebf\u7a0b\u6570", None))
        self.threadSelect.setItemText(0, QCoreApplication.translate("Setting", u"2", None))

        self.label_3.setText(QCoreApplication.translate("Setting", u"\u89e3\u7801\u5668\uff08\u9700\u91cd\u542f\uff09", None))
        self.logBox.setItemText(0, QCoreApplication.translate("Setting", u"WARN", None))
        self.logBox.setItemText(1, QCoreApplication.translate("Setting", u"INFO", None))
        self.logBox.setItemText(2, QCoreApplication.translate("Setting", u"DEBUG", None))

        self.pushButton.setText(QCoreApplication.translate("Setting", u"...", None))
        self.label_6.setText(QCoreApplication.translate("Setting", u"waifu2x\u8bbe\u7f6e", None))
        self.checkBox.setText(QCoreApplication.translate("Setting", u"\u662f\u5426\u542f\u7528", None))
        self.label.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u7ebf\u7a0b\u6570", None))
        self.label_2.setText(QCoreApplication.translate("Setting", u"http\u4ee3\u7406", None))
        self.label_4.setText(QCoreApplication.translate("Setting", u"\u4e3b\u9898", None))
        self.label_19.setText(QCoreApplication.translate("Setting", u"\u653e\u5927\u500d\u6570", None))
        self.label_17.setText(QCoreApplication.translate("Setting", u"\u53bb\u566a\u7b49\u7ea7", None))
        self.label_18.setText(QCoreApplication.translate("Setting", u"\u6a21\u578b", None))
        self.downAuto.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u5b8c\u540e\u81ea\u52a8\u8f6c\u6362", None))
        self.downNoise.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.downNoise.setItemText(1, QCoreApplication.translate("Setting", u"0", None))
        self.downNoise.setItemText(2, QCoreApplication.translate("Setting", u"1", None))
        self.downNoise.setItemText(3, QCoreApplication.translate("Setting", u"2", None))
        self.downNoise.setItemText(4, QCoreApplication.translate("Setting", u"3", None))

        self.downModel.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.downModel.setItemText(1, QCoreApplication.translate("Setting", u"cunet", None))
        self.downModel.setItemText(2, QCoreApplication.translate("Setting", u"photo", None))
        self.downModel.setItemText(3, QCoreApplication.translate("Setting", u"anime_style_art_rgb", None))

        self.label_12.setText(QCoreApplication.translate("Setting", u"Waifu2x\u770b\u56fe\u6a21\u5f0f", None))
        self.httpProxy.setText(QCoreApplication.translate("Setting", u"\u542f\u7528\u4ee3\u7406", None))
        self.httpEdit.setPlaceholderText(QCoreApplication.translate("Setting", u"http://127.0.0.1:10809", None))
        self.label_7.setText(QCoreApplication.translate("Setting", u"\u770b\u56fe\u9884\u52a0\u8f7d\u6570", None))
        self.label_5.setText(QCoreApplication.translate("Setting", u"\u4e0b\u8f7d\u548c\u7f13\u5b58\u8def\u5f84", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Setting", u"2", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Setting", u"3", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Setting", u"4", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Setting", u"5", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Setting", u"6", None))

        self.comboBox.setPlaceholderText("")
        self.themeBox.setItemText(0, QCoreApplication.translate("Setting", u"\u9ed8\u8ba4\uff08\u9700\u91cd\u542f\uff09", None))
        self.themeBox.setItemText(1, QCoreApplication.translate("Setting", u"\u9ed1", None))
        self.themeBox.setItemText(2, QCoreApplication.translate("Setting", u"\u767d", None))

        self.readNoise.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.readNoise.setItemText(1, QCoreApplication.translate("Setting", u"0", None))
        self.readNoise.setItemText(2, QCoreApplication.translate("Setting", u"1", None))
        self.readNoise.setItemText(3, QCoreApplication.translate("Setting", u"2", None))
        self.readNoise.setItemText(4, QCoreApplication.translate("Setting", u"3", None))

        self.label_13.setText(QCoreApplication.translate("Setting", u"\u53bb\u566a\u7b49\u7ea7", None))
        self.readModel.setItemText(0, QCoreApplication.translate("Setting", u"\u81ea\u52a8", None))
        self.readModel.setItemText(1, QCoreApplication.translate("Setting", u"cunet", None))
        self.readModel.setItemText(2, QCoreApplication.translate("Setting", u"photo", None))
        self.readModel.setItemText(3, QCoreApplication.translate("Setting", u"anime_style_art_rgb", None))

        self.label_15.setText(QCoreApplication.translate("Setting", u"\u653e\u5927\u500d\u6570", None))
        self.label_14.setText(QCoreApplication.translate("Setting", u"\u6a21\u578b", None))
    # retranslateUi

