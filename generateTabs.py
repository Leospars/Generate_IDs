from PIL.ImageFont import FreeTypeFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBox

from tests.SpecialComboBox import TtfComboBox, FontSizeComboBox
from tests.canvas import Canvas

class DataObject:
	"""
	to put in the data_type use type(var).__name__
	"""

	def __init__(self, data_type: str, data: str, position: QRect, metadata: QFont | FreeTypeFont, alignment="Center"):
		self.type = data_type.__name__ if isinstance(data_type, type) else data_type
		self.data = data
		self.position = position
		self.metadata = metadata
		self.alignment = alignment

def get_data_from_canvas(canvas: Canvas):
	data_array = []
	for rect, label, font in zip(canvas.rects, canvas.rectLabels, canvas.rectFonts):
		canvas_data = DataObject(type(label), label, rect, font)
		data_array.append(canvas_data)
	return data_array

# helper function to translate texts in the window
__translate__ = QtCore.QCoreApplication.translate

def generateToolBox(parent: QToolBox, canvas: Canvas | list[DataObject]):
	# if data types entered do not match expected throw an error
	if not isinstance(canvas, Canvas) and not isinstance(canvas, list):
		raise TypeError("canvas must be of type Canvas")

	if not isinstance(parent, QToolBox):
		raise TypeError("parent must be of type QToolBox")

	tool_box = QtWidgets.QToolBox()
	tool_box.setObjectName("toolBox")

	# get canvas data for generating frames
	canvas_data = get_data_from_canvas(canvas)

	# create a page for each field in the toolbox
	for box in canvas_data:
		field_name = box.data
		font = box.metadata
		data_type = type(font).__name__

		# create a page for each field in the toolbox
		page = QtWidgets.QWidget(tool_box)
		page.setObjectName(field_name + '_page')
		page.setGeometry(0, 0, 730, 232)

		# initialize font combobox
		ttf_combo_box = TtfComboBox(page)
		ttf_combo_box.setGeometry(QtCore.QRect(0, 0, 226, 22))
		ttf_combo_box.setObjectName(field_name + '_ttfBox')
		ttf_combo_box.setCurrentFont(font)

		# initialize font size combobox
		font_size_combo_box = FontSizeComboBox(page)
		font_size_combo_box.setGeometry(QtCore.QRect(246, 0, 226, 22))
		font_size_combo_box.setObjectName(field_name + '_fontSizeBox')
		font_size_combo_box.setCurrentText(str(font.pointSize()))
		font_size_combo_box.setGeometry(QtCore.QRect(240, 0, 73, 22))
		font_size_combo_box.setMaxVisibleItems(8)

		# initialize text box
		text_box = QtWidgets.QPlainTextEdit(page)
		text_box.setGeometry(QtCore.QRect(0, 30, 800, 80))
		text_box.setObjectName(field_name + '_data')
		if data_type == "QFont":
			text_box.setPlaceholderText(__translate__("MainWindow", "Enter comma seperated values here . . .\n"))
		else:
			# TODO: Add support for auto generating images
			text_box.setPlaceholderText(__translate__("MainWindow", "Enter path to folder with images"))

		# add the combo boxes to the page
		tool_box.addItem(page, __translate__("MainWindow", field_name))
		vLayout.addWidget(tool_box)  # Add the toolbox to the vLayout in the window

	tool_box.show()
	QtCore.QMetaObject.connectSlotsByName(parent)

def updateToolBox(tool_box: QToolBox, canvas: Canvas):
	# ignore up to last page than add to toolbox
	last_page = tool_box.count()
	canvas_data = get_data_from_canvas(canvas)
	canvas_data = canvas_data[last_page:]
	generateToolBox(tool_box, canvas_data)

class MainWindow(QMainWindow):
	def __init__(self):
		super(QMainWindow, self).__init__()
		generateToolBox(self, canvas)

if __name__ == "__main__":
	# test the generateTabs function
	app = QApplication([])
	canvas = Canvas()
	canvas.setGeometry(0, 0, 1100, 300)
	canvas.addTextBoxContent([QRect(0, 0, 100, 100), QRect(0, 0, 100, 100)], ["Name", "ID_Number"],
							 [QFont("Arial", 12), QFont("Lucida Console", 12)])

	window = QMainWindow()
	window.resize(800, 600)
	window.setWindowTitle("Generate Toolbox for IDs")
	centralWidget = QtWidgets.QWidget()
	window.setCentralWidget(centralWidget)
	vLayout = QtWidgets.QVBoxLayout(centralWidget)
	vLayout.setObjectName("verticalLayout")

	window.tool_box = QtWidgets.QToolBox()
	vLayout.addWidget(window.tool_box)

	generateToolBox(window.tool_box, canvas)
	window.show()
	app.exec()

	pass