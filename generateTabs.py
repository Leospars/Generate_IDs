import PyQt5
from PIL.ImageFont import FreeTypeFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolBox, QMainWindow, QApplication

from tests.SpecialComboBox import TtfComboBox
from tests.canvas import Canvas

class DataObject:
	"""
	to put in the data_type use type(var).__name__
	"""

	def __init__(self, data_type: str, data: str, position: QRect, metadata: QFont | FreeTypeFont,
				 alignment="Center"):
		self.type = data_type.__name__ if isinstance(data_type, type) else data_type
		self.data = data
		self.position = position
		self.metadata = metadata
		self.alignment = alignment

def get_data_from_canvas(canvas: Canvas):
	data_array = []
	for rect, label, font in zip(canvas.rects, canvas.rectLabels, canvas.rectFonts):
		canvas_data = DataObject(type(label), label, rect, font)
		print(canvas_data)
		data_array.append(canvas_data)
	return data_array

def generateDataTab(MainWindow: QMainWindow, canvas: Canvas):
	"""
	Set up the user interface for the MainWindow.
	Args:
		MainWindow (QMainWindow): The main window object.
		canvas (Canvas): The canvas object.
	"""
	MainWindow.setObjectName("MainWindow")
	MainWindow.setWindowTitle("dataUpdate")
	MainWindow.resize(768, 411)
	m_wind = MainWindow
	canvas_data = get_data_from_canvas(canvas)

	# Create the central widget and set its object name
	m_wind.Tab = QTabWidget()
	m_wind.Tab = QtWidgets.QTabWidget(MainWindow)
	m_wind.tool_box = QToolBox()  # initialize toolbox on page

	for box in canvas_data:
		field_name = box.data
		font = box.metadata

		# create a page for each field in the toolbox
		field_page = m_wind[field_name] = QWidget()
		field_page.setObjectName(field_name)
		field_page.setGeometry(0, 0, 1100, 300)

		# initialize font combobox
		ttfComboBox = m_wind[field_name + '_ttfBox'] = TtfComboBox()
		ttfComboBox.setGeometry(QtCore.QRect(0, 0, 226, 22))
		ttfComboBox.setObjectName(f"{field_name}_ttfBox")

		# initialize text box for user to enter comma seperated data
		# if data should be an image it should be a path to the images folder to be implemented
		data_input = m_wind[field_name + '_data']
		data_input = PyQt5.QtWidgets.QPlainTextEdit(field_page)
		data_input.setObjectName(field_name + '_data')
		data_input.setGeometry(0, 30, 800, 80)
		data_input.placeholderText("Enter comma seperated data here...")

		# add the font combobox and text box to the field page
		field_page.layout().addWidget(ttfComboBox)
		field_page.layout().addWidget(data_input)
		m_wind.tool_box.addItem(field_page, "")

# MainWindow.dataTab = QtWidgets.QWidget()
# MainWindow.dataTab.setObjectName("dataTab")
# MainWindow.verticalLayout_4 = QtWidgets.QVBoxLayout(MainWindow.dataTab)
# MainWindow.verticalLayout_4.setObjectName("verticalLayout_4")
#
# MainWindow.toolBox = QtWidgets.QToolBox(MainWindow.dataTab)
# MainWindow.toolBox.setObjectName("toolBox")
# MainWindow.toolBoxPage1 = QtWidgets.QWidget()
# MainWindow.toolBoxPage1.setGeometry(QtCore.QRect(0, 0, 1108, 609))
# MainWindow.toolBoxPage1.setObjectName("toolBoxPage1")
# MainWindow.textBox1_Data = QtWidgets.QPlainTextEdit(MainWindow.toolBoxPage1)
# MainWindow.textBox1_Data.setGeometry(QtCore.QRect(0, 30, 800, 80))
# sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
# sizePolicy.setHorizontalStretch(0)
# sizePolicy.setVerticalStretch(0)
# sizePolicy.setHeightForWidth(MainWindow.textBox1_Data.sizePolicy().hasHeightForWidth())
# MainWindow.textBox1_Data.setSizePolicy(sizePolicy)
# MainWindow.textBox1_Data.setObjectName("textBox1_Data")
# MainWindow.idTtfComboBox_1 = QtWidgets.QFontComboBox(MainWindow.toolBoxPage1)
# MainWindow.idTtfComboBox_1.setGeometry(QtCore.QRect(0, 0, 226, 22))
# MainWindow.idTtfComboBox_1.setObjectName("idTtfComboBox_1")
# MainWindow.toolBox.addItem(MainWindow.toolBoxPage1, "")
# MainWindow.toolBoxPage2 = QtWidgets.QWidget()
# MainWindow.toolBoxPage2.setGeometry(QtCore.QRect(0, 0, 1090, 243))
# MainWindow.toolBoxPage2.setObjectName("toolBoxPage2")
# MainWindow.textBox2_Data = QtWidgets.QPlainTextEdit(MainWindow.toolBoxPage2)
# MainWindow.textBox2_Data.setGeometry(QtCore.QRect(0, 30, 800, 80))
# MainWindow.textBox2_Data.setObjectName("textBox2_Data")
# MainWindow.idTtfComboBox_2 = QtWidgets.QFontComboBox(MainWindow.toolBoxPage2)
# MainWindow.idTtfComboBox_2.setGeometry(QtCore.QRect(0, 0, 226, 22))
# MainWindow.idTtfComboBox_2.setObjectName("idTtfComboBox_2")
# MainWindow.toolBox.addItem(MainWindow.toolBoxPage2, "")
# MainWindow.page = QtWidgets.QWidget()
# MainWindow.page.setGeometry(QtCore.QRect(0, 0, 1108, 609))
# MainWindow.page.setObjectName("page")
# MainWindow.toolBox.addItem(MainWindow.page, "")
# MainWindow.verticalLayout_4.addWidget(MainWindow.toolBox)
# MainWindow.Tab.addTab(MainWindow.dataTab, "")

def dataTabUpdate(self, canvas: Canvas):
	pass

class MainWindow(QMainWindow):
	def __init__(self):
		super(QMainWindow, self).__init__()
		generateDataTab(self, canvas)

if __name__ == "__main__":
	# test the generateDataTab function
	app = QApplication([])
	canvas = Canvas()
	canvas.setGeometry(0, 0, 1100, 300)
	canvas.addTextBoxContent(
		[QRect(0, 0, 100, 100), QRect(0, 0, 100, 100)],
		["Name", "ID_Number"],
		[QFont("Arial", 12), QFont("Lucida Console", 12)]
	)
	window = QMainWindow()
	generateDataTab(window, canvas)
	window.show()
	app.exec()

	pass