import weakref

from PySide2.QtCore import Qt, QEvent, QPoint, QRect
from PySide2.QtGui import QPainter, QColor, QPixmap, QFont, QFontMetrics, QPen, QBrush
from PySide2.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QFrame, QGraphicsItemGroup, QGraphicsItem, \
    QAbstractSlider, QLabel

from conf import config
from resources.resources import DataMgr
from src.qt.com.DWaterProgress import DWaterProgress
from src.qt.com.qt_git_label import QtGifLabel
from src.qt.com.qt_scroll import QtComGraphicsView
from src.qt.com.qtmsg import QtMsgLabel
from src.qt.read.qtreadimg_tool import QtImgTool


class QtImgFrame(QFrame):
    def __init__(self, readImg):
        QFrame.__init__(self)
        self._readImg = weakref.ref(readImg)
        self.graphicsView = QtComGraphicsView(self)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorUnderMouse)
        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.qtTool = QtImgTool(self)
        self.qtTool.hide()
        self.helpLabel = QLabel(self)
        self.helpPixMap = QPixmap()
        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        # self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setResizeAnchor(self.graphicsView.AnchorViewCenter)
        self.graphicsView.setTransformationAnchor(self.graphicsView.AnchorViewCenter)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(self.graphicsView.CacheBackground)
        self.graphicsView.setViewportUpdateMode(self.graphicsView.SmartViewportUpdate)

        self.graphicsItem1 = QGraphicsPixmapItem()
        self.graphicsItem1.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsItem2 = QGraphicsPixmapItem()
        self.graphicsItem2.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsItem3 = QGraphicsPixmapItem()
        self.graphicsItem3.setFlags(QGraphicsPixmapItem.ItemIsFocusable)

        self.graphicsGroup = QGraphicsItemGroup()
        self.graphicsGroup.setFlag(QGraphicsItem.ItemIsFocusable)
        self.graphicsGroup.addToGroup(self.graphicsItem1)
        self.graphicsGroup.addToGroup(self.graphicsItem2)
        self.graphicsGroup.addToGroup(self.graphicsItem3)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsScene.addItem(self.graphicsGroup)

        self.graphicsView.setMinimumSize(10, 10)

        self.helpLabel.installEventFilter(self)
        self.graphicsScene.installEventFilter(self)
        # self.graphicsView.installEventFilter(self)
        # self.graphicsItem.installSceneEventFilter(self.graphicsItem)

        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)
        self.pixMapList = [QPixmap(), QPixmap(), QPixmap()]
        self.graphicsItemList = [self.graphicsItem1, self.graphicsItem2, self.graphicsItem3]

        self.scaleCnt = 2
        self.startPos = QPoint()
        self.endPos = QPoint()
        self.process = DWaterProgress(self)
        self.waifu2xProcess = QtGifLabel(self)
        self.waifu2xProcess.setVisible(False)

        self.waifu2xProcess.Init(DataMgr.GetData("loading_gif"))
        self.downloadSize = 1
        self.downloadMaxSize = 1
        self.oldValue = -1
        self.graphicsView.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        self.graphicsView.horizontalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        # self.graphicsView.verticalScrollBar().setSingleStep(100)
        # self.graphicsView.verticalScrollBar().setPageStep(100)
        self.graphicsView.setSceneRect(0, 0, self.width(), self.height())

    @property
    def readImg(self):
        return self._readImg()

    def InitHelp(self):
        label = self.helpLabel
        font = QFont()
        font.setPointSize(64)
        fm = QFontMetrics(font)
        label.resize(self.width(), self.height())
        p = QPixmap(self.width(), self.height())
        p.fill(Qt.transparent)
        painter = QPainter(p)
        # painter.setFont(font)
        # painter.drawText(rect, text)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.setBrush(QBrush(QColor(218, 84, 124, 100)))
        painter.drawRect(QRect(0, self.height() // 2, self.width() // 3, self.height() // 2))
        painter.drawRect(QRect(self.width() // 3 * 2, self.height() // 2, self.width() // 3, self.height() // 2))

        painter.drawRect(QRect(self.width() // 3 * 1, 0, self.width() // 3, self.height() // 2))
        painter.drawRect(QRect(self.width() // 3 * 1, self.height() // 2, self.width() // 3, self.height() // 2))

        painter.setBrush(QBrush(QColor(51, 200, 255, 100)))
        painter.drawRect(QRect(0, 0, self.width()//4, self.height() // 2))
        painter.drawRect(QRect(0, 0, self.width()//3*4, self.height() // 2))

        painter.setFont(font)
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            nextPage = self.tr("上一页")
            lastPage = self.tr("下一页")
        else:
            lastPage = self.tr("上一页")
            nextPage = self.tr("下一页")
        painter.drawText(QRect(0, self.height() // 4 * 3, self.width() // 3, self.height() // 2), lastPage)
        painter.drawText(QRect(self.width() // 3 * 2, self.height() // 4 * 3, self.width() // 3, self.height() // 2),
                         nextPage)
        painter.drawText(QRect(0, self.height() // 4 * 1, self.width(), self.height()), self.tr("菜单"))
        painter.drawText(QRect(self.width()*2 // 3, self.height() // 4 * 1, self.width(), self.height()), self.tr("菜单"))

        if self.qtTool.stripModel in [ReadMode.UpDown, ReadMode.LeftRight]:
            painter.drawText(QRect(self.width() // 3, self.height() // 4 * 1, self.width(), self.height()), self.tr("上滑"))
            painter.drawText(QRect(self.width() // 3, self.height() // 4 * 3, self.width(), self.height()), self.tr("下滑"))
        self.helpPixMap = p
        label.setPixmap(p)
        label.setVisible(True)
        # p = QPixmap()
        # p.loadFromData(DataMgr().GetData("icon_picacg"))
        # label.setPixmap(p)
        return


    def eventFilter(self, obj, ev):
        # print(obj, ev)
        if obj == self.graphicsScene or obj == self.helpLabel:
            if ev.type() == QEvent.MouseButtonPress:
                if not self.helpLabel.isHidden():
                    self.helpLabel.hide()
                    return True
            elif ev.type() == QEvent.GraphicsSceneMousePress:
                if not self.helpLabel.isHidden():
                    self.helpLabel.hide()
                    return True
                # print(ev, ev.button())
                self.startPos = ev.screenPos()
                return False
            elif ev.type() == QEvent.KeyPress:
                if not self.helpLabel.isHidden():
                    self.helpLabel.hide()
                    return True
                if ev.key() == Qt.Key_Down:
                    from src.qt.read.qtreadimg import ReadMode
                    value = self.graphicsView.verticalScrollBar().value()
                    self.graphicsView.verticalScrollBar().setValue(value + 200)
                    self.UpdateScrollBar(self.graphicsView.verticalScrollBar().value(), -1)
                elif ev.key() == Qt.Key_Up:
                    value = self.graphicsView.verticalScrollBar().value()
                    self.graphicsView.verticalScrollBar().setValue(value - 200)
                    self.UpdateScrollBar(self.graphicsView.verticalScrollBar().value(), 1)
                elif ev.key() == Qt.Key_Left:
                    self.qtTool.LastPage()
                elif ev.key() == Qt.Key_Right:
                    self.qtTool.NextPage()
                return True
            elif ev.type() == QEvent.GraphicsSceneMouseRelease:
                # print(ev, self.width(), self.height(), self.readImg.pos())
                self.endPos = ev.screenPos()
                subPos = (self.endPos - self.startPos)
                if ev.button() == Qt.MouseButton.LeftButton:
                    if abs(subPos.x()) >= 50:
                        if subPos.x() < 0:
                            self.qtTool.NextPage()
                        elif subPos.y() > 0:
                            self.qtTool.LastPage()
                    elif abs(subPos.x()) <= 20:
                        curPos = self.endPos - self.readImg.pos()
                        if curPos.x() <= self.width() // 3:
                            if curPos.y() <= self.height() // 2:
                                self.readImg.ShowAndCloseTool()
                            else:
                                self.qtTool.LastPage()
                        elif curPos.x() <= self.width() // 3 * 2:
                            if curPos.y() <= self.height() // 2:
                                value = self.graphicsView.verticalScrollBar().value()

                                self.graphicsView.verticalScrollBar().setValue(value - self.height())
                                self.UpdateScrollBar(self.graphicsView.verticalScrollBar().value(), -1)
                            else:
                                value = self.graphicsView.verticalScrollBar().value()

                                self.graphicsView.verticalScrollBar().setValue(value + self.height())
                                self.UpdateScrollBar(self.graphicsView.verticalScrollBar().value(), 1)
                        else:
                            if curPos.y() <= self.height() //2:
                                self.readImg.ShowAndCloseTool()
                            else:
                                self.qtTool.NextPage()

        return super(self.__class__, self).eventFilter(obj, ev)

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScaleFrame()
        self.ScalePicture()

    def OnActionTriggered(self, action):
        if action != QAbstractSlider.SliderMove:
            return

        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.UpDown:
            value = self.graphicsView.verticalScrollBar().value()
        else:
            value = self.graphicsView.horizontalScrollBar().value()
        # print(value)

        self.UpdateScrollBar(value, value-self.oldValue)

    def UpdateScrollBar(self, value, add):
        self.UpdatePos(add)
        self.ResetScrollBar()
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.UpDown:
            self.oldValue = self.graphicsView.verticalScrollBar().value()
        else:
            self.oldValue = self.graphicsView.horizontalScrollBar().value()
        return True

    def ScaleFrame(self):
        size = self.size()
        w = size.width()
        h = size.height()
        self.graphicsView.setGeometry(0, 0, w, h)

        h2 = min(800, h)
        self.qtTool.setGeometry(w - 220, 0, 220, h2)

        # w = max((w - 150)//2, 0)
        # h = max((h - 150)//2, 0)
        self.process.setGeometry(w-150, h-150, 150, 150)
        self.waifu2xProcess.setGeometry(w-150, h-150, 150, 150)
        return

    def ScalePicture(self):
        self.graphicsView.setSceneRect(0, 0, self.width(), self.height())
        if not self.pixMapList:
            return
        self.ScaleGraphicsItem()

    def ResetScrollBar(self):
        width1 = self.graphicsItem1.pixmap().size().width()
        width2 = self.graphicsItem2.pixmap().size().width()
        height1 = self.graphicsItem1.pixmap().size().height()
        height2 = self.graphicsItem2.pixmap().size().height()
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.UpDown:
            self.graphicsView.verticalScrollBar().setMinimum(-100)
            self.graphicsView.verticalScrollBar().setMaximum(height1 + height2 + 100)
            self.graphicsView.verticalScrollBar().setSingleStep(60)
            self.graphicsView.verticalScrollBar().setPageStep(60)
            self.graphicsView.horizontalScrollBar().setMinimum(0)
            self.graphicsView.horizontalScrollBar().setMaximum(0)
        elif self.qtTool.stripModel == ReadMode.LeftRightScroll:
            self.graphicsView.horizontalScrollBar().setMinimum(-100)
            self.graphicsView.horizontalScrollBar().setMaximum(width1 + width2 + 100)
            self.graphicsView.horizontalScrollBar().setSingleStep(60)
            self.graphicsView.horizontalScrollBar().setPageStep(60)
            self.graphicsView.verticalScrollBar().setMinimum(0)
            self.graphicsView.verticalScrollBar().setMaximum(0)
        elif self.qtTool.stripModel == ReadMode.RightLeftScroll:
            self.graphicsView.horizontalScrollBar().setMinimum(-(width1 + width2 + 100))
            self.graphicsView.horizontalScrollBar().setMaximum(100)
            self.graphicsView.horizontalScrollBar().setSingleStep(60)
            self.graphicsView.horizontalScrollBar().setPageStep(60)
            self.graphicsView.verticalScrollBar().setMinimum(0)
            self.graphicsView.verticalScrollBar().setMaximum(0)
        else:
            self.graphicsView.verticalScrollBar().setMaximum(max(0, height1-self.height()))

    def MakePixItem(self, index):
        text = str(index+1)
        font = QFont()
        font.setPointSize(64)
        fm = QFontMetrics(font)

        p = QPixmap(self.width(), self.height())
        rect = QRect(self.width()//2-fm.width(text)//2, self.height()//2 - fm.height()//2, self.width()//2+fm.width(text)//2, self.height()//2+fm.height()//2)
        p.fill(Qt.transparent)
        painter = QPainter(p)
        painter.setFont(font)
        if config.ThemeText == "flatblack":
            painter.setPen(Qt.white)
        else:
            painter.setPen(Qt.black)
        painter.drawText(rect, text)
        return p

    def SetPixIem(self, index, data):

        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.LeftRight:
            if index > 0:
                self.pixMapList[index] = QPixmap()
                self.graphicsItemList[index].setPixmap(None)
            else:
                if not data and self.readImg.curIndex + index < self.readImg.maxPic:
                    data = self.MakePixItem(self.readImg.curIndex + index)
                    self.pixMapList[index] = data
                else:
                    self.pixMapList[index] = data

        elif self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.LeftRightDouble]:
            if index > 1:
                self.pixMapList[index] = QPixmap()
                self.graphicsItemList[index].setPixmap(None)
            else:
                if not data and self.readImg.curIndex+index < self.readImg.maxPic:
                    data = self.MakePixItem(self.readImg.curIndex+index)
                    self.pixMapList[index] = data
                else:
                    self.pixMapList[index] = data
        else:
            if not data and self.readImg.curIndex+index < self.readImg.maxPic:
                data = self.MakePixItem(self.readImg.curIndex+index)
                self.pixMapList[index] = data
            else:
                self.pixMapList[index] = data
        self.ScaleGraphicsItem()

    def ScaleGraphicsItem(self):
        from src.qt.read.qtreadimg import ReadMode
        if self.qtTool.stripModel == ReadMode.LeftRight:
            scale = (1 + self.scaleCnt * 0.1)
            wight = min(self.width(), self.width() * scale)
            height = self.height() * scale
            self.graphicsItem1.setPixmap(self.pixMapList[0].scaled(wight, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            height1 = self.graphicsItem1.pixmap().size().height()
            width1 = self.graphicsItem1.pixmap().size().width()
            width2 = self.graphicsItem2.pixmap().size().width()
            width3 = self.graphicsItem3.pixmap().size().width()
            height2 = self.graphicsItem2.pixmap().size().height()
            self.graphicsItem1.setPos((self.width()-width1)/2, max((self.height() - height1) // 2, 0))
        elif self.qtTool.stripModel in [ReadMode.RightLeftDouble, ReadMode.LeftRightDouble]:
            scale = (1 + self.scaleCnt * 0.1)
            self.graphicsItem1.setPixmap(
                self.pixMapList[0].scaled(min(self.width()//2, self.width()//2*scale), self.height()*scale,
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem2.setPixmap(
                self.pixMapList[1].scaled(min(self.width()//2, self.width()//2*scale), self.height()*scale,
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            height1 = self.graphicsItem1.pixmap().size().height()
            width1 = self.graphicsItem1.pixmap().size().width()
            width2 = self.graphicsItem2.pixmap().size().width()
            width3 = self.graphicsItem3.pixmap().size().width()
            height2 = self.graphicsItem2.pixmap().size().height()
            if self.qtTool.stripModel == ReadMode.LeftRightDouble:
                self.graphicsItem1.setPos((self.width()//2 - width1), max((self.height() - height1) // 2, 0))
                self.graphicsItem2.setPos(self.width()//2, max((self.height() - height2) // 2, 0))
            else:
                self.graphicsItem2.setPos((self.width()//2 - width1), max((self.height() - height1) // 2, 0))
                self.graphicsItem1.setPos(self.width()//2, max((self.height() - height2) // 2, 0))
        elif self.qtTool.stripModel in [ReadMode.LeftRightScroll]:
            scale = (1 + self.scaleCnt * 0.1)
            self.graphicsItem1.setPixmap(
                self.pixMapList[0].scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem2.setPixmap(
                self.pixMapList[1].scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem3.setPixmap(
                self.pixMapList[2].scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            height1 = self.graphicsItem1.pixmap().size().height()
            width1 = self.graphicsItem1.pixmap().size().width()
            width2 = self.graphicsItem2.pixmap().size().width()
            width3 = self.graphicsItem3.pixmap().size().width()
            height2 = self.graphicsItem2.pixmap().size().height()
            height3 = self.graphicsItem3.pixmap().size().height()
            self.graphicsItem1.setPos(0, (self.height()-height1)/2)
            self.graphicsItem2.setPos(width1, (self.height()-height2)/2)
            self.graphicsItem3.setPos(width1+width2, (self.height()-height3)/2)
        elif self.qtTool.stripModel in [ReadMode.RightLeftScroll]:
            scale = (1 + self.scaleCnt * 0.1)
            self.graphicsItem1.setPixmap(
                self.pixMapList[0].scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem2.setPixmap(
                self.pixMapList[1].scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem3.setPixmap(
                self.pixMapList[2].scaled(self.width() * scale*10, min(self.height(), self.height() * scale),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
            height1 = self.graphicsItem1.pixmap().size().height()
            width1 = self.graphicsItem1.pixmap().size().width()
            width2 = self.graphicsItem2.pixmap().size().width()
            width3 = self.graphicsItem3.pixmap().size().width()
            height2 = self.graphicsItem2.pixmap().size().height()
            height3 = self.graphicsItem3.pixmap().size().height()
            self.graphicsItem1.setPos(self.width()-width1, (self.height()-height1)/2)
            self.graphicsItem2.setPos(self.width()-width1-width1, (self.height()-height2)/2)
            self.graphicsItem3.setPos(self.width()-width1-width1-width2, (self.height()-height3)/2)
        elif self.qtTool.stripModel in [ReadMode.UpDown]:
            scale = (0.5 + self.scaleCnt * 0.1)
            minWidth = min(self.width(), self.width() * scale)
            minHeight = self.height() * scale * 10

            self.graphicsItem1.setPixmap(
                self.pixMapList[0].scaled(minWidth, minHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem2.setPixmap(
                self.pixMapList[1].scaled(minWidth, minHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.graphicsItem3.setPixmap(
                self.pixMapList[2].scaled(minWidth, minHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            height1 = self.graphicsItem1.pixmap().size().height()
            width1 = self.graphicsItem1.pixmap().size().width()
            width2 = self.graphicsItem2.pixmap().size().width()
            width3 = self.graphicsItem3.pixmap().size().width()
            height2 = self.graphicsItem2.pixmap().size().height()
            self.graphicsItem1.setPos((self.width()-width1)/2, 0)
            self.graphicsItem2.setPos((self.width()-width2)/2, 0+height1)
            self.graphicsItem3.setPos((self.width()-width3)/2, 0+height1 + height2)
        self.ResetScrollBar()

    def UpdateProcessBar(self, info):
        if info:
            self.downloadSize = info.downloadSize
            self.downloadMaxSize = max(1, info.size)
            value = int((self.downloadSize / self.downloadMaxSize) * 100)
            # print(value)
            self.process.setValue(value)
        else:
            self.downloadSize = 0
            self.downloadMaxSize = 1
            self.process.setValue(0)

    def InitPixMap(self):
        pixMap1 = QPixmap()
        pixMap2 = QPixmap()
        pixMap3 = QPixmap()
        self.pixMapList = []
        self.pixMapList.append(pixMap1)
        self.pixMapList.append(pixMap2)
        self.pixMapList.append(pixMap3)
        self.graphicsGroup.setPos(0, 0)

    def UpdatePixMap(self):
        if not self.pixMapList:
            return
        self.ScaleGraphicsItem()
        return

    def UpdatePos(self, value):

        from src.qt.read.qtreadimg import ReadMode
        # scale = (1+self.scaleCnt*0.1)
        if self.qtTool.stripModel == ReadMode.UpDown:
            height = self.graphicsItem1.pixmap().size().height()
            scroll = self.graphicsView.verticalScrollBar()
        elif self.qtTool.stripModel in [ReadMode.LeftRightScroll, ReadMode.RightLeftScroll]:
            height = self.graphicsItem1.pixmap().size().width()
            scroll = self.graphicsView.horizontalScrollBar()
        else:
            return

        if self.qtTool.stripModel in [ReadMode.UpDown, ReadMode.LeftRightScroll]:
            if value > 0 and self.oldValue != 0 and self.readImg.curIndex >= self.readImg.maxPic - 1:
                QtMsgLabel().ShowMsgEx(self.readImg, self.tr("已经到最后一页"))
                return

            ## 切换上一图片
            if value < 0 and scroll.value() < 0:
                if self.readImg.curIndex <= 0:
                    return
                self.readImg.curIndex -= 1
                subValue = scroll.value()
                self.readImg.ShowImg()
                self.readImg.ShowOtherPage()
                if self.qtTool.stripModel == ReadMode.UpDown:
                    height = self.graphicsItem1.pixmap().size().height()
                else:
                    height = self.graphicsItem1.pixmap().size().width()
                subValue += height
                scroll.setValue(subValue)

                pass

            ## 切换下一图片
            elif value > 0 and scroll.value() >= height:
                if self.readImg.curIndex >= self.readImg.maxPic - 1:
                    return
                if self.qtTool.stripModel == ReadMode.RightLeftDouble:
                    self.readImg.curIndex += 2
                    self.readImg.curIndex = min(self.readImg.curIndex, self.readImg.maxPic)
                else:
                    self.readImg.curIndex += 1
                subValue = scroll.value() - height
                self.readImg.ShowImg()
                self.readImg.ShowOtherPage()
                # print(subValue)
                scroll.setValue(subValue)

        else:
            if value <= 0 and self.readImg.curIndex >= self.readImg.maxPic - 1:
                QtMsgLabel().ShowMsgEx(self.readImg, self.tr("已经到最后一页"))
                return

            ## 切换上一图片
            if value > 0 and scroll.value() > 0:
                if self.readImg.curIndex <= 0:
                    return
                self.readImg.curIndex -= 1
                subValue = scroll.value() - height
                self.readImg.ShowImg()
                self.readImg.ShowOtherPage()
                # print(subValue)
                scroll.setValue(subValue)

                pass

            ## 切换下一图片
            elif value < 0 and scroll.value() < -height:
                if self.readImg.curIndex >= self.readImg.maxPic - 1:
                    return
                self.readImg.curIndex += 1
                subValue = scroll.value()
                self.readImg.ShowImg()
                self.readImg.ShowOtherPage()
                height = self.graphicsItem1.pixmap().size().width()
                subValue += height
                scroll.setValue(subValue)
