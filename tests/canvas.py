from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QLabel

class Canvas(QLabel):
	def __init__(self, parent=None):
		super(Canvas, self).__init__(parent)
		self.setMouseTracking(True)
		self.rects = []
		self.rectLabels = []
		self.rectFonts = []
		self.show()
		self.painter = QPainter()

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

	def addTextBox(self, rect: QRect(), _id: str, font=QFont("Arial", 12)):
		self.rects.append(rect)
		self.rectLabels.append(_id)
		self.rectFonts.append(font)
		self.update()

	def addTextBoxContent(self, rects, rectIDs, rectFonts):
		self.rects.extend(rects)
		self.rectLabels.extend(rectIDs)
		self.rectFonts.extend(rectFonts)
		self.update()

	def clearCanvas(self):
		self.rects.clear()
		self.rectLabels.clear()
		self.rectFonts.clear()
		self.update()