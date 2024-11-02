import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel


class PixmapWidget(QLabel):
    def __init__(self, pixmap_path, parent=None):
        super().__init__(parent)
        # check if pixmap_path is a valid path
        if not os.path.exists(pixmap_path):
            raise FileNotFoundError("File not found")

        self.pixmap = QPixmap(pixmap_path)
        # self.pixmap = self.pixmap.scaled(scaled, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)
        self.resize(400, 300)
        print("pixmap size: ", self.pixmap.size(), "widget size: ", self.size())
        self.scaled_pixmap = self.pixmap

    def resizeEvent(self, event):
        self.scaled_pixmap = self.pixmap.scaled(800, 600, Qt.KeepAspectRatio)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.scaled_pixmap)


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    window.resize(800, 600)
    centralWidget = QWidget()
    centralWidget.resize(800, 600)
    v_layout = QVBoxLayout(centralWidget)
    pixmap_widget = PixmapWidget('../img/MGI_Blank Lvl1.png', centralWidget)
    v_layout.addWidget(pixmap_widget)
    window.setCentralWidget(centralWidget)
    window.show()
    app.exec()
