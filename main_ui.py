# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from SpecialComboBox import FontSizeComboBox, TtfComboBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1208, 806)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Tab = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tab.sizePolicy().hasHeightForWidth())
        self.Tab.setSizePolicy(sizePolicy)
        self.Tab.setUsesScrollButtons(True)
        self.Tab.setObjectName("Tab")
        self.setupTab = QtWidgets.QWidget()
        self.setupTab.setMaximumSize(QtCore.QSize(1125, 715))
        self.setupTab.setObjectName("setupTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.setupTab)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.clearIDButton = QtWidgets.QPushButton(self.setupTab)
        self.clearIDButton.setObjectName("clearIDButton")
        self.verticalLayout_6.addWidget(self.clearIDButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.addTextBoxButton = QtWidgets.QPushButton(self.setupTab)
        self.addTextBoxButton.setObjectName("addTextBoxButton")
        self.verticalLayout_6.addWidget(self.addTextBoxButton)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.setupTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.idTypeName = QtWidgets.QLineEdit(self.setupTab)
        self.idTypeName.setText("")
        self.idTypeName.setObjectName("idTypeName")
        self.gridLayout_3.addWidget(self.idTypeName, 1, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.fontComboBox = TtfComboBox(self.setupTab)
        self.fontComboBox.setObjectName("fontComboBox")
        self.gridLayout_2.addWidget(self.fontComboBox, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.setupTab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.fontSizeComboBox = FontSizeComboBox(self.setupTab)
        self.fontSizeComboBox.setEditable(True)
        self.fontSizeComboBox.setMaxVisibleItems(12)
        self.fontSizeComboBox.setObjectName("fontSizeComboBox")
        self.gridLayout_2.addWidget(self.fontSizeComboBox, 1, 2, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setObjectName("gridLayout")
        self.txtBoxH = QtWidgets.QLineEdit(self.setupTab)
        self.txtBoxH.setText("")
        self.txtBoxH.setObjectName("txtBoxH")
        self.gridLayout.addWidget(self.txtBoxH, 2, 3, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout.addLayout(self.verticalLayout_5, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.setupTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMaximumSize(QtCore.QSize(400, 100))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)
        self.txtBoxW = QtWidgets.QLineEdit(self.setupTab)
        self.txtBoxW.setText("")
        self.txtBoxW.setObjectName("txtBoxW")
        self.gridLayout.addWidget(self.txtBoxW, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.setupTab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 3, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, 20, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.setupTab)
        self.frame.setMinimumSize(QtCore.QSize(800, 0))
        self.frame.setObjectName("frame")
        self.template_img = QtWidgets.QLabel(self.frame)
        self.template_img.setEnabled(True)
        self.template_img.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.template_img.setMaximumSize(QtCore.QSize(800, 600))
        self.template_img.setText("")
        self.template_img.setPixmap(QtGui.QPixmap("img/no-image.png"))
        self.template_img.setScaledContents(True)
        self.template_img.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.template_img.setObjectName("template_img")
        self.canvas = QtWidgets.QLabel(self.frame)
        self.canvas.setGeometry(QtCore.QRect(240, 0, 941, 621))
        self.canvas.setMouseTracking(False)
        self.canvas.setText("")
        self.canvas.setObjectName("canvas")
        self.verticalLayout_2.addWidget(self.frame)
        self.uploadButton = QtWidgets.QPushButton(self.setupTab)
        self.uploadButton.setObjectName("uploadButton")
        self.verticalLayout_2.addWidget(self.uploadButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.generateIDButton = QtWidgets.QPushButton(self.setupTab)
        self.generateIDButton.setObjectName("generateIDButton")
        self.verticalLayout.addWidget(self.generateIDButton)
        self.Tab.addTab(self.setupTab, "")
        self.dataTab = QtWidgets.QWidget()
        self.dataTab.setObjectName("dataTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dataTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tool_box = QtWidgets.QToolBox(self.dataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_box.sizePolicy().hasHeightForWidth())
        self.tool_box.setSizePolicy(sizePolicy)
        self.tool_box.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tool_box.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tool_box.setObjectName("tool_box")
        self.idField_1 = QtWidgets.QWidget()
        self.idField_1.setGeometry(QtCore.QRect(0, 0, 1158, 677))
        self.idField_1.setObjectName("idField_1")
        self.textBox2_Data = QtWidgets.QPlainTextEdit(self.idField_1)
        self.textBox2_Data.setGeometry(QtCore.QRect(0, 30, 800, 80))
        self.textBox2_Data.setObjectName("textBox2_Data")
        self.idTtfComboBox_2 = TtfComboBox(self.idField_1)
        self.idTtfComboBox_2.setGeometry(QtCore.QRect(0, 0, 226, 22))
        self.idTtfComboBox_2.setObjectName("idTtfComboBox_2")
        self.comboBox = FontSizeComboBox(self.idField_1)
        self.comboBox.setGeometry(QtCore.QRect(240, 0, 73, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setMaxVisibleItems(12)
        self.comboBox.setObjectName("comboBox")
        self.tool_box.addItem(self.idField_1, "")
        self.verticalLayout_4.addWidget(self.tool_box)
        self.Tab.addTab(self.dataTab, "")
        self.verticalLayout_3.addWidget(self.Tab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.Tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ID Genrator"))
        self.clearIDButton.setText(_translate("MainWindow", "Clear IDs"))
        self.addTextBoxButton.setText(_translate("MainWindow", "Add Field"))
        self.label_2.setText(_translate("MainWindow", "Field"))
        self.idTypeName.setPlaceholderText(_translate("MainWindow", "First_Name"))
        self.label.setText(_translate("MainWindow", "Font"))
        self.fontSizeComboBox.setCurrentText(_translate("MainWindow", "12"))
        self.txtBoxH.setPlaceholderText(_translate("MainWindow", "30"))
        self.label_3.setText(_translate("MainWindow", "Width"))
        self.txtBoxW.setPlaceholderText(_translate("MainWindow", "150"))
        self.label_4.setText(_translate("MainWindow", "Height"))
        self.uploadButton.setText(_translate("MainWindow", "Upload Image"))
        self.generateIDButton.setText(_translate("MainWindow", "Generate IDs"))
        self.Tab.setTabText(self.Tab.indexOf(self.setupTab), _translate("MainWindow", "Setup"))
        self.comboBox.setCurrentText(_translate("MainWindow", "12"))
        self.tool_box.setItemText(self.tool_box.indexOf(self.idField_1), _translate("MainWindow", "ID_Field"))
        self.Tab.setTabText(self.Tab.indexOf(self.dataTab), _translate("MainWindow", "Data"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
