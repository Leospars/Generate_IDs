''' Create GUI for generate_IDs.py to allow users to
    - Select a template
    - Select a folder to save the certificates
    - Select the font size
    - Position the text box and alignment of the text
    - Generate certificates
'''

import PyQt5.QtWidgets as Qtw
from tests.canvas import Canvas
from generateID_ui import Ui_MainWindow
from PyQt5.QtCore import Qt, QMimeData, QRect, QSize, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QFont, QPainter
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel, QMainWindow

# from PyQt5.uic import loadUi

textBoxNum = 0
click_flag = 0


def increment_click():
    global click_flag
    click_flag += 1

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # loadUi('generateID.ui', self)
        self.setupUi(self)
        self.addWidgets()
        self.setEventHandlers()

    def addWidgets(self):
        print("tempate image parent: ", self.template_img.parent())
        self.canvas = Canvas(self.template_img.parent())
        self.canvas.setGeometry(self.template_img.geometry())
        self.canvas.draw = lambda: self.addPaint(self.canvas)

    def setEventHandlers(self):
        self.uploadButton.clicked.connect(self.uploadImage)
        self.generateIDButton.clicked.connect(self.generateID)
        self.mousePressEvent = lambda e: increment_click()
        self.addTextBoxButton.clicked.connect(self.addTextBox)
        self.clearIDButton.clicked.connect(self.canvas.clearCanvas)
        self.txtBox = Canvas(self)

    def uploadImage(self):
        template_filename, _ = QFileDialog.getOpenFileName(self, "Open Template File", "",
                                                           "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")
        if template_filename:
            self.template_img.setPixmap(QPixmap(template_filename))
            print(template_filename)

    def addPaint(self, canvas):
        painter = canvas.painter
        # tint background
        painter.setBrush(Qt.green)
        painter.setOpacity(0.2)
        painter.drawRect(canvas.geometry())
        print("Canvas rect:", canvas.rect(), "Canvas geometry:", canvas.geometry(),
              "Template img rect:", self.template_img.rect(), "Template img geometry:", self.template_img.geometry())

    def generateID(self):
        print("Generate ID")

    def addTextBox(self):
        # Change template image cursor
        self.canvas.setCursor(Qt.CrossCursor)
        self.canvas.mousePressEvent = lambda event: self.createTextBoxOnClick(event)
        print("Add Textbox")

    def createTextBoxOnClick(self, event):
        # get values from user input
        width = self.txtBoxW.text() if self.txtBoxW.text() else self.txtBoxW.placeholderText()
        height = self.txtBoxH.text() if self.txtBoxH.text() else self.txtBoxH.placeholderText()
        width = int(width)
        height = int(height)
        font = self.fontComboBox.currentFont()  # get font from combobox

        #increment textBoxID
        _id = self.idTypeName.text() if self.idTypeName.text() else self.idTypeName.placeholderText()
        if _id in self.canvas.rectIDs:
            _id += "_" + str(len(self.canvas.rectIDs))

        self.canvas.addTextBoxContext(
            rects=[QRect(event.pos().x(), event.pos().y(), width, height)],
            rectIDs=[_id],
            rectFonts=[font]
        )
        self.canvas.mousePressEvent = lambda ev: None
        print(f"TextBox{textBoxNum} added at {event.pos().x(), event.pos().y()} with size {width}x{height}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()