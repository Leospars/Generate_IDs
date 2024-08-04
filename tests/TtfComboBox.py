from PyQt5.QtWidgets import QApplication, QFontComboBox, QVBoxLayout, QWidget
from GetFonts import GetFonts as gf


class TtfComboBox(QFontComboBox):
    def __init__(self):
        super(QFontComboBox, self).__init__()
        self.clear()
        font_dirmap = gf.get_font_dirmap()
        print(f"Number of Fonts: {len(font_dirmap.keys())}")
        self.addItems(font_dirmap.keys())

# Create an instance of QApplication
class App(QApplication):
    def __init__(self):
        super(QApplication, self).__init__([])
        self.font_combo5 = None
        self.app = QApplication([])
        self.window = None
        self.layout = None
        self.font_combo1 = None
        self.font_combo2 = None
        self.font_combo3 = None
        self.font_combo4 = None
        self.ttf_combo = None
        self.run()

    def run(self):
        self.window = QWidget()
        self.layout = QVBoxLayout()

        self.font_combo1 = QFontComboBox()
        self.font_combo1.setFontFilters(QFontComboBox.AllFonts)

        self.font_combo2 = QFontComboBox()
        self.font_combo2.setFontFilters(QFontComboBox.ScalableFonts)

        self.font_combo3 = QFontComboBox()
        self.font_combo3.setFontFilters(QFontComboBox.NonScalableFonts)

        self.font_combo4 = QFontComboBox()
        self.font_combo4.setFontFilters(QFontComboBox.MonospacedFonts)
        print(f"All monospace Fonts: {self.font_combo4.children()}")

        self.font_combo5 = QFontComboBox()
        self.font_combo5.setFontFilters(QFontComboBox.ProportionalFonts)

        self.ttf_combo = TtfComboBox()
        print(f"All ttf Fonts: {self.ttf_combo.children()}")

        self.layout.addWidget(self.font_combo1)
        self.layout.addWidget(self.font_combo3)
        self.layout.addWidget(self.ttf_combo)
        self.window.setLayout(self.layout)
        self.window.show()


app = App()
app.exec_()