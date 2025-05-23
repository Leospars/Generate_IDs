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

from pathlib import Path
CURR_FILE = Path(__file__).resolve()
DIR = Path(__file__).resolve().parent

from lib.id_generator import ID_Generator
from lib.canvas import Canvas
from lib.canvas import center_rect
from lib.configured_log import log as print
from lib.generate_tabs import generate_tool_box, update_tool_box, get_data_from_toolbox
from lib.paths import IMG_DIR  # evaluates and updates BASE_DIR
from main_ui import Ui_MainWindow

print(f"Main Path: {Path(__file__).resolve()}")
print(f"Main Base Dir: {DIR}")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # loadUi('main.ui', self)
        self.template_fpath = str(IMG_DIR / "no-image.png")
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
        self.template_img.setPixmap(QPixmap(self.template_fpath))

        # remove all pages in tool box
        self.clear_ids()

    def setEventHandlers(self):
        self.uploadButton.clicked.connect(self.uploadImage)
        self.generateIDButton.clicked.connect(self.generate_certificates)
        self.addTextBoxButton.clicked.connect(self.addTextBox)
        self.clearIDButton.clicked.connect(self.clear_ids)

    def uploadImage(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Template File", str(IMG_DIR),
                                                  "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")

        self.template_fpath = file_path if file_path else self.template_fpath
        if self.template_fpath:
            self.template_img.setPixmap(QPixmap(self.template_fpath))
            print(self.template_fpath)

    def clear_ids(self):
        self.canvas.clearCanvas()
        print(f"Range: {range(0, self.tool_box.count())}, {list(range(0, self.tool_box.count()))} ")
        for i in reversed(range(0, self.tool_box.count())):
            print(f"Removing page {i}: {self.tool_box.widget(i).objectName() if self.tool_box.widget(i) else None}")
            self.tool_box.removeItem(i)
        print(f"Toolbox is emptied now. Page Count: {self.tool_box.count()}")
        generate_tool_box(self.tool_box, self.canvas)

    def addPaint(self, canvas):
        painter = canvas.painter
        # tint background
        painter.setBrush(Qt.green)
        painter.setOpacity(0.2)
        painter.drawRect(self.rect())

    def generate_certificates(self):
        print("Generating ID")
        generator = ID_Generator(self.canvas.rectLabels, self.canvas.rects, self.canvas.rectFonts,
                                 self.template_fpath)
        toolbox_data = get_data_from_toolbox(self.tool_box, self.canvas)
        data_list = [page_data.labels for page_data in toolbox_data]
        fonts = [page_data.metadata for page_data in toolbox_data]
        label_positions = [page_data.position for page_data in toolbox_data]
        alignment = [page_data.alignment for page_data in toolbox_data]

        generator.gen_certs(data_list, label_positions, fonts, self.template_fpath,
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

        update_tool_box(self.tool_box, self.canvas)
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
