import os
import time
from PIL import Image, ImageDraw, ImageFont
import PyQt5.QtWidgets as Qtw

# Create fake names of charcters from movies and cartoons
lvl1_students = [ "Sherice Marytal", "Mirabell Madrigal", "Jazmine Topples", "Mary Poppins", "Kim Possible",
                  "Ron Stoppable", "Kermit the Frog", "Danny Phantom", "Mickey Mouse"]

# Create fake names from anime characters
lvl2_students = ["Eren Yeager", "Armin Arlert", "Edward Elric", "Riza Hawkeye", "Killua Zoldyck", "Gon Freecss",
                 "Phosphophyllite", "Shinobu Kocho", "Senku Ishigami", "Shikamaru Nara", "Rika Furude", "Yami Sukehiro",
                 "Seras Victoria", "Gintoki Sakata", "Misa Amane", "L Lawliet", "Fuhrer King Bradley", "Shinra Kusakabe",
                 "Ritsu Kageyama", "Hinata Shoyo"]

class ID_Generator:
    def __init__(self, data=[lvl1_students, lvl2_students], dataBoxPosition=[], template="", font_size="", alignment=""):
        self.data = data
        self.dataBoxPosition = dataBoxPosition
        self.template = template
        self.font_size = font_size
        self.alignment = alignment

    # declare variable for handling paths
    abspath = lambda path: os.path.abspath(path)
    relpath = lambda path: os.path.relpath(path)

    def generate_cert(
            data_list,
            save_folder="",
            template="L1 Blank Certificate.png",
            cfont=ImageFont.truetype("./font/Sans.ttf", 55),
            align="center",
    ):
        if not save_folder:
            tk.Tk().withdraw()
            save_folder = filedialog.askdirectory(title="Save Generated Certificates to", initialdir=os.getcwd())
            if not save_folder:
                print("No folder selected. Exiting...")
                return

            save_folder = filedialog.askdirectory(
                title="Save Generated Certificates to ", initialdir=os.getcwd()
            )

            print(f"Save folder: {save_folder}")
            tk.destroy()

        if save_folder == "":
            print("No folder selected. Exiting...")
            return

        if template == "":
            # Get folder location
            import tkinter as tk
            from tkinter import filedialog

            tk = tk.Tk()
            tk.withdraw()

            template = tk.filedialog.askopenfile(title="Template file")
            print(f"template location : {template}")
            tk.destroy()

        filename = ""
        for name in data_list:
            # Open an Template Image
            img = Image.open(template)

            # Call draw Method to add 2D graphics in an image
            draw = ImageDraw.Draw(img)

            # Scale the location based on image built open of size (1037, 801)
            (imgsz_x, imgsz_y) = img.size
            scale_x = imgsz_x / 1037
            scale_y = imgsz_y / 801

            # draw a text box transparent background
            rect = [(230 * scale_x, 330 * scale_y), (992 * scale_x, 407 * scale_y)]
            # draw.rectangle(rect, fill=None, outline=2)
            width = rect[1][0] - rect[0][0]
            height = rect[1][1] - rect[0][1]
            x = rect[0][0]
            y = rect[0][1]

            # Evaluate position of text in textbox
            if align == "center":
                text_x = (x + width / 2) - draw.textlength(name, font=cfont) / 2
                text_y = (y + height / 2) - draw.textlength("W", font=cfont) / 2

            # Add Text to an image
            draw.text((text_x, text_y), name, font=cfont, fill=(0, 0, 0), align="center")

            # Save the edited image
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            # Change name characters or pattern to meet structure nsfor file names
            restrict_char = "`'’"
            print(f"name: {name}")
            for char in restrict_char:
                name = name.replace(char, "_")

            filename = name + " Certificate.png"
            save_path = abspath(os.path.join(save_folder, filename))
            img.save(save_path)

        print(f"Completed generating {len(lvl1_students)} certificates for {save_folder}")
        # delay one second then open folder
        time.sleep(1)
        os.startfile(os.path.join(save_folder, filename))

if __name__ == "__main__":
    # Generate Certificates for Level 1 Students
    generate_cert(lvl1_students, template="MGI_Blank Lvl1.png", cfont=ImageFont.truetype("./font/Sans.ttf", 115))
    generate_cert(lvl2_students, template="MGI_Blank Lvl2.png", cfont=ImageFont.truetype("./font/Sans.ttf", 115))