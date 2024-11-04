import PyQt5.QtWidgets as Qtw
from PyQt5.QtGui import QFont

from tests.GetFonts import GetFonts


class TtfComboBox(Qtw.QComboBox):
    def __init__(self, parent: Qtw.QWidget | None = None):
        super().__init__(parent)
        self.clear()
        self.all_fonts = GetFonts().ttf_db.keys()
        self.addItems(self.all_fonts)
        self.setCurrentFont(QFont("Arial", 12))
        self.setCurrentText("Arial")

    def setCurrentFont(self, font: QFont) -> None:
        self.setCurrentText(font.family())
        self.setCurrentIndex(self.findText(font.family()))

    def currentFont(self) -> QFont:
        return QFont(self.currentText(), 10)


class FontSizeComboBox(Qtw.QComboBox):
    def __init__(self, parent: Qtw.QWidget | None = None):
        super().__init__()
        self.clear()
        self.setParent(parent)
        self.setEditable(True)  # allow user to enter custom font size
        for i in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 32, 36, 48, 72]:
            self.addItem(str(i))
        self.setCurrentText("12")
        self.resize(54, 22)
        self.lineEdit().editingFinished.connect(self.validate_input)

    def validate_input(self):
        text = self.currentText()
        try:
            value = int(text)
            if value < 1 or value > 700:
                raise ValueError
        except ValueError:
            Qtw.QMessageBox.warning(self, "Invalid Input", "Please enter a valid font size between 1 and 700.")
            # remove invalid input from the combobox
            self.removeItem(self.currentIndex())
            self.setCurrentText("12")  # Reset to default value


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
