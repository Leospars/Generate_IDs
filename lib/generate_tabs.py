from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBox

from lib.canvas import Canvas
from lib.configured_log import log as print
from lib.special_combo_box import TtfComboBox, FontSizeComboBox


class CanvasData:
    """
    store data for each canvas field
    """

    # TODO: Use class constant variables for alignment
    def __init__(self, data: str | Image, position: QRect, metadata: QFont | FreeTypeFont, alignment="center",
                 is_text=True):
        self.isText = is_text
        self.label_name = data if is_text else "Image"
        self.image = data if not is_text else None
        self.position = position
        self.metadata = metadata
        self.alignment = alignment


class ToolPageData:
    """
    store data from toolbox pages
    """

    # TODO: Use class constant variables for alignment
    def __init__(self, page_name: str, labels: list[str], position: QRect, metadata: QFont,
                 alignment="center", is_text=True, images: list[Image] = None):
        self.page_name = page_name
        self.isText = is_text
        self.labels = labels if is_text else []
        self.images = images
        self.position = position
        self.metadata = metadata
        self.alignment = alignment


def get_data_from_canvas(canvas: Canvas):
    canvas_data_list = []
    for rect, label, font in zip(canvas.rects, canvas.rectLabels, canvas.rectFonts):
        canvas_data = CanvasData(label, rect, font, is_text=True)
        canvas_data_list.append(canvas_data)
    return canvas_data_list


# helper function to translate texts in the window
__translate__ = QtCore.QCoreApplication.translate


def generate_tool_box(tool_box: QToolBox, canvas: Canvas | list[CanvasData]):
    # if data types entered do not match expected throw an error
    if not isinstance(canvas, Canvas) and not isinstance(canvas, list):
        raise TypeError("canvas must be of type Canvas")

    if not isinstance(tool_box, QToolBox):
        raise TypeError("tool_box must be of type QToolBox")

    tool_box.setObjectName("toolBox")

    # get canvas data for generating frames
    if isinstance(canvas, Canvas):
        canvas_data = get_data_from_canvas(canvas)
    else:
        canvas_data = canvas

    # create a page for each field in the toolbox
    for label in canvas_data:
        field_name = label.label_name
        font = label.metadata
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
            text_box.setPlaceholderText("Enter comma seperated values here . . .\n")
        else:
            # TODO: Add support for auto generating images
            text_box.setPlaceholderText("Enter path to folder with images")

        # add the page to the toolbox
        tool_box.addItem(page, field_name)
        print(f"Toolbox Page Count In function: {tool_box.count()}")
    return tool_box


def update_tool_box(tool_box: QToolBox, canvas: Canvas):
    # if data types entered do not match expected throw an error
    if not isinstance(canvas, Canvas) and not (isinstance(canvas, list) and isinstance(canvas[0], CanvasData)):
        raise TypeError("canvas must be of type Canvas")

    if not isinstance(tool_box, QToolBox):
        raise TypeError("tool_box must be of type QToolBox")

    # ignore up to last page than add to toolbox
    last_page = tool_box.count()
    canvas_data = get_data_from_canvas(canvas)
    canvas_data = canvas_data[last_page:]
    generate_tool_box(tool_box, canvas_data)


def get_data_from_toolbox(tool_box: QToolBox, canvas: Canvas):
    canvas_data = get_data_from_canvas(canvas)
    toolbox_data = []

    for i in range(tool_box.count()):
        page = tool_box.widget(i)
        if canvas_data[i].isText:
            label_name = canvas_data[i].label_name
        else:
            print("Image data not supported yet")
            return

        text_box = page.findChild(QtWidgets.QPlainTextEdit, f"{label_name}_data")
        font_combo_box = page.findChild(TtfComboBox, f"{label_name}_ttfBox")
        font_size_combo_box = page.findChild(FontSizeComboBox, f"{label_name}_fontSizeBox")

        # get Convert text in textbox to list
        text = text_box.toPlainText().strip()
        labels = text.split(",") if text else []
        labels = [label.strip() for label in labels]

        # get font and font size
        font_size = int(font_size_combo_box.currentText())
        font = font_combo_box.currentFont()
        font.setPointSize(font_size)

        # extend data to respective lists
        page_data = ToolPageData(f"{label_name}_page", labels, canvas_data[i].position, font)
        toolbox_data.append(page_data)

    return toolbox_data


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        generate_tool_box(self, canvas)


if __name__ == "__main__":
    # test the generateTabs function
    app = QApplication([])
    canvas = Canvas()
    canvas.addTextBoxContent([QRect(0, 0, 100, 100), QRect(0, 0, 130, 100)], ["Name", "ID_Number"],
                             [QFont("Arial", 12), QFont("Lucida Console", 12)])
    window = QMainWindow()
    window.resize(800, 600)
    window.setWindowTitle("Generate Toolbox for IDs")
    window.mainLayout = QtWidgets.QVBoxLayout()

    centralWidget = QtWidgets.QWidget()
    centralWidget.resize(800, 600)
    window.setCentralWidget(centralWidget)
    window.mainLayout.addWidget(centralWidget)
    window.setLayout(window.mainLayout)

    vLayout = QtWidgets.QVBoxLayout(centralWidget)
    vLayout.setObjectName("verticalLayout")

    window.tool_box = QtWidgets.QToolBox()
    generate_tool_box(window.tool_box, canvas)
    get_data_from_toolbox(window.tool_box, canvas)
    vLayout.addWidget(window.tool_box)
    centralWidget.setLayout(vLayout)

    window.show()
    app.exec()
