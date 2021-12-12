import os
import shutil

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QTimer, QUrl
from PySide2.QtGui import QCursor, QDesktopServices
from PySide2.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem, QAction

from config import config
from config.setting import Setting
from interface.ui_download import Ui_Download
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
from view.download.download_db import DownloadDb
from view.download.download_info import DownloadInfo


class DownloadView(QtWidgets.QWidget, Ui_Download):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Download.__init__(self)
        self.setupUi(self)
        self.downloadingList = []  # 正在下载列表
        self.downloadList = []  # 下载队列
        self.downloadDict = {}  # bookId ：downloadInfo
        self.convertList = []
        self.convertingList = []

        # if config.Language == "English":
        #     HorizontalHeaderLabels = ["id", "Title", "Download Status", "Download Progress", "Download Chapters", "Download Speed", "Convert Progress", "Covert Chapters", "Covert Time", "Convert Status"]
        # else:
        #     HorizontalHeaderLabels = ["id", "标题", "下载状态", "下载进度", "下载章节", "下载速度", "转换进度", "转换章节", "转换耗时", "转换状态"]

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tableWidget.setColumnCount(10)
        # self.tableWidget.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        self.timer = QTimer(self.tableWidget)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.UpdateTable)
        self.timer.start()

        # self.settings = QSettings('download.ini', QSettings.IniFormat)
        # self.InitSetting()

        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)

        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)

        self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)
        self.order = {}

        self.db = DownloadDb()
        self.radioButton.setChecked(Setting.DownloadAuto.value)
        datas = self.db.LoadDownload(self)
        for task in datas.values():
            self.downloadDict[task.bookId] = task
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            task.status = self.GetNewStatus(task.status)
            task.convertStatus = self.GetNewStatus(task.convertStatus)
            if task.status != DownloadInfo.Success:
                task.status = DownloadInfo.Pause
            if task.convertStatus != DownloadInfo.ConvertSuccess:
                task.convertStatus = DownloadInfo.Pause
            self.tableWidget.insertRow(rowCont)
            self.UpdateTableItem(task)

    def GetNewStatus(self, status):

        if status.isnumeric():
            return int(status)
        # 兼容老數據
        infos = [DownloadInfo.Success, DownloadInfo.Reading, DownloadInfo.ReadingEps, DownloadInfo.ReadingPicture, DownloadInfo.Downloading, DownloadInfo.Waiting,
         DownloadInfo.Pause, DownloadInfo.Error, DownloadInfo.NotFound, DownloadInfo.ConvertSuccess, DownloadInfo.Converting]
        for i in infos:
            if Str.GetStr(i) == status:
                return i
        return DownloadInfo.Pause

    def Close(self):
        self.timer.stop()

    def GetDownloadEpsId(self, bookId):
        if bookId not in self.downloadDict:
            return []
        return self.downloadDict[bookId].downloadEpsIds

    def GetDownloadCompleteEpsId(self, bookId):
        if bookId not in self.downloadDict:
            return []
        return self.downloadDict[bookId].GetDownloadCompleteEpsId()

    def GetConvertFilePath(self, bookId, epsId, index):
        if bookId not in self.downloadDict:
            return ""
        task = self.downloadDict[bookId]
        if epsId not in task.epsInfo:
            return ""
        epsTitle = task.epsInfo[epsId].epsTitle
        savePath = os.path.join(task.convertPath, ToolUtil.GetCanSaveName(epsTitle))
        return os.path.join(savePath, "{:04}.{}".format(index + 1, "jpg"))

    def GetDonwloadFilePath(self, bookId, epsId, index):
        if bookId not in self.downloadDict:
            return ""
        task = self.downloadDict[bookId]
        savePath = task.savePath
        return os.path.join(savePath, "{:04}.{}".format(index + 1, "jpg"))

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh:
            for task in self.downloadDict.values():
                self.UpdateTableItem(task)
        pass

    def UpdateTable(self):
        for task in self.downloadingList:
            assert isinstance(task, DownloadInfo)
            if task.status != task.Downloading:
                continue
            task.speedStr = ToolUtil.GetDownloadSize(task.speed) + "/s"
            task.speed = 0
            self.UpdateTableItem(task)

    def AddDownload(self, bookId, token, site):
        if bookId not in self.downloadDict:
            task = DownloadInfo(self)
            task.bookId = bookId
            task.token = token
            task.domain = site
            self.downloadDict[task.bookId] = task
            self.downloadList.append(task)
            rowCont = self.tableWidget.rowCount()
            task.tableRow = rowCont
            self.tableWidget.insertRow(rowCont)
        else:
            task = self.downloadDict.get(bookId)
            if task.status == task.Success:
                task.status = task.Waiting
                if task not in self.downloadList:
                    self.downloadList.append(task)
            if task.convertStatus == task.Converting:
                task.SetConvertStatu(task.Pause)
            elif task.convertStatus == task.ConvertSuccess:
                task.SetConvertStatu(task.Waiting)
        self.UpdateTableItem(task)
        self.HandlerDownloadList()
        self.db.AddDownloadDB(task)
        return True

    def AddConvert(self, bookId):
        if bookId not in self.downloadDict:
            return False
        task = self.downloadDict.get(bookId)
        if task not in self.convertList:
            self.convertList.append(task)
        self.HandlerConvertList()

    def HandlerDownloadList(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.downloadingList)

        if addNum <= 0:
            return

        for _ in range(addNum):
            if len(self.downloadList) <= 0:
                return
            for task in list(self.downloadList):
                assert isinstance(task, DownloadInfo)
                if task.status != DownloadInfo.Waiting:
                    continue
                self.downloadList.remove(task)
                self.downloadingList.append(task)
                task.status = DownloadInfo.Downloading
                task.AddBookPicInfos()
                self.UpdateTableItem(task)
                break
        pass

    def HandlerConvertList(self):
        downloadNum = config.DownloadThreadNum
        addNum = downloadNum - len(self.convertingList)

        if addNum <= 0:
            return

        for _ in range(addNum):
            if len(self.convertList) <= 0:
                return
            for task in list(self.convertList):
                assert isinstance(task, DownloadInfo)
                if task.status != DownloadInfo.Success:
                    continue
                if task.convertStatus != DownloadInfo.Waiting:
                    continue
                self.convertList.remove(task)
                self.convertingList.append(task)
                task.convertStatus = DownloadInfo.Converting
                task.StartConvert()
                self.UpdateTableItem(task)
                break
        pass

    def UpdateTableItem(self, info):
        assert isinstance(info, DownloadInfo)
        self.tableWidget.setItem(info.tableRow, 0, QTableWidgetItem(info.bookId))
        self.tableWidget.setItem(info.tableRow, 1, QTableWidgetItem(info.title))
        self.tableWidget.setItem(info.tableRow, 2, QTableWidgetItem(info.domain))
        self.tableWidget.setItem(info.tableRow, 3, QTableWidgetItem(Str.GetStr(info.status)))
        self.tableWidget.setItem(info.tableRow, 4,
                                 QTableWidgetItem("{}/{}".format(str(info.curDownloadPic), str(info.maxDownloadPic))))
        self.tableWidget.setItem(info.tableRow, 5, QTableWidgetItem(ToolUtil.GetDownloadSize(info.size)))
        self.tableWidget.setItem(info.tableRow, 6, QTableWidgetItem(info.speedStr))
        self.tableWidget.setItem(info.tableRow, 7, QTableWidgetItem("{}/{}".format(str(info.curConvertCnt), str(info.convertCnt))))
        self.tableWidget.setItem(info.tableRow, 8, QTableWidgetItem("{}".format(str(info.convertTick))))
        self.tableWidget.setItem(info.tableRow, 9, QTableWidgetItem(Str.GetStr(info.convertStatus)))
        self.tableWidget.update()
        return

    def RemoveRecord(self, bookId):
        task = self.downloadDict.get(bookId)
        if not task:
            return
        assert isinstance(task, DownloadInfo)
        task.SetStatu(task.Pause)
        task.SetConvertStatu(task.Pause)
        if task in self.downloadingList:
            self.downloadingList.remove(task)
        if task in self.downloadList:
            self.downloadList.remove(task)
        if task in self.convertList:
            self.convertList.remove(task)
        if task in self.convertingList:
            self.convertingList.remove(task)
        self.downloadDict.pop(bookId)
        self.tableWidget.removeRow(task.tableRow)
        self.db.DelDownloadDB(bookId)

    def UpdateTableRow(self):
        count = self.tableWidget.rowCount()
        for i in range(count):
            bookId = self.tableWidget.item(i, 0).text()
            info = self.downloadDict.get(bookId)
            if info:
                info.tableRow = i

    # 右键菜单
    def SelectMenu(self, pos):
        index = self.tableWidget.indexAt(pos)
        openDirAction = QAction(Str.GetStr(Str.OpenDir), self)
        openDirAction.triggered.connect(self.ClickOpenFilePath)

        pauseAction = QAction(Str.GetStr(Str.Pause), self)
        pauseAction.triggered.connect(self.ClickPause)

        removeAction = QAction(Str.GetStr(Str.DeleteRecord), self)
        removeAction.triggered.connect(self.DelRecording)

        removeFileAction = QAction(Str.GetStr(Str.DeleteRecordFile), self)
        removeFileAction.triggered.connect(self.DelRecordingAndFile)

        # self.openDirAction = QAction("打开目录", self)
        # self.openDirAction.triggered.connect(self.ClickOpenFilePath)

        # selectEpsAction = QAction(Str.GetStr(Str.SelectEps), self)
        # selectEpsAction.triggered.connect(self.ClickDownloadEps)

        startAction = QAction(Str.GetStr(Str.Start), self)
        startAction.triggered.connect(self.ClickStart)

        startConvertAction = QAction(Str.GetStr(Str.StartConvert), self)
        startConvertAction.triggered.connect(self.ClickConvertStart)

        pauseConvertAction = QAction(Str.GetStr(Str.PauseConvert), self)
        pauseConvertAction.triggered.connect(self.ClickConvertPause)

        if index.isValid():
            selected = self.tableWidget.selectedIndexes()
            selectRows = set()
            for index in selected:
                selectRows.add(index.row())
            if not selectRows:
                return
            if len(selectRows) == 1:
                # 单选
                row = selectRows.pop()
                col = 0
                bookId = self.tableWidget.item(row, col).text()
                task = self.downloadDict.get(bookId)
                if not task:
                    return

                menu = QMenu(self.tableWidget)

                menu.addAction(openDirAction)
                # menu.addAction(selectEpsAction)
                assert isinstance(task, DownloadInfo)
                if task.status in [DownloadInfo.Pause, DownloadInfo.Error]:
                    menu.addAction(startAction)
                elif task.status in [DownloadInfo.Downloading, DownloadInfo.Waiting,
                                     DownloadInfo.Reading, DownloadInfo.ReadingPicture, DownloadInfo.ReadingEps]:
                    menu.addAction(pauseAction)
                else:
                    if task.convertStatus in [DownloadInfo.Converting]:
                        menu.addAction(pauseConvertAction)
                    elif task.convertStatus in [DownloadInfo.Pause, DownloadInfo.Error, DownloadInfo.NotFound]:
                        menu.addAction(startConvertAction)
            else:
                menu = QMenu(self.tableWidget)

            menu.addAction(removeAction)
            menu.addAction(removeFileAction)
            menu.exec_(QCursor.pos())
        pass

    def ClickOpenFilePath(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        # 只去第一个
        row = selectRows.pop()
        col = 0
        bookId = self.tableWidget.item(row, col).text()
        task = self.downloadDict.get(bookId)
        assert isinstance(task, DownloadInfo)
        QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(task.savePath)))
        return

    def ClickPause(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status in [DownloadInfo.Success]:
                continue
            if task in self.downloadingList:
                self.downloadingList.remove(task)
            task.SetStatu(task.Pause)
        self.HandlerDownloadList()
        return

    def ClickConvertPause(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.convertStatus in [DownloadInfo.ConvertSuccess]:
                continue
            if task in self.convertingList:
                self.convertingList.remove(task)
            task.SetConvertStatu(task.Pause)
        self.HandlerConvertList()
        return

    def ClickStart(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue
            # task.status = DownloadInfo.Reading

            if task not in self.downloadList:
                self.downloadList.append(task)
            task.SetStatu(task.Waiting)
        self.HandlerDownloadList()

    def ClickConvertStart(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in selectRows:
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.convertStatus not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue
            # task.status = DownloadInfo.Reading
            if task not in self.convertList:
                self.convertList.append(task)
            task.SetConvertStatu(task.Waiting)
        self.HandlerConvertList()

    def DelRecording(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        for row in sorted(selectRows, reverse=True):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            self.RemoveRecord(bookId)
        self.UpdateTableRow()

    def DelRecordingAndFile(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if not selectRows:
            return
        try:
            for row in sorted(selectRows, reverse=True):
                col = 0
                bookId = self.tableWidget.item(row, col).text()
                bookInfo = self.downloadDict.get(bookId)
                if not bookInfo:
                    continue
                self.RemoveRecord(bookId)
                path = os.path.dirname(bookInfo.savePath)
                if os.path.isdir(path):
                    shutil.rmtree(path, True)

        except Exception as es:
            Log.Error(es)
        self.UpdateTableRow()

    def OpenBookInfo(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if len(selectRows) > 1:
            return
        if len(selectRows) <= 0:
            return
        row = list(selectRows)[0]
        col = 0
        bookId = self.tableWidget.item(row, col).text()
        if not bookId:
            return
        info = self.downloadDict.get(bookId)
        if not info:
            return
        QtOwner().OpenBookInfo(bookId, info.token)

    def StartAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue

            if task not in self.downloadList:
                self.downloadList.append(task)
            task.SetStatu(task.Waiting)
        self.HandlerDownloadList()

    def StopAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status in [DownloadInfo.Success]:
                continue
            if task in self.downloadingList:
                self.downloadingList.remove(task)
            task.SetStatu(task.Pause)

    def StartConvertAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.status not in [DownloadInfo.Success]:
                continue
            if task.convertStatus not in [DownloadInfo.Pause, DownloadInfo.Error]:
                continue
            # task.status = DownloadInfo.Reading
            if task not in self.convertList:
                self.convertList.append(task)
            task.SetConvertStatu(task.Waiting)
        self.HandlerConvertList()

    def StopConvertAll(self):
        for row in range(self.tableWidget.rowCount()):
            col = 0
            bookId = self.tableWidget.item(row, col).text()
            task = self.downloadDict.get(bookId)
            if not task:
                continue
            if task.convertStatus in [DownloadInfo.ConvertSuccess]:
                continue
            if task in self.convertingList:
                self.convertingList.remove(task)
            task.SetConvertStatu(task.Pause)

    def SetAutoConvert(self):
        Setting.DownloadAuto.SetValue(int(self.radioButton.isChecked()))

    def Sort(self, col):
        order = self.order.get(col, 1)
        if order == 1:
            self.tableWidget.sortItems(col, Qt.AscendingOrder)
            self.order[col] = 0
        else:
            self.tableWidget.sortItems(col, Qt.DescendingOrder)
            self.order[col] = 1
        self.UpdateTableRow()
