import json
import os
import pickle
import threading
import time
from queue import Queue
from zlib import crc32

from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QImage

from config import config
from config.setting import Setting
from tools.log import Log
from tools.status import Status
from tools.singleton import Singleton
from tools.str import Str
from tools.tool import CTime, ToolUtil


class QtTaskQObject(QObject):
    taskBack = Signal(int, bytes)
    downloadBack = Signal(int, int, bytes)
    downloadStBack = Signal(int, str)
    convertBack = Signal(int)
    imageBack = Signal(int, QImage)

    def __init__(self):
        super(self.__class__, self).__init__()


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


class QtTaskBase:
    Id = 1

    def __init__(self):
        self.__taskFlagId = QtTaskBase.Id
        QtTaskBase.Id += 1

    @property
    def req(self):
        return

    # callBack(data)
    # callBack(data, backParam)
    def AddHttpTask(self, req, callBack=None, backParam=None):
        from tools.qt_domain import QtDomainMgr
        from task.task_http import TaskHttp
        if not Setting.IsOpenDoh.value:
            return TaskHttp().AddHttpTask(req, callBack, backParam, cleanFlag=self.__taskFlagId)
        else:
            return QtDomainMgr().AddHttpTask(req, callBack, backParam, cleanFlag=self.__taskFlagId)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadBook(self, bookId, index, token="", domain=config.CurSite, statusBack=None, downloadCallBack=None, completeCallBack=None, backParam=None, isSaveCache=True, isSaveFile=False, filePath=""):
        from task.task_download import TaskDownload
        return TaskDownload().DownloadBook(bookId, index, token, domain, statusBack, downloadCallBack, completeCallBack, backParam, isSaveCache, self.__taskFlagId, isSaveFile, filePath)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, backParam=None, isSaveCache=True, isSaveFile=False, filePath="", isReload=False):
        from tools.qt_domain import QtDomainMgr
        from task.task_download import TaskDownload
        if not Setting.IsOpenDohPicture.value:
            return TaskDownload().DownloadTask(url, path, downloadCallBack, completeCallBack, backParam, isSaveCache, self.__taskFlagId, isSaveFile, filePath, isReload)
        else:
            return QtDomainMgr.AddDownloadTask(url, path, downloadCallBack, completeCallBack, backParam, isSaveCache, self.__taskFlagId, isSaveFile, filePath, isReload)

    @classmethod
    def GetCoverKey(cls, bookId, token, site):
        return "{}/{}_{}_cover".format(site, bookId, token)

    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().AddConvertTaskByData(path, imgData, model, completeCallBack, backParam, self.__taskFlagId)

    def AddQImageTask(self, data, callBack=None, backParam=None):
        from task.task_qimage import TaskQImage
        return TaskQImage().AddQImageTask(data, callBack, backParam, cleanFlag=self.__taskFlagId)

    def ClearTask(self):
        from task.task_http import TaskHttp
        return TaskHttp().Cancel(self.__taskFlagId)

    def ClearDownload(self):
        from task.task_download import TaskDownload
        return TaskDownload().Cancel(self.__taskFlagId)
    
    def ClearConvert(self):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().Cancel(self.__taskFlagId)

    def ClearWaitConvertIds(self, taskIds):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().ClearWaitConvertIds(taskIds)

    def ClearQImageTask(self):
        from task.task_qimage import TaskQImage
        return TaskQImage().Cancel(self.__taskFlagId)


class QtDownloadTask(object):
    Waiting = Str.Waiting
    Reading = Str.Reading
    ReadingPicture = Str.ReadingPicture
    Downloading = Str.Downloading
    Success = Str.Success
    Error = Str.Error

    def __init__(self, downloadId=0):
        self.downloadId = downloadId
        self.downloadCallBack = None       # addData, laveSize
        self.downloadCompleteBack = None   # data, status

        self.status = self.Waiting
        self.statusBack = None             # data, status
        self.domain = config.CurSite
        self.fileSize = 0
        self.saveData = b""
        self.bookId = ""
        self.index = ""
        self.site = ""
        self.token = ""
        self.isSaveCache = ""
        self.isSaveFile = False
        self.resetCnt = 0
        self.cacheCallBack = ""   # 临时保存一个callback，因为

        self.originalName = ""
        self.backParam = None
        self.cleanFlag = ""
        self.tick = 0
        self.cacheAndLoadPath = ""   # 保存和加载
        self.loadPath = ""           # 只加载

        self.imgData = b""
        self.scale = 0
        self.noise = 0
        self.model = {
            "model": 1,
            "scale": 2,
            "toH": 100,
            "toW": 100,
        }


class TaskBase(Singleton):
    taskId = 0
    taskObj = QtTaskQObject()

    def __init__(self):
        Singleton.__init__(self)
        self.thread = threading.Thread(target=self.Run)
        self.thread.setName("Task-" + str(self.__class__.__name__))
        self.thread.setDaemon(True)
        self._inQueue = Queue()
        self.tasks = {}
        self.flagToIds = {}

    def Stop(self):
        self._inQueue.put("")
        return

    def Run(self):
        return

    def Cancel(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
        self.flagToIds.pop(cleanFlag)
