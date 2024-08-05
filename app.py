''' Create GUI for generate_IDs.py to allow users to
    - Select a template
    - Select a folder to save the certificates
    - Select the font size
    - Position the text box and alignment of the text
    - Generate certificates
'''

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

from generateID_ui import Ui_MainWindow
from generateTabs import generateDataTab, dataTabUpdate
from tests.SpecialComboBox import TtfComboBox
from tests.canvas import Canvas

# from PyQt5.uic import loadUi

textBoxNum = 0

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(QMainWindow, self).__init__()
		# loadUi('generateID.ui', self)
		self.setupUi(self)
		self.addWidgets()
		self.setEventHandlers()

	def addWidgets(self):
		self.fontComboBox = TtfComboBox(self.fontComboBox)
		self.canvas = Canvas(self.template_img.parent())
		self.canvas.setGeometry(self.template_img.geometry())
		self.canvas.draw = lambda: self.addPaint(self.canvas)
		generateDataTab(self, self.canvas)

	def setEventHandlers(self):
		self.uploadButton.clicked.connect(self.uploadImage)
		self.generateIDButton.clicked.connect(self.generateID)
		self.addTextBoxButton.clicked.connect(self.addTextBox)
		self.clearIDButton.clicked.connect(self.canvas.clearCanvas)
		self.txtBox = Canvas(self)

	def uploadImage(self):
		template_filename, _ = QFileDialog.getOpenFileName(self, "Open Template File", "",
														   "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")
		if template_filename:
			self.template_img.setPixmap(QPixmap(template_filename))
			print(template_filename)

	def addPaint(self, canvas):
		painter = canvas.painter
		# tint background
		painter.setBrush(Qt.green)
		painter.setOpacity(0.2)
		painter.drawRect(self.geometry())

	def generateID(self):
		print("Generate ID")

	def addTextBox(self):
		# Change template image cursor
		self.canvas.setCursor(Qt.CrossCursor)
		self.canvas.mousePressEvent = lambda event: self.createTextBoxOnClick(event)
		print("Add Textbox")

	def __addTextBox2ndClick__(self, ev, x, y):
		# get data from user input
		width = ev.pos().x() - x
		height = ev.pos().y() - y
		font = self.fontComboBox.currentFont()  # get font from combobox

		# increment textBoxID
		_id = self.idTypeName.text() if self.idTypeName.text() else self.idTypeName.placeholderText()
		if _id in self.canvas.rectLabels:
			_id += "_" + str(len(self.canvas.rectLabels))

		# Add TextBox to canvas
		self.canvas.addTextBox(
			rect=QRect(x, y, width, height),
			_id=_id,
			font=font
		)
		dataTabUpdate(self, self.canvas)
		self.canvas.unsetCursor()  # revert cursor
		self.canvas.mousePressEvent = lambda ev: None  # remove event handler
		print(f"{_id} added at {x, y} with size {width}x{height}")

	def createTextBoxOnClick(self, event):
		# On first click get top  corner from user input
		x, y = event.pos().x(), event.pos().y()

		# On second click
		self.canvas.mousePressEvent = lambda ev: self.__addTextBox2ndClick__(ev, x, y)

if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()