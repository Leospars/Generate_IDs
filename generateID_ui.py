# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\generateID.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(856, 634)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBoxIcon = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBoxIcon.sizePolicy().hasHeightForWidth())
        self.textBoxIcon.setSizePolicy(sizePolicy)
        self.textBoxIcon.setMinimumSize(QtCore.QSize(100, 20))
        self.textBoxIcon.setMaximumSize(QtCore.QSize(150, 100))
        self.textBoxIcon.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.textBoxIcon.setMouseTracking(True)
        self.textBoxIcon.setAutoFillBackground(False)
        self.textBoxIcon.setStyleSheet("margin: auto 0;\n"
"text-align: center;\n"
"height: auto;\n"
"border: 1px solid grey;\n"
"background-color: white")
        self.textBoxIcon.setTextFormat(QtCore.Qt.AutoText)
        self.textBoxIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.textBoxIcon.setObjectName("textBoxIcon")
        self.horizontalLayout.addWidget(self.textBoxIcon)
        self.template_img = QtWidgets.QLabel(self.centralwidget)
        self.template_img.setMinimumSize(QtCore.QSize(3, 0))
        self.template_img.setMouseTracking(True)
        self.template_img.setText("")
        self.template_img.setPixmap(QtGui.QPixmap(".\\MGI_Blank Lvl1.png"))
        self.template_img.setScaledContents(True)
        self.template_img.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.template_img.setObjectName("template_img")
        self.horizontalLayout.addWidget(self.template_img)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setObjectName("uploadButton")
        self.verticalLayout_main.addWidget(self.uploadButton)
        self.generateIDButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateIDButton.setObjectName("generateIDButton")
        self.verticalLayout_main.addWidget(self.generateIDButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ID Genrator"))
        self.textBoxIcon.setText(_translate("MainWindow", "Text Box"))
        self.uploadButton.setText(_translate("MainWindow", "Upload Image"))
        self.generateIDButton.setText(_translate("MainWindow", "Generate IDs"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
