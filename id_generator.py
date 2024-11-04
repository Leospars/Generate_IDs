import os
import tkinter
from tkinter import filedialog

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont

from lib.configured_log import log as print
from tests.GetFonts import GetFonts

# Create fake names of characters from movies and cartoons
lvl1_students = ["Ron Stoppable", "Kermit the Frog", "Danny Phantom", "Mickey Mouse"]

# Create fake names from anime characters
lvl2_students = ["Shinobu Kocho", "Senku Ishigami", "Shikamaru Nara", "Rika Furude"]

_get_fonts = GetFonts()
_def_font_location = list(filter(lambda font_loc: font_loc.endswith("lucon.ttf"), _get_fonts.system_ttf_fonts))[0]
print(f"Uploaded Fonts: {_def_font_location}")
_default_font = ImageFont.truetype(_def_font_location, 55)
print(f"\nDefault Font: {_default_font.font.family}, {_default_font.font.height}pt")


class ID_Generator:
    def __init__(self, data: list[list], label_positions: list[QRect] = [], template: str = "", save_folder="",
                 font: list[QFont] = [], alignment="center"):

        self.data = data
        self.label_positions = label_positions
        self.template = template
        self.save_folder = save_folder
        if font is None:
            self.fonts = [_default_font]
        else:
            self.fonts = font
        self.alignment = alignment
        self.filenames = []
        self.save_folder = ""

    @staticmethod
    def select_save_folder():
        tk = tkinter.Tk()
        tk.withdraw()
        save_folder = filedialog.askdirectory(title="Save Generated Certificates to", initialdir=os.getcwd())
        if not save_folder:
            print("No folder selected. Exiting...")
            tk.destroy()
            return

        print(f"Save folder: {save_folder}")
        tk.destroy()
        return save_folder

    @staticmethod
    def getFileLocation(title_msg: str):
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
            fonts = [_default_font]
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

        # print adjusted parameters
        print(f"Data: {data_list}\nLabel Positions: {label_positions}\nTemplate: {template}\n"
              f"Save Folder: {save_folder}\nFonts: {[[ttf.font.family, ttf.font.height] for ttf in fonts]}\n"
              f"Alignment: {alignment}")

        self.add_label_to_cert(data_list[0], fonts[0], label_positions[0], template, save_folder,
                               alignment=alignment[0], canvas_size=canvas_size, save_cert_filepath=True,
                               create_file=True)

        print(f"Range: {list(range(1, len(data_list)))}, Length: 1 to {len(data_list)}")
        for i in range(1, len(data_list)):
            # for each image generated in the first iteration, add the label to the certificate
            print(f"Adding label set {i}: {data_list[i]}")
            print(f"Saved paths: {[fname.split("\\")[-1] for fname in self.filenames]}")
            for j in range(len(self.filenames)):
                certificate = self.filenames[j]
                print(f"Adding label to {certificate.split("\\")[-1]}")
                self.add_label_to_cert([data_list[i][j]], fonts[i], label_positions[i], certificate, save_folder,
                                       filename=certificate, alignment=alignment[i], canvas_size=canvas_size,
                                       create_file=False)

    def add_label_to_cert(self, data: list[str] | list[Image],
                          font: FreeTypeFont = ImageFont.truetype("font/Sans.ttf", 55),
                          cert_pos: QRect = QRect(), template: str = None, save_folder: str = None, filename: str = "",
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
            template = ID_Generator.getFileLocation("Template file")
            if not template:
                print("No template selected. Exiting...")
                return

        for name in data:
            # Open an Template Image
            img = Image.open(template)

            # Call draw Method to add 2D graphics in an image
            draw = ImageDraw.Draw(img)

            # Scale the location based on image built open of canvas size
            # TODO: Ensure that canvas ratio matches image ratio to ensure text is on image
            (canvas_x, canvas_y) = canvas_size.width(), canvas_size.height()
            (imgsz_x, imgsz_y) = img.size
            scale_x = imgsz_x / float(canvas_x)
            scale_y = imgsz_y / float(canvas_y)

            # print(f"Image: {imgsz_x}, {imgsz_y}")
            # print(f"Canvas: {canvas_x}, {canvas_y}")
            # print(f"Scale: {scale_x}, {scale_y}")

            # draw a text box transparent background
            top_corner = (x0 := cert_pos.x() * scale_x, y0 := cert_pos.y() * scale_y)
            bottom_corner = (x1 := cert_pos.bottomRight().x() * scale_x, y1 := cert_pos.bottomRight().y() * scale_y)

            rect = [top_corner, bottom_corner]
            width = rect[1][0] - rect[0][0]
            height = rect[1][1] - rect[0][1]
            x = rect[0][0]
            y = rect[0][1]

            # Evaluate position of text in textbox
            if alignment == "center":
                text_x = (x + width / 2) - draw.textlength(name, font=font) / 2
            text_y = (y + height / 2) - draw.textlength("W", font=font) / 2

            # Draw rect for debugging
            print(f"Cert_pos {cert_pos} -> Rect: {rect}")
            draw.rectangle(rect, outline=2)

            # Add Text to an image
            draw.text((text_x, text_y), name, font=font, fill=(0, 0, 0), align="center")

            # Save the edited image
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            # Change name characters or pattern to meet structure for file names
            restrict_char = "`'’"
            print(f"name: {name}")
            for char in restrict_char:
                name = name.replace(char, "_")

            if create_file:
                filename = (name + " Certificate.png").strip()
            if not create_file and not filename:
                print("No filename provided. Exiting...")
                return

            save_path = os.path.abspath(os.path.join(save_folder, filename))
            img.save(save_path)
            if save_cert_filepath: self.filenames.append(save_path)

        print(f"Completed generating {len(data)} certificates for {save_folder}")
        # delay one second then open folder
        # time.sleep(1)
        # os.startfile(os.path.join(save_folder, filename))


if __name__ == "__main__":
    # Generate Certificates for Level 1 Students
    generator = ID_Generator(data=[lvl1_students, lvl2_students], label_positions=[QRect(230, 330, 992, 407)])
    # generator.add_label_to_cert(lvl2_students, font=generator._default_font,
    #                                 cert_pos=QRect(230, 330, 992, 407), template="img/MGI_Blank Lvl2.png")
    # generator.add_label_to_cert(lvl1_students, generator._default_font, 100),
    #                             template="img/MGI_Blank Lvl1.png", cert_pos=QRect(210, 330, 1092, 407))
    generator.gen_certs(data_list=[lvl1_students, lvl2_students],
                        label_positions=[QRect(230, 220, 302, 107), QRect(96, 430, 302, 107)],
                        template="img/MGI_Blank Lvl1.png",
                        fonts=[QFont("Sans", 85), QFont("Sans", 62)],
                        alignment=["center", "center"],
                        canvas_size=QRect(0, 0, 800, 600),
                        save_folder="./Certificates")
    # open the last image generated
    os.startfile(generator.filenames[0])
