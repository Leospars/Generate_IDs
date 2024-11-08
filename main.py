''' Create GUI to allow users to
    - Select a template
    - Select a folder to save the certificates
    - Select the font size
    - Position the text box and alignment of the text
    - Generate certificates
'''

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow, QDialog

from id_generator import ID_Generator
from lib.canvas import Canvas
from lib.configured_log import log as print
from lib.generate_tabs import generateToolBox, updateToolBox, get_data_from_toolbox
from main_ui import Ui_MainWindow
from tests.windowBuild import center_rect


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # loadUi('main.ui', self)
        self.template_filename = "./img/no-image.png"
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
        self.dataDialog.setGeometry(center_rect(300, 400))

        # set default template image
        self.template_img.setPixmap(QPixmap(self.template_filename))

        # remove all pages in tool box
        self.clear_ids()

    def setEventHandlers(self):
        self.uploadButton.clicked.connect(self.uploadImage)
        self.generateIDButton.clicked.connect(self.generate_certificates)
        self.addTextBoxButton.clicked.connect(self.addTextBox)
        self.clearIDButton.clicked.connect(self.clear_ids)

    def uploadImage(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Template File", "",
                                                  "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")

        self.template_filename = filename if filename else self.template_filename
        if self.template_filename:
            self.template_img.setPixmap(QPixmap(self.template_filename))
            print(self.template_filename)

    def clear_ids(self):
        self.canvas.clearCanvas()
        print(f"Range: {range(0, self.tool_box.count())}, {list(range(0, self.tool_box.count()))} ")
        for i in reversed(range(0, self.tool_box.count())):
            print(f"Removing page {i}: {self.tool_box.widget(i).objectName() if self.tool_box.widget(i) else None}")
            self.tool_box.removeItem(i)
        print(f"Toolbox is emptied now. Page Count: {self.tool_box.count()}")
        generateToolBox(self.tool_box, self.canvas)

    def addPaint(self, canvas):
        painter = canvas.painter
        # tint background
        painter.setBrush(Qt.green)
        painter.setOpacity(0.2)
        painter.drawRect(self.rect())

    def generate_certificates(self):
        print("Generating ID")
        generator = ID_Generator(self.canvas.rectLabels, self.canvas.rects, self.canvas.rectFonts,
                                 self.template_filename)
        toolbox_data = get_data_from_toolbox(self.tool_box, self.canvas)
        data_list = [data.labels for data in toolbox_data]
        fonts = [data.metadata for data in toolbox_data]
        label_positions = [data.position for data in toolbox_data]
        alignment = [data.alignment for data in toolbox_data]

        generator.gen_certs(data_list, label_positions, fonts, self.template_filename,
                            alignment=alignment, canvas_size=self.canvas.size())

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

        # Move start coordinates to top left corner if width or height is negative
        if width < 0 or height < 0:
            x, y = (x + width), (y + height)
            width, height = abs(width), abs(height)

        # Add TextBox to canvas
        self.canvas.addTextBox(
            rect=QRect(x, y, width, height),
            _id=_id,
            font=font
        )
        # print(f"Canvas Data: {self.canvas.rects, self.canvas.rectLabels,
        # [[font.family(), font.pointSize()] for font in self.canvas.rectFonts]}")

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
