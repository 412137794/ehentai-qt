import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices

from conf import config
from ui.about import Ui_AboutForm


class QtAbout(QtWidgets.QWidget, Ui_AboutForm):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_AboutForm.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("关于")
        self.owner = weakref.ref(owner)
        self.label.setText("E-hentai漫画{}".format(config.UpdateVersion))
        self.label_3.linkActivated.connect(self.OpenUrl)

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.UpdateUrl))
