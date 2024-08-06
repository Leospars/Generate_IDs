import PyQt5.QtWidgets as Qtw
from PyQt5.QtGui import QFont

from tests.GetFonts import GetFonts

class TtfComboBox(Qtw.QFontComboBox):
	def __init__(self, parent: Qtw.QWidget | None = None):
		super().__init__(parent)
		self.clear()
		font_dirmap = GetFonts.get_font_dirmap()
		self.addItems(font_dirmap.keys())
		self.setCurrentFont(QFont("Arial", 12))

class FontSizeComboBox(Qtw.QComboBox):
	def __init__(self, parent: Qtw.QWidget | None = None):
		super().__init__()
		self.clear()
		self.setParent(parent)
		for i in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 32, 36, 48, 72]:
			self.addItem(str(i))
		self.setCurrentText("12")
		self.resize(54, 22)

if __name__ == "__main__":
	import sys

	app = Qtw.QApplication(sys.argv)
	window = Qtw.QMainWindow()
	window.setWindowTitle("Special ComboBoxes Demo")
	window.resize(300, 100)
	centralWidget = Qtw.QWidget()
	window.setCentralWidget(centralWidget)

	layout = Qtw.QVBoxLayout(centralWidget)
	centralWidget.setLayout(layout)
	font_box = TtfComboBox()
	font_size_box = FontSizeComboBox()
	layout.addWidget(font_size_box)
	layout.addWidget(font_box)

	window.show()
	sys.exit(app.exec())