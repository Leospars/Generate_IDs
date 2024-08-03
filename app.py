''' Create GUI for auto_cert.py to allow users to
    - Select a template
    - Select a folder to save the certificates
    - Select the font size
    - Position the text box and alignment of the text
    - Generate certificates
'''

import PyQt5.QtWidgets as Qtw
from PyQt5.QtCore import Qt, QMimeData, QRect, QSize, QPoint
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel
from PyQt5.uic import loadUi


class MainWindow(Qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('generateID.ui', self)
        self.uploadButton.clicked.connect(self.uploadImage)
        # Allow the text box icon to create a draggable textbox to overlay on the template image
        # self.setAcceptDrops(True)
        self.template_img.setAcceptDrops(True)  # Allows item to drag and drop onto the image
        self.template_img.dragEnterEvent = lambda e: e.accept()
        self.textBoxIcon = DragLabel(self.textBoxIcon)
        self.generateIDButton.clicked.connect(self.generateID)

    def uploadImage(self):
        template_filename, _ = QFileDialog.getOpenFileName(self, "Open Template File", "",
                                                           "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")
        if template_filename:
            self.template_img.setPixmap(QPixmap(template_filename))
            print(template_filename)

    def generateID(self):
        print("Generate ID")


class DragLabel(QLabel):
    def __init__(self, parent=None):
        super(DragLabel, self).__init__(parent)
        self.dragStartPos = QPoint()
        self.dropAction = None


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            # set an image when dragging and dropping
            icon_pixmap = QPixmap(self.size())
            print(f"label size: {self.size}")
            self.render(icon_pixmap)
            drag.setPixmap(icon_pixmap)

            self.setCursor(Qt.ClosedHandCursor)
            self.dragStartPos = event.pos()

            self.dropAction = drag.exec(Qt.MoveAction)

    def dropEvent(self, event) :
        self.setCursor(Qt.OpenHandCursor)
        event.accept()
        if self.dropAction == Qt.MoveAction:
            textBox = ResizeableLabel(self.parent())
            self.move(event.pos() - self.dragStartPos)


class ResizeableLabel (QLabel):
    def __init__(self, parent=None):
        super(ResizeableLabel, self).__init__(parent)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton and
                self.geometry().contains(event.pos())):
            self.dragStartPos = event.pos()

    def resizeEvent(self, event):
        self.setPixmap(self.pixmap().scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def setPixmap(self, pixmap):
        super(ResizeableLabel, self).setPixmap(pixmap)
        self.setMinimumSize(1, 1)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()