import os
from pathlib import Path

from PIL import ImageFont
from PyQt5.QtGui import QFont
from lib.paths import BASE_DIR

class GetFonts:
    """
    Find all ttf fonts in the system and map them to their font family
    param system_ttf_fonts: List of all ttf fonts files in the system
    param ttf_dir_map: Map all ttf font family to font file location in directories(dir) {family: file_location}
    """

    def __init__(self):
        self.all_ttf_fonts: list[str] = self.find_all_ttf_fonts()  # List of all ttf fonts files in the system
        self.uploaded_fonts: list[str] = self._get_uploaded_fonts()  # List file location of ttf files uploaded in app
        self.ttf_db = self.map_ttf_dir()  # Map all ttf font family to font file location [family: file_location]

    @staticmethod
    def _get_ttf_fonts(_dir):
        fonts = []
        for root, dirs, files in os.walk(_dir):
            for file in files:
                if file.endswith(".ttf"):
                    fpath = str(Path(root) / file)
                    try:
                        ImageFont.truetype(fpath)
                        fonts.append(fpath)
                    except Exception as e:
                        print(f"Cannot load {fpath} font: {e}")
                        continue
        return fonts
    @staticmethod
    def _get_uploaded_fonts():
        fonts = []
        # create a list of the absolute file location of all the fonts in this folder
        fonts_dir = (BASE_DIR / "font").resolve()
        for root, dirs, files in os.walk(str(fonts_dir)):
            for file in files:
                if file.endswith(".ttf"):
                    fonts.append((Path(root) / file).resolve())
        return fonts

    @staticmethod
    def __get_fonts_directory__():
        if os.name == "nt":
            return Path(os.environ['WINDIR']) / 'Fonts'
        elif os.name == "posix":
            if 'darwin' in os.uname().sysname.lower():
                return "/System/Library/Fonts"
            else:
                return "/usr/share/fonts"
        else:
            return None

    @staticmethod
    def find_all_ttf_fonts():
        fonts_dir = GetFonts.__get_fonts_directory__()
        if not fonts_dir:
            print("This function is only for Windows, Linux, and macOS.")
            return None

        directories = [fonts_dir, str(BASE_DIR / "font")]
        system_ttf_fonts = []
        for _dir in directories:
            if _dir and Path(_dir).exists():
                ttf_fonts = GetFonts._get_ttf_fonts(_dir)
                system_ttf_fonts.extend(ttf_fonts)
        sorted(system_ttf_fonts)
        return system_ttf_fonts  # List of all ttf fonts in the system

    @staticmethod
    def map_ttf_dir() -> dict[str, str]: # [family: file_location]
        ttf_dir_map = {}
        all_fonts = GetFonts.find_all_ttf_fonts()
        for font_location in all_fonts:
            try:
                loaded_font = ImageFont.truetype(font_location)
                font_family = loaded_font.font.family
                ttf_dir_map[font_family] = font_location
            except Exception as e:
                print(f"Cannot load {font_location} font: {e}")
                continue
        ttf_dir_map = dict(sorted(ttf_dir_map.items()))  # Sort the dictionary by font family
        return ttf_dir_map

    # Search for the font file in the fonts direct
    def find_ttf_font(self, font_family):
        return self.ttf_db.get(font_family)

    def qfont_to_ttf(self, qfont: QFont):
        _qff = qfont.family()
        if _qff in self.ttf_db:
            return ImageFont.truetype(self.ttf_db[_qff], float(qfont.pointSize()))
        else:
            print(f"Font conversion not found for {_qff}. Exiting...")
            return None


if __name__ == "__main__":
    from PIL import Image, ImageDraw

    gf = GetFonts()
    print(f"Total TTF Fonts: {len(gf.all_ttf_fonts)} :\n All ttf fonts:")

    __filter_font_loc = list(filter(lambda font_loc: font_loc.endswith("Sans.ttf"), GetFonts().all_ttf_fonts))
    print(f"Default font: {__filter_font_loc}")
    font = QFont("Lucida Console", 12)
    ttf_font = gf.qfont_to_ttf(font)
    print(f"\nFont: {font.family()}, {font.pointSize()}pt")
    print(f"TTF Font: {ttf_font.font.family}, {ttf_font.font.height}pt")

    print(f"Font Family: {font.family()}")
    font_path = gf.find_ttf_font(font.family())
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
