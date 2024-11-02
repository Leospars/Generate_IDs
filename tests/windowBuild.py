from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QPixmap, QFont, QWindow
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QLineEdit, QApplication, QDialog, QGridLayout

from tests.canvas import Canvas


def center_rect(width, height):
    # Get device screen size
    screen_geo = QApplication.desktop().geometry()
    print(screen_geo)
    x = (screen_geo.width() - width) // 2
    y = (screen_geo.height() - height) // 2
    return QRect(x, y, width, height)

def canvasBuild(self):
    self.vBoxLayout = QVBoxLayout()
    canvas_geometry = QRect(0, 0, 800, 800)
    self.label = QLabel(self)
    self.label.setGeometry(canvas_geometry)
    self.label.setPixmap(QPixmap("./img/MGI_Blank Lvl1.png"))
    self.label.setScaledContents(True)

    self.canvas = Canvas(self)
    self.canvas.setGeometry(canvas_geometry)
    self.clearButton = QPushButton("Clear", self)
    self.clearButton.clicked.connect(self.canvas.clearCanvas)

    self.drawOnCanvas()
    self.vBoxLayout.addWidget(self.label)
    self.vBoxLayout.addWidget(self.canvas)

    self.gridLayout = QGridLayout()
    self.vBoxLayout.addLayout(self.gridLayout)
    self.label_width = QLabel(self)
    self.label_width.setMaximumSize(QSize(400, 100))
    self.label_width.setObjectName("label_width")
    self.gridLayout.addWidget(self.label_width, 4, 1, 1, 1)

    self.txtBoxW = QLineEdit(self)
    self.txtBoxW.setText("")
    self.txtBoxW.setObjectName("txtBoxW")
    self.gridLayout.addWidget(self.txtBoxW, 2, 1, 1, 1)

    self.label_4 = QLabel(self)
    self.label_4.setObjectName("label_4")
    self.gridLayout.addWidget(self.label_4, 4, 3, 1, 1)

    self.show()

    class Window(QDialog):
        def __init__(self):
            super(Window, self).__init__()
            self.setGeometry(self.__center_rect__(1000, 800))
            self.setWindowTitle("Place TextBox")
            self.setModal(True)
            self.setMouseTracking(True)
            canvasBuild(self)

        def drawOnCanvas(self):
            self.canvas.addTextBoxContext(
                rects=[QRect(100, 100, 200, 200), QRect(300, 300, 200, 200)],
                rectIDs=["TextBox1", "TextBox2"],
                rectFonts=[QFont("Arial", 12), QFont("Arial", 12)]
            )
            self.canvas.mousePressEvent = lambda event: self.canvas.addTextBoxOnClick(event)


if __name__ == '__main__':
    app = QApplication([])
    window = QWindow()
    window.show()
    app.exec()