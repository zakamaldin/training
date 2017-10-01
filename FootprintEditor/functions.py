import os.path
from tkinter import PhotoImage
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(PROJECT_DIR, "icons")
PROGRAM_NAME = " Footprint Editor "


# получаем словарь вида {"название изображения":изображение}
def icons_image():
	icons = {}
	images = os.listdir(IMAGE_DIR)
	for image in images:
		icons[os.path.splitext(image)[0]] = PhotoImage(file=os.path.abspath(os.path.join(IMAGE_DIR, image)))
	return icons



