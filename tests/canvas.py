from PyQt5.QtGui import QPainter, QPen, QPixmap, QFont, QWindow
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QDialog, QLineEdit

class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.rects = []
        self.rectIDs = []
        self.rectFonts = []
        self.show()
        self.painter = QPainter()

    def paintEvent(self, event):
        painter = self.painter
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        for rect, _id, font in zip(self.rects, self.rectIDs, self.rectFonts):
            painter.drawRect(rect)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, _id)
        self.draw()
        painter.end()

    def draw(self):
        self.painter.drawRect(self.geometry())
        pass

    def addTextBoxOnClick(self, event, width=200, height=200, _id=str("TextBox"), font=QFont("Arial", 12)):
        pos = event.pos()
        print(f"{pos.x(), pos.y()}")
        self.rects.append(QRect(pos.x(), pos.y(), width, height))
        self.rectIDs.append(_id)
        self.rectFonts.append(font)
        self.update()

    def addTextBoxContext(self, rects, rectIDs, rectFonts):
        self.rects.extend(rects)
        self.rectIDs.extend(rectIDs)
        self.rectFonts.extend(rectFonts)
        self.update()

    def clearCanvas(self):
        self.rects.clear()
        self.rectIDs.clear()
        self.rectFonts.clear()
        self.update()
        self.paintEvent(None)