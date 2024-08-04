import os

import PyQt5.QtGui
from PIL import ImageFont, ImageDraw, Image
from PyQt5.QtWidgets import QApplication


def get_fonts_directory():
    if os.name == "nt":
        return os.path.join(os.environ['WINDIR'], 'Fonts')
    elif os.name == "posix":
        if 'darwin' in os.uname().sysname.lower():
            return "/System/Library/Fonts"
        else:
            return "/usr/share/fonts"
    else:
        return None


def get_downloads_directory():
    if os.name == "nt":
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    elif os.name == "posix":
        return os.path.join(os.environ['HOME'], 'Downloads')
    else:
        return None


font_dirmap = dict()  # Map all ttf font family to font file location


def find_all_ttf_fonts():
    fonts_dir = get_fonts_directory()
    if not fonts_dir:
        print("This function is only for Windows, Linux, and macOS.")
        return None

    ttf_fonts = []

    def get_ttf_fonts(dir):
        ttf_fonts = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".ttf"):
                    ttf_fonts.append(os.path.join(root, file))
        return ttf_fonts

    directories = [fonts_dir, os.path.abspath("../font"), os.path.join(get_downloads_directory(), "Fonts")]
    for dir in directories:
        if os.path.exists(dir):
            ttf_fonts = get_ttf_fonts(dir)
            # Check if all the fonts can be loaded by PIL
            for font_location in ttf_fonts:
                try:
                    loaded_Font = ImageFont.truetype(font_location)
                    font_family = loaded_Font.getname()[0]
                    font_dirmap[font_family] = font_location
                except Exception as e:
                    print(f"Cannot load {font_location} font")
                    ttf_fonts.remove(font_location)
                    continue
    return ttf_fonts


system_ttf_fonts = find_all_ttf_fonts()  # List of all ttf fonts in the system


# Search for the font file in the fonts direct
def find_ttf_font(font_family):
    return font_dirmap.get(font_family, None)


def qFontToPILFont(qfont: PyQt5.QtGui.QFont):
    if qfont.family() in font_dirmap:
        return ImageFont.truetype(font_dirmap[qfont], qfont.pointSize())
    else:
        return None


ttfComboBox = PyQt5.QtWidgets.QComboBox()
ttfComboBox.addItems(font_dirmap.keys())

if __name__ == "__main__":
    print(f"Mapped fonts: {font_dirmap}")

    font = PyQt5.QtGui.QFont("Lucida Console", 12)
    print(f"Font: {font.family()}, {font.pointSize()}pt")

    print(f"All ttf fonts mapped: {font_dirmap}")
    # display the font in a PyQt Label
    # async def execApp():
    #     app = QApplication([])
    #     label = QLabel("Hello World")
    #     label.setFont(font)
    #     label.show()
    #     app.exec_()
    #
    # asyncio.run(execApp())

    print(f"Font Family: {font.family()}")
    font_path = find_ttf_font(str(font.family()))
    if font_path:
        print(f"Font path: {font_path}")
    else:
        print(f"Font '{font.family()}' not found in the fonts directory. ")

    if font_path:
        # Write on a blank image in the font
        img = Image.new('RGB', (200, 100), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), "Hello World", font=ImageFont.truetype(font_path, 20))
        img.show()