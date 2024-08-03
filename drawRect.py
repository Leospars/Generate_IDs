from PyQt5.QtGui import QPainter, QPen, QPixmap, QFont
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Draw Rectangle")
        self.setMouseTracking(True)
        self.vBoxLayout = QVBoxLayout()
        self.canvas = Canvas(self)
        self.canvas.setGeometry(0, 0, 600, 400)
        self.vBoxLayout.addWidget(self.canvas)
        self.show()

class Canvas(QLabel) :
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.paintID = "TextBox1"
        self.setMouseTracking(True)
        self.setGeometry(0, 0, 800, 600)
        self.rects = [QRect(0, 0, 200, 200)]
        self.rectIDs = ["TextBox1"]
        self.rectFonts = [QFont("Arial", 12)]
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        for rect, _id in zip(self.rects, self.rectIDs):
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter, _id)

    def mousePressEvent(self, event):
        pos = event.pos()
        print(f"{pos.x(), pos.y()}")
        self.rects.append(QRect(pos.x(), pos.y(), 200, 200))
        self.rectIDs.append(f"TextBox{len(self.rects)}")
        self.paintEvent(event)
        self.update()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()