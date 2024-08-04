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
from PyQt5.uic import loadUi

textBoxNum = 0

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # loadUi('generateID.ui', self)
        self.setupUi(self)
        self.addWidgets()
        self.setEventHandlers()

    def addWidgets(self):
        self.template_overlay = Canvas(self.template_img)
        self.template_overlay.setGeometry(self.template_img.geometry())
        self.template_overlay.draw = lambda: self.addPaint(self.template_overlay)
        self.horizontalLayout.addWidget(self.template_overlay)

    def addPaint(self, canvas):
        painter = canvas.painter
        # tint background
        painter.setBrush(Qt.black)
        painter.setOpacity(0.5)
        painter.drawRect(canvas.rect())
        painter.setBrush(Qt.blue)
        painter.setOpacity(0.3)
        painter.drawRect(canvas.geometry())
        print("Canvas rect:", canvas.rect(), "Canvas geometry:", canvas.geometry(),
              "Template img rect:", self.template_img.rect(), "Template img geometry:", self.template_img.geometry())

    def setEventHandlers(self):
        self.uploadButton.clicked.connect(self.uploadImage)
        self.generateIDButton.clicked.connect(self.generateID)
        self.addTextBoxButton.clicked.connect(self.addTextBox)

        self.txtBox = Canvas(self)

    def uploadImage(self):
        template_filename, _ = QFileDialog.getOpenFileName(self, "Open Template File", "",
                                                           "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")
        if template_filename:
            self.template_img.setPixmap(QPixmap(template_filename))
            print(template_filename)

    def generateID(self):
        print("Generate ID")

    def addTextBox(self):
        # Change template image cursor
        self.template_img.setCursor(Qt.CrossCursor)
        self.template_overlay.mousePressEvent = lambda event: self.createTextBoxOnClick(event)
        print("Add Teox")

    def createTextBoxOnClick(self, event):
        # get values from user input
        print(f"Width: {self.txtBoxW.placeholderText()}, Height: {self.txtBoxH.text()}")
        width = self.txtBoxW.text() | self.txtBoxW.placeholderText()
        height = self.txtBoxH.text() | self.txtBoxH.placeholderText()
        width = int(width)
        height = int(height)
        font = self.fontComboBox.currentFont()  # get font from combobox

        #increment textBoxID
        global textBoxNum
        textBoxNum += 1

        self.template_overlay.addTextBoxContext(
            rects=[QRect(event.pos().x(), event.pos().y(), width, height)],
            rectIDs=[f"TextBox{textBoxNum}"],
            rectFonts=[font]
        )
        print(f"TextBox{textBoxNum} added at {event.pos().x(), event.pos().y()} with size {width}x{height}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()