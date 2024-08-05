import os

import PyQt5.QtGui
from PIL import ImageFont, ImageDraw, Image

class GetFonts:
	def __init__(self):
		self.system_ttf_fonts = self.find_all_ttf_fonts()  # List of all ttf fonts files in the system
		self.font_dirmap = self.get_font_dirmap()  # Map all ttf font family to font file location

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

		directories = [fonts_dir, os.path.abspath("./font"),
					   os.path.join(GetFonts.__get_downloads_directory__(), "Fonts")]
		system_ttf_fonts = []
		for _dir in directories:
			if os.path.exists(_dir):
				ttf_fonts = get_ttf_fonts(_dir)
				# Check if all the fonts can be loaded by PIL
				for font_location in ttf_fonts:
					try:
						loaded_font = ImageFont.truetype(font_location)
						system_ttf_fonts.append(font_location)
					except Exception as e:
						print(f"Cannot load {font_location} font")
						ttf_fonts.remove(font_location)
						continue

		return system_ttf_fonts  # List of all ttf fonts in the system

	@staticmethod
	def get_font_dirmap():
		font_dirmap = {}
		all_fonts = GetFonts.find_all_ttf_fonts()
		for font_location in all_fonts:
			try:
				loaded_font = ImageFont.truetype(font_location)
				font_family = loaded_font.getname()[0]
				font_dirmap[font_family] = font_location
			except Exception as e:
				print(f"Cannot load {font_location} font")
				continue
		font_dirmap = dict(sorted(font_dirmap.items()))  # Sort the dictionary by font family
		return font_dirmap

	# Search for the font file in the fonts direct
	def find_ttf_font(self, font_family):
		return self.font_dirmap.get(font_family, None)

	def qFontToPILFont(self, qFont: PyQt5.QtGui.QFont):
		if qFont.family() in self.font_dirmap:
			return ImageFont.truetype(self.font_dirmap[qFont.family()], qFont.pointSize())
		else:
			return None

if __name__ == "__main__":
	font = PyQt5.QtGui.QFont("Lucida Console", 12)
	print(f"Font: {font.family()}, {font.pointSize()}pt")
	gf = GetFonts()

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