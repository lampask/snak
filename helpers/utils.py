from PIL import Image, ImageDraw, ImageTk
import globals.globals as globals
from enum import Enum

def rgb2rgbInt(rgb):
    return (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def col(color):
    rgb2rgbInt(color.get_rgb())

CELL_DIMENSIONS = (globals.DOT_SIZE, globals.DOT_SIZE)
CELL_XY_PRESET = (0, 0, globals.DOT_SIZE, globals.DOT_SIZE)

def _Snak_Body():
    image = Image.new('RGB', CELL_DIMENSIONS, col(globals.BOARD_COLOR))
    draw = ImageDraw.Draw(image)
    draw.rectangle(CELL_XY_PRESET, col(globals.SNAK_COLOR), col(globals.SNAK_OUTLINE))
    return image

def _Snak_Head():
    image = Image.new('RGB', CELL_DIMENSIONS, col(globals.BOARD_COLOR))
    draw = ImageDraw.Draw(image)
    draw.rectangle(CELL_XY_PRESET, col(globals.SNAK_COLOR), col(globals.SNAK_OUTLINE), 3)
    return image

def _Snak_Snack():
    image = Image.new('RGB', CELL_DIMENSIONS, col(globals.BOARD_COLOR))
    draw = ImageDraw.Draw(image)
    draw.ellipse(CELL_XY_PRESET, col(globals.SNAK_SNACK_COLOR), col(globals.SNAK_SNACK_OUTLINE))
    return image
    
class Texture(Enum):
    SNAK_BODY = staticmethod(_Snak_Body)
    SNAK_HEAD = staticmethod(_Snak_Head)
    SNAK_SNACK = staticmethod(_Snak_Snack)

    
    
