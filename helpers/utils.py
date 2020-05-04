from tkinter import Button, Label, Frame, Canvas, Entry, Listbox, Scrollbar
from PIL import Image, ImageDraw
import globals.globals as globals
import cairosvg
from enum import Enum
from colour import Color

def rgb2rgbInt(rgb):
    return (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def col(color):
    rgb2rgbInt(Color(color).get_rgb())


CELL_DIMENSIONS = (globals.DOT_SIZE, globals.DOT_SIZE)
CELL_XY_PRESET = (0, 0, globals.DOT_SIZE, globals.DOT_SIZE)

def _Snak_Body():
    image = Image.new('RGB', CELL_DIMENSIONS, col(globals.BOARD_COLOR.get()))
    draw = ImageDraw.Draw(image)
    draw.rectangle(CELL_XY_PRESET, col(globals.SNAK_COLOR), col(globals.SNAK_OUTLINE))
    return image

def _Snak_Head():
    image = Image.new('RGB', CELL_DIMENSIONS, col(globals.BOARD_COLOR.get()))
    draw = ImageDraw.Draw(image)
    draw.rectangle(CELL_XY_PRESET, col(globals.SNAK_COLOR), col(globals.SNAK_OUTLINE), 3)
    return image

def _Snak_Snack():
    image = Image.new('RGB', CELL_DIMENSIONS, col(globals.BOARD_COLOR.get()))
    draw = ImageDraw.Draw(image)
    draw.ellipse(CELL_XY_PRESET, col(globals.SNAK_SNACK_COLOR), col(globals.SNAK_SNACK_OUTLINE))
    return image

def _Github_Icon(inverted=False):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" enable-background="new 0 0 50 50">
                <path fill-rule="evenodd" clip-rule="evenodd" fill="{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()}" d="M25 10c-8.3 0-15 6.7-15 15 0 6.6 4.3 12.2 10.3 14.2.8.1 1-.3 1-.7v-2.6c-4.2.9-5.1-2-5.1-2-.7-1.7-1.7-2.2-1.7-2.2-1.4-.9.1-.9.1-.9 1.5.1 2.3 1.5 2.3 1.5 1.3 2.3 3.5 1.6 4.4 1.2.1-1 .5-1.6 1-2-3.3-.4-6.8-1.7-6.8-7.4 0-1.6.6-3 1.5-4-.2-.4-.7-1.9.1-4 0 0 1.3-.4 4.1 1.5 1.2-.3 2.5-.5 3.8-.5 1.3 0 2.6.2 3.8.5 2.9-1.9 4.1-1.5 4.1-1.5.8 2.1.3 3.6.1 4 1 1 1.5 2.4 1.5 4 0 5.8-3.5 7-6.8 7.4.5.5 1 1.4 1 2.8v4.1c0 .4.3.9 1 .7 6-2 10.2-7.6 10.2-14.2C40 16.7 33.3 10 25 10z"/>
            </svg>"""
    item = cairosvg.svg2png(bytestring=bytes(svg, "UTF-8"), parent_width=32, parent_height=32)
    return item

def _Volume_On_Icon(inverted=False):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75 75" enable-background="new 0 0 75 75">
                <path d="M39.389,13.769 L22.235,28.606 L6,28.606 L6,47.699 L21.989,47.699 L39.389,62.75 L39.389,13.769z" style="stroke:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};stroke-width:5;stroke-linejoin:round;fill:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};"/>
                <path d="M48,27.6a19.5,19.5 0 0 1 0,21.4M55.1,20.5a30,30 0 0 1 0,35.6M61.6,14a38.8,38.8 0 0 1 0,48.6" style="fill:none;stroke:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};stroke-width:5;stroke-linecap:round"/>
            </svg>"""
    item = cairosvg.svg2png(bytestring=bytes(svg, "UTF-8"), parent_width=20, parent_height=20)
    return item

# <polygon points="39.389,13.769 22.235,28.606 6,28.606 6,47.699 21.989,47.699 39.389,62.75 39.389,13.769" style="stroke:#111111;stroke-width:5;stroke-linejoin:round;fill:#111111;"/>
def _Volume_Off_Icon(inverted=False):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75 75" enable-background="new 0 0 75 75">
                <path d="M39.389,13.769 L22.235,28.606 L6,28.606 L6,47.699 L21.989,47.699 L39.389,62.75 L39.389,13.769z" style="stroke:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};stroke-width:5;stroke-linejoin:round;fill:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};"/>
                <path d="M 48.651772,50.269646 69.395223,25.971024" style="fill:none;stroke:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};stroke-width:5;stroke-linecap:round"/>
                <path d="M 69.395223,50.269646 48.651772,25.971024" style="fill:none;stroke:{globals.BOARD_COLOR.get() if inverted else globals.UI_OUTLINE.get()};stroke-width:5;stroke-linecap:round"/>
            </svg>"""
    item = cairosvg.svg2png(bytestring=bytes(svg, "UTF-8"), parent_width=20, parent_height=20)
    return item

class Texture(Enum):
    SNAK_BODY = staticmethod(_Snak_Body)
    SNAK_HEAD = staticmethod(_Snak_Head)
    SNAK_SNACK = staticmethod(_Snak_Snack)
    GITHUB = staticmethod(_Github_Icon)
    VOLUME_ON = staticmethod(_Volume_On_Icon)
    VOLUME_OFF = staticmethod(_Volume_Off_Icon)

class GameButton(Button):

    def __init__(self, master, highlightthickness=5, bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(),
                 highlightbackground=globals.UI_OUTLINE.get(), activebackground=globals.UI_OUTLINE.get(), update=True, override=None,
                 relief="flat", *args, **kwargs):
        Button.__init__(self, master, highlightthickness=highlightthickness, bg=bg, fg=fg,
                        highlightbackground=highlightbackground, activebackground=activebackground,
                        relief=relief, *args, **kwargs)
        if update:
            globals.events.setting_change += lambda: self.config(bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(),
                                                                 highlightbackground=globals.UI_OUTLINE.get(), activebackground=globals.UI_OUTLINE.get())
        else:
            globals.events.setting_change += lambda: self.config(bg=override.get(), fg=globals.UI_OUTLINE.get(),
                                                                 highlightbackground=globals.UI_OUTLINE.get(), activebackground=globals.UI_OUTLINE.get())
class GameLabel(Label):

    def __init__(self, master, bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(), *args, **kwargs):
        Label.__init__(self, master, bg=bg, fg=fg, *args, **kwargs)
        globals.events.setting_change += lambda: self.config(bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get())

class GameFrame(Frame):

    def __init__(self, master, bg=globals.BOARD_COLOR.get(), *args, **kwargs):
        Frame.__init__(self, master, bg=bg, *args, **kwargs)
        globals.events.setting_change += lambda: self.config(bg=globals.BOARD_COLOR.get())

class GameCanvas(Canvas):

    def __init__(self, master, width=globals.BOARD_WIDTH, height=globals.BOARD_HEIGHT,
                 bg=globals.BOARD_COLOR.get(), highlightthickness=0, *args, **kwargs):
        Canvas.__init__(self, master, width=width, height=height, bg=bg, highlightthickness=highlightthickness, *args, **kwargs)
        globals.events.setting_change += lambda: self.config(width=globals.BOARD_WIDTH, height=globals.BOARD_HEIGHT,
                                                             bg=globals.BOARD_COLOR.get(), highlightthickness=0)

class GameEntry(Entry):

    def __init__(self, master, width=4, bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(), insertbackground=globals.UI_OUTLINE.get(),
                 highlightbackground=globals.UI_OUTLINE.get(), highlightcolor=globals.UI_OUTLINE.get(), *args, **kwargs):
        Entry.__init__(self, master, width=width, bg=bg, fg=fg, insertbackground=insertbackground,
                       highlightbackground=highlightbackground, highlightcolor=highlightcolor, *args, *kwargs)
        globals.events.setting_change += lambda: self.config(width=4, bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(),
                                                             insertbackground=globals.UI_OUTLINE.get(), highlightbackground=globals.UI_OUTLINE.get(),
                                                             highlightcolor=globals.UI_OUTLINE.get())

class GameListbox(Listbox):

    def __init__(self, master, bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(), selectbackground=globals.UI_OUTLINE.get(),
                 selectforeground=globals.BOARD_COLOR.get(), disabledforeground=globals.UI_OUTLINE.get(), highlightbackground=globals.UI_OUTLINE.get(),
                 selectmode="single", *args, **kwargs):
        Listbox.__init__(self, master, bg=bg, fg=fg, selectbackground=selectbackground, selectforeground=selectforeground,
                         highlightbackground=highlightbackground, disabledforeground=disabledforeground, selectmode=selectmode, *args, *kwargs)
        globals.events.setting_change += lambda: self.config(bg=globals.BOARD_COLOR.get(), fg=globals.UI_OUTLINE.get(),
                                                             selectbackground=globals.UI_OUTLINE.get(), selectforeground=globals.BOARD_COLOR.get(),
                                                             highlightbackground=globals.UI_OUTLINE.get(), disabledforeground=globals.UI_OUTLINE.get(),
                                                             selectmode="single")
class GameScrollbar(Scrollbar):

    def __init__(self, master, bg=globals.UI_OUTLINE.get(), troughcolor=globals.BOARD_COLOR.get(), *args, **kwargs):
        Scrollbar.__init__(self, master, bg=bg, troughcolor=troughcolor, *args, **kwargs)
        globals.events.setting_change += lambda: self.config(bg=globals.UI_OUTLINE.get(), troughcolor=globals.BOARD_COLOR.get())
