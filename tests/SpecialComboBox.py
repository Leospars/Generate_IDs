import PyQt5.QtWidgets as Qtw

from tests.GetFonts import GetFonts

class TtfComboBox(Qtw.QFontComboBox):
	def __init__(self, parent: Qtw.QWidget | None = None):
		super().__init__()
		self.clear()
		font_dirmap = GetFonts.get_font_dirmap()
		self.addItems(font_dirmap.keys())
		self.setParent(parent)

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
	app = Qtw.QApplication([])
	window = Qtw.QMainWindow()
	window.setWindowTitle("Special ComboBoxes")
	window.resize(300, 200)
	centWidget = Qtw.QWidget()
	import sys

	print(sys.argv)
	layout = Qtw.QGridLayout(window)
	font_box = TtfComboBox(window)
	font_size_box = FontSizeComboBox(window)
	layout.addWidget(font_size_box, 0, 0, 1, 1)
	layout.addWidget(font_box, 1, 1, 1, 1)

	# vLayout.addLayout(layout)
	window.setLayout(layout)
	window.show()
	app.exec()