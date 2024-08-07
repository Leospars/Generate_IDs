''' Create GUI for auto_cert.py to allow users to
    - Select a template
    - Select a folder to save the certificates
    - Select the font size
    - Position the text box and alignment of the text
    - Generate certificates
'''

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow, QDialog

from generateID_ui import Ui_MainWindow
from generateTabs import generateToolBox, updateToolBox
from tests.canvas import Canvas
from tests.windowBuild import centerRectOnScreen

# from PyQt5.uic import loadUi

textBoxNum = 0

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(QMainWindow, self).__init__()
		# loadUi('generateID.ui', self)
		self.setupUi(self)
		self.show()
		self.addWidgets()
		self.setEventHandlers()

	def addWidgets(self):
		self.canvas = Canvas(self.frame)
		self.canvas.setGeometry(self.template_img.geometry())
		self.canvas.draw = lambda: self.addPaint(self.canvas)
		print(f"canvas geometry: {self.canvas.geometry()} template_img geo {self.template_img.geometry()}\n"
			  f"canvas hint {self.canvas.sizeHint()} template_img hint {self.template_img.sizeHint()}\n"
			  f"canvas sizePolicy {self.canvas.sizePolicy()} template_img sizePolicy "
			  f"{self.template_img.sizePolicy()}\n")

		# create dialog window for adding data
		self.dataDialog = QDialog()
		self.dataDialog.setWindowTitle("Add Data For ID")
		self.dataDialog.setGeometry(centerRectOnScreen(300, 400))

		# remove all pages in tool box
		for i in range(0, self.tool_box.count()):
			self.tool_box.removeItem(i)
		print(f"Toolbox is emptied now. Page Count: {self.tool_box.count()}")
		generateToolBox(self.tool_box, self.canvas)

	def setEventHandlers(self):
		self.uploadButton.clicked.connect(self.uploadImage)
		self.generateIDButton.clicked.connect(self.generateID)
		self.addTextBoxButton.clicked.connect(self.addTextBox)
		self.clearIDButton.clicked.connect(self.canvas.clearCanvas)

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
		painter.drawRect(self.rect())

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

		# get font size
		font_size = self.fontSizeComboBox.currentText()
		font.setPointSize(int(font_size))

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
		updateToolBox(self.tool_box, self.canvas)
		self.canvas.unsetCursor()  # revert cursor
		self.canvas.mousePressEvent = lambda ev: None  # remove event handler
		print(f"{_id} added at {x, y} with size {width}x{height}")
		print(f"Toolbox Page Count: {self.tool_box.count()}")

	def createTextBoxOnClick(self, event):
		# On first click get top left corner from user input
		x, y = event.pos().x(), event.pos().y()
		# TODO: Show text box preview onMouseMove Event

		# On second click
		self.canvas.mousePressEvent = lambda ev: self.__addTextBox2ndClick__(ev, x, y)

if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()