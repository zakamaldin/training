import os
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import filedialog
import pygame
import time
import threading
import pickle

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(PROJECT_DIR, "icons")
PROGRAM_NAME = 'My Drum Machine'

MAX_NUMBER_OF_PATTERNS = 10
MAX_NUMBER_OF_DRUM_SAMPLES = 5
MAX_NUMBER_OF_UNITS = 5
MAX_BPU = 5
MAX_BEATS_PER_MINUTE = 300
INITIAL_NUMBER_OF_UNITS = 4
INITIAL_BPU = 4
INITIAL_BEATS_PER_MINUTE = 240
COLOR_1 = 'grey55'
COLOR_2 = 'khaki'
BUTTON_CLICKED_COLOR = 'green'


# получаем словарь вида {"название изображения":изображение}
def icons_image():
    icons = {}
    images = os.listdir(IMAGE_DIR)
    for image in images:
        icons[os.path.splitext(image)[0]] = PhotoImage(file=os.path.abspath(os.path.join(IMAGE_DIR, image)))
    return icons



