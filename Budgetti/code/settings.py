import os
from tkinter import Tk

# Fenstergröße
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
ENTRY_WIDTH = 280
ENTRY_HEIGHT = 280
BG_COLOR = "#454545"
MENU_BG_COLOR = "#333333"

# Fonts
HIGHLIGHT_FONT = ("Verdana", 16)
TEXT_FONT = ("Verdana", 12)

MAX_NAME_LENGTH = 45

# Images
PICON_PATH = os.path.join("budgetti", "images", "icon.png")

# Berechne zentrierte Start-Geometry
def get_geometry(master: Tk):
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    placement_x = (screen_width - WINDOW_WIDTH) // 2
    placement_y = (screen_height - WINDOW_HEIGHT) // 2
    return f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{placement_x}+{placement_y}"


