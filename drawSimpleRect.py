# Draw a rectangle in a label

from PyQt5.QtGui import QPainter, QPen, QPixmap, QFont
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Draw Rectangle")
        self.setMouseTracking(True)
        self.vBoxLayout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 600, 400)
        self.label.setText("Hello")
        self.label.setPixmap(QPixmap("./MGI_Blank Lvl1.png"))
        self.label.setScaledContents(True)
        self.canvas = Canvas(self)
        self.canvas.setGeometry(0, 0, 600, 400)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.canvas)
        self.show()

class Canvas(QLabel) :
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setGeometry(0, 0, 800, 600)
        self.rect = QRect(0, 0, 500, 200)
        self.show()

    def paintEvent(self, a0):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawRect(self.rect)
        painter.end()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()