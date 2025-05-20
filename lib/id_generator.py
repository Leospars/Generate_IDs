import re
import tkinter
from tkinter import filedialog

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from os import startfile

from lib.configured_log import log as print
from lib.get_fonts import GetFonts
from lib.paths import get_downloads_directory, BASE_DIR, FONT_DIR, IMG_DIR


class ID_Generator:
    __filter_font_loc = list(filter(lambda font_loc: font_loc.endswith("Sans.ttf"), GetFonts().all_ttf_fonts))
    _default_font = ImageFont.truetype(__filter_font_loc[0], 55)
    print(f"Default Font: {_default_font.font.family}, {_default_font.font.height}pt")

    def __init__(self, data: list[list[str]], label_positions: list[QRect], fonts: list[QFont], template: str,
                 save_folder="",
                 alignment="center"):

        self.data = data
        self.label_positions = label_positions
        self.template = template
        self.save_folder = save_folder
        if fonts is None:
            self.fonts: list[FreeTypeFont] = [ID_Generator._default_font]
        else:
            self.fonts = fonts
        self.alignment: str = alignment
        self.saved_filepaths: list[Path] = []
        self.save_folder = ""
        self.id_group = "Certificate"

    @staticmethod
    def select_save_folder():
        tk = tkinter.Tk()
        tk.withdraw()
        save_folder = filedialog.askdirectory(title="Save Generated Certificates to", initialdir=get_downloads_directory())
        if not save_folder:
            print("No folder selected. Exiting...")
            tk.destroy()
            return

        print(f"Save folder: {save_folder}")
        tk.destroy()
        return save_folder

    @staticmethod
    def get_file_location(title_msg: str):
        tk = tkinter.Tk()
        tk.withdraw()
        file_location = filedialog.askopenfile(title=title_msg)
        print(f"File location: {file_location}")
        return file_location

    def gen_certs(self, data_list: list[list[str]], label_positions: list[QRect], fonts: list[QFont],
                  template: str = "", canvas_size=QRect(0, 0, 1037, 801), save_folder: str = None,
                  alignment: list[str] = None):

        data_list = self.data if not data_list else data_list
        label_positions = self.label_positions if not label_positions else label_positions
        template = self.template if not template else template
        save_folder = self.save_folder if not save_folder else save_folder

        if not data_list or not data_list[0] or not label_positions:
            print("No data provided. Exiting...")
            return

        if not save_folder:
            save_folder = ID_Generator.select_save_folder()
            if save_folder is None:
                print("No folder selected. Exiting...")
                return

        if not fonts:
            print("No fonts provided. Exiting...")
            return
        else:
            for i in range(len(fonts)):
                font = fonts[i]
                if not font:
                    print("Font not found. Exiting...")
                    return
                else:
                    fonts[i] = GetFonts().qfont_to_ttf(fonts[i])

        if not alignment:
            alignment = [self.alignment]

        num_certs = max(map(len, data_list))
        longest_list_i = data_list.index(max(data_list, key=len))  # will generate this list first
        print(f"Number of Certificates: {num_certs}")
        print(f"File name list: {data_list[longest_list_i]}")

        # If the data lists entered are different lengths repeat the last data set, good for entering signatures
        for data in data_list:
            [data.append(data[-1]) for _ in range(num_certs - len(data))]

        # print adjusted parameters
        print(f"Data: {data_list}\nLabel Positions: {label_positions}\nTemplate: {template}\n"
              f"Save Folder: {save_folder}\nFonts: {[[ttf.font.family, ttf.font.height] for ttf in fonts]}\n"
              f"Alignment: {alignment}")

        # Generate certificate with the longest label first
        self.add_label_to_cert(data_list[longest_list_i], fonts[longest_list_i],
                               label_positions[longest_list_i], template, save_folder,
                               alignment=alignment[longest_list_i], canvas_size=canvas_size, save_cert_filepath=True,
                               create_file=True)
        print(f"Saved paths: {[fpath.name for fpath in self.saved_filepaths]}")

        # For each label_list set from the 2nd set upwards add their corresponding labels to the certificate
        for i in range(len(data_list)):
            if i == longest_list_i:
                continue

            print(f"Adding label index {i}")
            data = data_list[i]
            print(f"Adding label index {i}: {data_list[i]}")

            # For each image created in the first iteration add the label to the certificate
            for j in range(len(data)):
                cert_path = self.saved_filepaths[j]
                fname = cert_path.name
                print(f"Adding label: {data[j]} to {fname}")
                self.add_label_to_cert([data[j]], fonts[i], label_positions[i], template=cert_path,
                                       save_folder=save_folder, filename=fname, alignment=alignment[i],
                                       canvas_size=canvas_size,
                                       create_file=False)

    def add_label_to_cert(self, data: list[str] | list[Image],
                          font: FreeTypeFont = ImageFont.truetype(FONT_DIR / "Sans.ttf", 55),
                          cert_pos: QRect = QRect(), template: str | Path = None, save_folder: str = None, filename: str = "",
                          alignment="center", canvas_size=QRect(0, 0, 1037, 801),
                          save_cert_filepath=False, create_file=False):
        if not data or not data[0]:
            print("No data provided. Exiting...")
            return
        if not alignment:
            alignment = "center"

        if not save_folder:
            save_folder = ID_Generator.select_save_folder()
            if save_folder is None:
                print("No folder selected. Exiting...")
                return

        if template is None:
            template = ID_Generator.get_file_location("Template file")
            if not template:
                print("No template selected. Exiting...")
                return

        for name in data:
            # Open an Template Image
            img = Image.open(template)

            # Call draw Method to add 2D graphics in an image
            draw = ImageDraw.Draw(img)

            # Scale font size and text box based on canvas and image size
            font_size, text_box, scaled_rect = self._scale_text_box(font, name, cert_pos, canvas_size)
            _font = ImageFont.truetype(font.path, font_size)
            text_x, text_y, text_w, text_h = text_box

            # Draw rect for debugging
            # rect_textbox = (text_x, text_y, text_x + text_w, text_y + text_h)
            # print(f"Cert_pos {cert_pos} -> Rect: {rect_textbox}")
            # draw.rectangle(rect_textbox, outline=2)
            # draw.rectangle(scaled_rect, outline=2)

            # Add Text to an image

            draw.text((text_x, text_y), name, font=_font, fill=(0, 0, 0), align=alignment)

            # Save the edited image
            if not Path(save_folder).exists():
                Path.mkdir(Path(save_folder), parents=True)

            # Change name characters or pattern to meet structure for file names
            name = re.sub(r'[`\'’<>:,"\\/|?*]', '*', name)
            name = re.sub(r'\*+', lambda m: '_' if len(m.group(0)) == 1 else '__', name)

            if create_file:
                filename = (name + f" {self.id_group}.png").strip()
            if not create_file and not filename:
                print("No filename provided. Exiting...")
                return

            save_path = (Path(save_folder) / filename).resolve()
            img.save(save_path)
            if save_cert_filepath: self.saved_filepaths.append(save_path)

        print(f"Completed generating {len(data)} certificates for {save_folder}")
        # delay one second then open folder
        # time.sleep(1)
        # os.startfile(os.path.join(save_folder, filename))

    def _scale_text_box(self, font: FreeTypeFont, name: str, cert_pos: QRect, canvas_size: QRect, template: str = None,
                        alignment: str = "center"):
        if not template:
            template = self.template
        if not alignment:
            alignment = self.alignment

        # Scale the location based on image built open of canvas size
        img = Image.open(template)
        # TODO: Ensure that canvas ratio matches image ratio to ensure text is on image
        (canvas_width, canvas_height) = canvas_size.width(), canvas_size.height()
        (imgsz_x, imgsz_y) = img.size
        scale_x = imgsz_x / float(canvas_width)
        scale_y = imgsz_y / float(canvas_height)

        # Debugging Scaled text box to match QFont and Pil.Image Size
        # print(f"Image: {imgsz_x}, {imgsz_y}")
        # print(f"Canvas: {canvas_width}, {canvas_height}")
        # print(f"Scale: {scale_x}, {scale_y}")

        # scale the font size
        font_size = int(font.size * scale_y)
        font = ImageFont.truetype(font.path, font_size)
        text_w, text_h = font.font.getsize(name)[0]
        #print(f"Font Size: {font.size}, {font.font.family}, {font.font.height}")

        # scale text box
        top_left = (x0 := cert_pos.x() * scale_x, y0 := cert_pos.y() * scale_y)
        bottom_right = (x1 := cert_pos.bottomRight().x() * scale_x, y1 := cert_pos.bottomRight().y() * scale_y)
        scaled_rect = (top_left, bottom_right)
        scaled_rect_w, scaled_rect_h = x1 - x0, y1 - y0

        # Default text position
        text_x = x0
        text_y = y0
        # Evaluate position of text in textbox
        # print(f"Text position: {text_x}, {text_y}")
        # print(f"Text Length: {text_w}, {text_h}")
        if alignment == "center":
            if scaled_rect_w > text_w:
                text_x = int(x0 + (scaled_rect_w - text_w) / 2)
                text_y = int(y0 + (scaled_rect_h - text_h) / 2)
            else:
                print("Text too long for textbox. Adjusting... Not implemented yet")

        return font.size, (int(text_x), int(text_y), text_w, text_h), scaled_rect


if __name__ == "__main__":
    # Create fake names of characters from movies and cartoons
    lvl1_students = ["Kermit the Frog", "Danny Phantom", "Mickey Mouse"]

    # Create fake names from anime characters
    lvl2_students = ["Shinobu Kocho", "Senku Ishigami", "Shikamaru Nara", "Rika Furude"]

    # Generate Certificates for Level 1 Students
    generator = ID_Generator(data=[lvl1_students, lvl2_students], label_positions=[QRect(230, 330, 992, 407)],
                             fonts=[QFont("Sans", 85), QFont("Sans", 62)], template=IMG_DIR/"_Certificate.png")
    generator.gen_certs(data_list=[lvl1_students, lvl2_students],
                        label_positions=[QRect(230, 220, 402, 107), QRect(96, 430, 402, 107)],
                        template= IMG_DIR / "_Certificate.png",
                        fonts=[QFont("Sans", 45), QFont("Sans", 32)],
                        alignment=["center", "center"],
                        canvas_size=QRect(0, 0, 800, 600),
                        save_folder=BASE_DIR / "Certificates")
    # open the last image generated
    startfile(generator.saved_filepaths[0])
