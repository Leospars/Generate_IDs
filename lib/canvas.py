from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QLabel, QApplication


def center_rect(width, height):
    # Get device screen size
    screen_geo = QApplication.desktop().geometry()
    print(screen_geo)
    x = (screen_geo.width() - width) // 2
    y = (screen_geo.height() - height) // 2
    return QRect(x, y, width, height)


class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.rects = []
        self.rectLabels: list[str] = []
        self.rectFonts: list[QFont] = []
        self.painter = QPainter()
        self.show()

    def paintEvent(self, event):
        painter = self.painter
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for rect, label, font in zip(self.rects, self.rectLabels, self.rectFonts):
            painter.drawRect(rect)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, label)
        self.draw()
        painter.end()

    def draw(self):
        self.painter.drawRect(self.geometry())  # add border around canvas
        pass

    def addTextBox(self, rect: QRect, _id: str, font: QFont = QFont("Arial", 12)):
        self.rects.append(rect)
        self.rectLabels.append(_id)
        self.rectFonts.append(font)
        self.update()

    def addTextBoxContent(self, rects: list[QRect], rect_ids: list[str], rect_fonts: list[QFont]):
        self.rects.extend(rects)
        self.rectLabels.extend(rect_ids)
        self.rectFonts.extend(rect_fonts)
        self.update()

    def clearCanvas(self):
        self.rects.clear()
        self.rectLabels.clear()
        self.rectFonts.clear()
        self.update()
