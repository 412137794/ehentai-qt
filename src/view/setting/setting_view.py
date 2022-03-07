import base64
import os
import re
import sys
from functools import partial

from PySide2 import QtWidgets
from PySide2.QtCore import QSettings, Qt, QSize, QUrl, QFile, QTranslator, QLocale
from PySide2.QtGui import QDesktopServices
from PySide2.QtWidgets import QFileDialog

from config import config
from config.setting import Setting, SettingValue
from interface.ui_setting_new import Ui_SettingNew
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from view.tool.doh_dns_view import DohDnsView


class SettingView(QtWidgets.QWidget, Ui_SettingNew):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_SettingNew.__init__(self)
        self.setupUi(self)

        self.mainSize = None
        self.bookSize = None
        self.readSize = None
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []
        self.translate = QTranslator()
        self.translate2 = QTranslator()

        # RadioButton:
        self.themeGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ThemeIndex))
        self.languageGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.Language))
        self.logGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.LogIndex))
        self.mainScaleGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ScaleLevel))
        self.proxyGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.IsHttpProxy))

        # CheckButton:
        self.checkBox_IsUpdate.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUpdate, self.checkBox_IsUpdate))
        self.readCheckBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenWaifu, self.readCheckBox))
        self.coverCheckBox.clicked.connect(partial(self.CheckButtonEvent, Setting.CoverIsOpenWaifu, self.coverCheckBox))
        self.downAuto.clicked.connect(partial(self.CheckButtonEvent, Setting.DownloadAuto, self.downAuto))
        self.titleBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsNotUseTitleBar, self.titleBox))
        self.dohRadio.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenDoh, self.dohRadio))
        self.dohPictureRadio.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenDohPicture, self.dohPictureRadio))

        # LineEdit:
        self.httpEdit.editingFinished.connect(partial(self.LineEditEvent, Setting.HttpProxy, self.httpEdit))
        self.sockEdit.editingFinished.connect(partial(self.LineEditEvent, Setting.Sock5Proxy, self.sockEdit))
        self.dohLine.editingFinished.connect(partial(self.LineEditEvent, Setting.DohAddress, self.dohLine))

        # Button:

        # comboBox:
        # self.encodeSelect.currentIndexChanged.connect(partial(self.CheckRadioEvent, "LookReadMode"))
        self.readModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.LookModel))
        self.readNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.LookNoise))
        self.coverModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.CoverLookModel))
        self.coverNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.CoverLookNoise))
        self.downModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadModel))
        self.downNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadNoise))
        self.encodeSelect.currentTextChanged.connect(partial(self.CheckRadioEvent, Setting.SelectEncodeGpu))
        self.threadSelect.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.Waifu2xCpuCore))

        # spinBox
        # self.preDownNum.valueChanged.connect(partial(self.SpinBoxEvent, "", self.preDownNum))
        self.coverSize.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverSize))
        self.categorySize.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CategorySize))
        self.readScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.LookScale))
        self.coverScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverLookScale))
        self.downScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.DownloadScale))
        self.lookMaxBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.LookMaxNum))
        self.coverMaxBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverMaxNum))

        self.generalButton.clicked.connect(partial(self.MoveToLabel, self.generalLabel))
        # self.readButton.clicked.connect(partial(self.MoveToLabel, self.readLabel))
        self.proxyButton.clicked.connect(partial(self.MoveToLabel, self.proxyLabel))
        self.waifu2xButton.clicked.connect(partial(self.MoveToLabel, self.waifu2xLabel))
        self.downloadButton.clicked.connect(partial(self.MoveToLabel, self.downloadLabel))

        self.setDirButton.clicked.connect(self.SelectSavePath)
        self.openDownloadDir.clicked.connect(partial(self.OpenDir, self.downloadDir))
        # self.openChatDir.clicked.connect(partial(self.OpenDir, self.chatDir))
        self.openCacheDir.clicked.connect(partial(self.OpenDir, self.cacheDir))
        self.openWaifu2xDir.clicked.connect(partial(self.OpenDir, self.waifu2xDir))
        self.dohButton.clicked.connect(self.OpenDohView)

        self.msgLabel.setVisible(False)

    def MoveToLabel(self, label):
        p = label.pos()
        self.scrollArea.vScrollBar.ScrollTo(p.y())
        return

    def CheckMsgLabel(self):
        isNeed = False
        for name in dir(Setting):
            setItem = getattr(Setting, name)
            if isinstance(setItem, SettingValue):
                if setItem.isNeedReset:
                    if setItem.value != setItem.setV:
                        isNeed = True
        if isNeed:
            self.msgLabel.setVisible(True)
            QtOwner().ShowErrOne(Str.GetStr(Str.NeedResetSave))
        else:
            self.msgLabel.setVisible(False)
        return

    def ButtonClickEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        mo = re.search(r"\d+", button.objectName())
        if mo:
            value = int(mo.group())
            setItem.SetValue(value)
            if setItem == Setting.ThemeIndex:
                self.SetTheme()
            elif setItem == Setting.LogIndex:
                Log.UpdateLoggingLevel()
            elif setItem == Setting.Language:
                self.SetLanguage()
            elif setItem == Setting.IsHttpProxy:
                self.SetSock5Proxy()
            QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def CheckButtonEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(button.isChecked()))
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def CheckRadioEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(value)
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        if setItem == Setting.IsHttpProxy:
            self.SetSock5Proxy()
        self.CheckMsgLabel()
        return

    def LineEditEvent(self, setItem, lineEdit):
        assert isinstance(setItem, SettingValue)
        value = lineEdit.text()
        setItem.SetValue(value)
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def SpinBoxEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(value))
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def OpenDohView(self):
        view = DohDnsView(QtOwner().owner)
        view.exec_()

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh:
            self.InitSetting()
        return

    def LoadSetting(self):
        self.InitSetting()
        self.SetTheme()
        self.SetLanguage()
        self.SetSock5Proxy()
        return

    def ExitSaveSetting(self, mainQsize):
        return

    def InitSetting(self):
        self.checkBox_IsUpdate.setChecked(Setting.IsUpdate.value)
        self.SetRadioGroup("themeButton", Setting.ThemeIndex.value)
        self.SetRadioGroup("languageButton", Setting.Language.value)
        self.SetRadioGroup("mainScaleButton", Setting.ScaleLevel.value)
        self.SetRadioGroup("proxy", Setting.IsHttpProxy.value)
        self.coverSize.setValue(Setting.CoverSize.value)
        self.categorySize.setValue(Setting.CategorySize.value)
        self.SetRadioGroup("logutton", Setting.LogIndex.value)
        self.httpEdit.setText(Setting.HttpProxy.value)
        self.sockEdit.setText(Setting.Sock5Proxy.value)
        self.titleBox.setChecked(Setting.IsNotUseTitleBar.value)
        self.dohLine.setText(Setting.DohAddress.value)
        self.dohRadio.setChecked(Setting.IsOpenDoh.value)

        for index in range(self.encodeSelect.count()):
            if Setting.SelectEncodeGpu.value == self.encodeSelect.itemText(index):
                self.encodeSelect.setCurrentIndex(index)

        self.readCheckBox.setChecked(Setting.IsOpenWaifu.value)
        self.readNoise.setCurrentIndex(Setting.LookNoise.value)
        self.readScale.setValue(Setting.LookScale.value)
        self.readModel.setCurrentIndex(Setting.LookModel.value)

        self.coverCheckBox.setChecked(Setting.CoverIsOpenWaifu.value)
        self.coverNoise.setCurrentIndex(Setting.CoverLookNoise.value)
        self.coverScale.setValue(Setting.CoverLookScale.value)
        self.coverModel.setCurrentIndex(Setting.CoverLookModel.value)

        self.downAuto.setChecked(Setting.DownloadAuto.value)
        self.downNoise.setCurrentIndex(Setting.DownloadNoise.value)
        self.downScale.setValue(Setting.DownloadScale.value)
        self.downModel.setCurrentIndex(Setting.DownloadModel.value)
        self.SetDownloadLabel()

    def retranslateUi(self, SettingNew):
        Ui_SettingNew.retranslateUi(self, SettingNew)
        self.SetDownloadLabel()

    def SetRadioGroup(self, text, index):
        radio = getattr(self, text+str(index))
        if radio:
            radio.setChecked(True)

    def SetSock5Proxy(self):
        try:
            import socket
            import socks
            if not QtOwner().backSock:
                QtOwner().backSock = socket.socket
            if Setting.IsHttpProxy.value == 2 and Setting.Sock5Proxy.value:
                data = Setting.Sock5Proxy.value.replace("http://", "").replace("https://", "").replace("sock5://", "").replace("socks5://", "")
                data = data.split(":")
                if len(data) == 2:
                    host = data[0]
                    port = data[1]
                    socks.set_default_proxy(socks.SOCKS5, host, int(port))
                    socket.socket = socks.socksocket
                else:
                    QtOwner().ShowMsg(Str.GetStr(Str.Sock5Error))
            else:
                socks.set_default_proxy()
                socket.socket = QtOwner().backSock
        except Exception as es:
            Log.Error(es)
            QtOwner().ShowMsg(Str.GetStr(Str.Sock5Error))

    def SetLanguage(self):
        language = Setting.Language.value

        # Auto
        if language == 0:
            locale = QLocale.system().name()
            Log.Info("Init translate {}".format(locale))
            if locale[:3].lower() == "zh_":
                if locale.lower() == "zh_cn":
                    language = 1
                else:
                    language = 2
            else:
                language = 3

        if language == Setting.Language.autoValue:
            return

        Setting.Language.autoValue = language

        if language == 1:
            QtOwner().app.removeTranslator(self.translate)
            QtOwner().app.removeTranslator(self.translate2)
        elif language == 2:
            self.translate.load(QLocale(), ":/file/tr/str_hk.qm")
            self.translate2.load(QLocale(), ":/file/tr/ui_hk.qm")
            QtOwner().app.installTranslator(self.translate2)
            QtOwner().app.installTranslator(self.translate)
        else:
            self.translate.load(QLocale(), ":/file/tr/str_en.qm")
            self.translate2.load(QLocale(), ":/file/tr/ui_en.qm")
            QtOwner().app.installTranslator(self.translate2)
            QtOwner().app.installTranslator(self.translate)
        Str.Reload()
        QtOwner().owner.RetranslateUi()

    def SetTheme(self):
        themeId = Setting.ThemeIndex.value
        if themeId == 0:
            themeId = self.GetSysColor()

        if themeId == Setting.ThemeIndex.autoValue:
            return

        Setting.ThemeIndex.autoValue = themeId

        if themeId == 1:
            f = QFile(":/file/theme/dark_pink.qss")
        else:
            f = QFile(":/file/theme/light_pink.qss")
        f.open(QFile.ReadOnly)
        data = str(f.readAll(), encoding='utf-8')
        QtOwner().app.setStyleSheet(data)
        self.SetSettingTheme(themeId)
        f.close()

    def SetSettingTheme(self, themId):
        if themId != 1:
            qss = """
                .QFrame
                {
                    background-color: rgb(253, 253, 253);
                    
                    border:2px solid rgb(234,234,234);
                    border-radius:5px
                }        
                """
        else:
            qss = """
                .QFrame
                {
                    background-color: rgb(50, 50, 50);

                    border:2px solid rgb(35,35,35);
                    border-radius:5px
                }        
                """
        self.scrollArea.setStyleSheet(qss)

    def GetSysColor(self):
        # TODO
        # MacOS 和 KDE如何获取系统颜色
        if sys.platform == "win32":
            return self.GetWinSysColor() + 1
        elif sys.platform == "darwin":
            return self.GetMacOsSysColor()
        return 1

    def GetWinSysColor(self):
        path = "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = "AppsUseLightTheme"
        settings = QSettings(path, QSettings.Format.NativeFormat)
        value = settings.value(key, 0)
        return value

    def GetMacOsSysColor(self):
        try:
            import subprocess
            cmd = "defaults read -g AppleInterfaceStyle"
            results = subprocess.getoutput(cmd)
            if results == "Dark":
                return 1
            else:
                return 2
        except Exception as es:
            Log.Error(es)
        return 1

    def SaveSetting(self):
        return

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            Setting.SavePath.SetValue(url)
        self.SetDownloadLabel()

    def SetDownloadLabel(self):
        url = Setting.SavePath.value
        if not url:
            url = "./"
        self.downloadDir.setText(os.path.join(url, config.SavePathDir))
        self.cacheDir.setText(os.path.join(url, config.CachePathDir))
        self.waifu2xDir.setText(os.path.join(os.path.join(url, config.CachePathDir), config.Waifu2xPath))

    def OpenDir(self, label):
        QDesktopServices.openUrl(QUrl.fromLocalFile(label.text()))
        return

    def SetGpuInfos(self, gpuInfo, cpuNum):
        self.gpuInfos = gpuInfo
        config.EncodeGpu = Setting.SelectEncodeGpu.value

        if not self.gpuInfos:
            config.EncodeGpu = "CPU"
            config.Encode = -1
            self.encodeSelect.addItem(config.EncodeGpu)
            self.encodeSelect.setCurrentIndex(0)

        if not config.EncodeGpu or (config.EncodeGpu != "CPU" and config.EncodeGpu not in self.gpuInfos):
            config.EncodeGpu = self.gpuInfos[0]
            config.Encode = 0

        index = 0
        if self.gpuInfos:
            for info in self.gpuInfos:
                self.encodeSelect.addItem(info)
                if info == config.EncodeGpu:
                    self.encodeSelect.setCurrentIndex(index)
                    config.Encode = index
                index += 1

        self.encodeSelect.addItem("CPU")
        if config.EncodeGpu == "CPU":
            config.Encode = -1
            self.encodeSelect.setCurrentIndex(index)

        config.UseCpuNum = Setting.Waifu2xCpuCore.value
        if config.UseCpuNum > cpuNum:
            config.UseCpuNum = cpuNum
        for i in range(cpuNum):
            self.threadSelect.addItem(str(i + 1))
        self.threadSelect.setCurrentIndex(config.UseCpuNum)

        Log.Info("waifu2x GPU: " + str(self.gpuInfos) + ",select: " + str(config.EncodeGpu) + ",use cpu num: " + str(config.UseCpuNum))
        return

    def GetGpuName(self):
        return config.EncodeGpu
        # index = config.Encode
        # if index >= len(self.gpuInfos) or index < 0:
        #     return "GPU"
        # return self.gpuInfos[index]

    def OpenWaifu2xHelp(self):
        return
        # QDesktopServices.openUrl(QUrl(config.Waifu2xUrl))