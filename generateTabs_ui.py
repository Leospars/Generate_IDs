# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabGroup.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow
from tests.SpecialComboBox import TtfComboBox, FontSizeComboBox

from generateTabs import get_data_from_canvas
from tests.canvas import Canvas

# helper function to translate texts in the window
_translate = QtCore.QCoreApplication.translate


def generateTabs(parent: QtWidgets):
    self = parent
    vlayout = QtWidgets.QVBoxLayout(self)
    vlayout.setObjectName("verticalLayout")
    tool_box = QtWidgets.QToolBox()
    tool_box.setObjectName("toolBox")

    # get canvas data for generating frames
    canvas = self.canvas = Canvas(self)
    canvas.addTextBoxContent(
        rects=[QRect(0, 0, 100, 50), QRect(210, 30, 150, 40)],
        rectIDs=["TextBox1", "TextBox2"],
        rectFonts=[QFont("Lucida Console", 60), QFont("Arial", 12)],
    )
    canvas_data = get_data_from_canvas(canvas)

    # create a page for each field in the toolbox
    for box in canvas_data:
        field_name = box.label_name

        # create a page for each field in the toolbox
        page = QtWidgets.QWidget(tool_box)
        page.setObjectName(field_name + '_page')
        page.setGeometry(0, 0, 730, 232)

        # initialize font combobox
        ttf_combo_box = TtfComboBox(page)
        ttf_combo_box.setGeometry(QtCore.QRect(0, 0, 226, 22))
        ttf_combo_box.setObjectName(field_name + '_ttfBox')

        # initialize font size combobox
        font_size_combo_box = FontSizeComboBox(page)
        font_size_combo_box.setGeometry(QtCore.QRect(246, 0, 226, 22))
        font_size_combo_box.setObjectName(field_name + '_fontSizeBox')

        # initialize text box
        text_box = QtWidgets.QPlainTextEdit(page)
        text_box.setGeometry(QtCore.QRect(0, 30, 800, 80))
        text_box.setObjectName(field_name + '_data')
        text_box.setPlaceholderText(_translate("MainWindow", "Enter comma seperated values here . . .\n"))

        # add the combo boxes to the page
        tool_box.addItem(page, _translate("MainWindow", field_name))
        vlayout.addWidget(tool_box)  # Add the toolbox to the vlayout in the window

    tool_box.show()
    self.statusbar = QtWidgets.QStatusBar(parent)
    self.statusbar.setObjectName("statusbar")
    self.setStatusBar(self.statusbar)

    self.setLayout(vlayout)
    QtCore.QMetaObject.connectSlotsByName(parent)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle(_translate("MainWindow", "Generated Tabs"))
        self.resize(768, 411)
        generateTabs(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    generateTabs(ui)
    ui.show()
    sys.exit(app.exec_())
