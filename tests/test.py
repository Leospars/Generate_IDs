from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        widget1 = QLabel("Widget 1", central_widget)
        widget1.setPixmap(QPixmap("..\img\MGI_Blank Lvl1.png"))
        widget1.setScaledContents(True)
        widget1.setStyleSheet("background-color: red;")
        widget1.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        widget1.setGeometry(0, 0, 800, 600)

        widget2 = QLabel("Widget 2", central_widget)

        def paint(event, widget):
            painter = QPainter(widget)
            painter.setBrush(Qt.green)
            painter.setOpacity(0.3)

        widget2.paintEvent = lambda event: paint(event, widget2)

        widget2.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        widget2.setGeometry(0, 0, 800, 600)

        self.setGeometry(400, 400, 400, 300)
        self.setWindowTitle('Align Widgets Example')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
