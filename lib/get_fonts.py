import os

from PIL import ImageFont
from PyQt5.QtGui import QFont


class GetFonts:
    """
    Find all ttf fonts in the system and map them to their font family
    param system_ttf_fonts: List of all ttf fonts files in the system
    param ttf_dir_map: Map all ttf font family to font file location in directories(dir) {family: file_location}
    """

    def __init__(self):
        self.system_ttf_fonts = self.find_all_ttf_fonts()  # List of all ttf fonts files in the system
        self.ttf_db = self.map_ttf_dir()  # Map all ttf font family to font file location
        self.uploaded_fonts = self._get_uploaded_fonts()  # List file location of ttf files uploaded in app

    @staticmethod
    def _get_uploaded_fonts():
        fonts = []
        # create a list of the absolute file location of all the fonts in this folder

        for root, dirs, files in os.walk(os.path.abspath("../font")):
            for file in files:
                if file.endswith(".ttf"):
                    fonts.append(os.path.join(root, file))

        return fonts

    @staticmethod
    def __get_fonts_directory__():
        if os.name == "nt":
            return os.path.join(os.environ['WINDIR'], 'Fonts')
        elif os.name == "posix":
            if 'darwin' in os.uname().sysname.lower():
                return "/System/Library/Fonts"
            else:
                return "/usr/share/fonts"
        else:
            return None

    @staticmethod
    def __get_downloads_directory__():
        if os.name == "nt":
            return os.path.join(os.environ['USERPROFILE'], 'Downloads')
        elif os.name == "posix":
            return os.path.join(os.environ['HOME'], 'Downloads')
        else:
            return None

    @staticmethod
    def find_all_ttf_fonts():
        fonts_dir = GetFonts.__get_fonts_directory__()
        if not fonts_dir:
            print("This function is only for Windows, Linux, and macOS.")
            return None

        def get_ttf_fonts(_dir):
            fonts = []
            for root, dirs, files in os.walk(_dir):
                for file in files:
                    if file.endswith(".ttf"):
                        fonts.append(os.path.join(root, file))
            return fonts

        directories = [fonts_dir, os.path.join(os.path.curdir, "./font"),
                       os.path.join(GetFonts.__get_downloads_directory__(), "Fonts")]
        system_ttf_fonts = []
        for _dir in directories:
            if os.path.exists(_dir):
                ttf_fonts = get_ttf_fonts(_dir)
                # Check if all the fonts can be loaded by PIL
                for font_location in ttf_fonts:
                    try:
                        ImageFont.truetype(font_location)  # try loading font
                        system_ttf_fonts.append(font_location)
                    except Exception as e:
                        print(f"Cannot load {font_location} font: {e}")
                        ttf_fonts.remove(font_location)
                        continue
        return system_ttf_fonts  # List of all ttf fonts in the system

    @staticmethod
    def map_ttf_dir():
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
        return self.ttf_db.get(font_family, None)

    def qfont_to_ttf(self, qfont: QFont):
        qfont_family = qfont.family()
        if qfont_family in self.ttf_db:
            return ImageFont.truetype(self.ttf_db[qfont_family], float(qfont.pointSize()))
        else:
            print(f"Font conversion not found for {qfont_family}. Exiting...")
            return None


if __name__ == "__main__":
    from PIL import Image, ImageDraw

    gf = GetFonts()
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
