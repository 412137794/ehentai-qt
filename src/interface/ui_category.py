# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_category.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from component.list.category_list_widget import CategoryListWidget


class Ui_Category(object):
    def setupUi(self, Category):
        if not Category.objectName():
            Category.setObjectName(u"Category")
        Category.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Category)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bookList = CategoryListWidget(Category)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout.addWidget(self.bookList)


        self.retranslateUi(Category)

        QMetaObject.connectSlotsByName(Category)
    # setupUi

    def retranslateUi(self, Category):
        Category.setWindowTitle(QCoreApplication.translate("Category", u"\u5206\u7c7b", None))
    # retranslateUi

