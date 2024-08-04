from PyQt5.QtWidgets import QFontComboBox
from GetFonts import GetFonts

class TtfComboBox(QFontComboBox):
    def __init__(self):
        super(QFontComboBox, self).__init__()
        self.clear()
        font_dirmap = GetFonts.get_font_dirmap()
        print(f"Number of Fonts: {len(font_dirmap.keys())}")
        self.addItems(font_dirmap.keys())