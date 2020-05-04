from tkinter import Tk, Frame, Canvas, Button, messagebox, CENTER, N, FLAT, SW, SE
from PIL import ImageTk
import webbrowser

from views.game import Snak
from views.setup import Setup
from views.credits import Credits
from views.stats import Stats
from views.multiplayer import Multiplayer

import globals.globals as globals
import globals.constants as constants

import helpers.utils as utils
from helpers.utils import GameButton, GameFrame, GameCanvas, GameLabel

import logging
import coloredlogs
import gettext
import pickle
import os

# setup localization
_ = gettext.gettext

# setup logger
coloredlogs.install(level='DEBUG')

# Views
game = None
view = None
root = None

settings = None

class Main(Tk):

    def __init__(self, *args, **kw):
        Tk.__init__(self, *args, **kw)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.ontop = None
        self.frames = {}
        for F in (Snak, Multiplayer, Stats, Credits, Startup):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Startup")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.title(frame.title)
        if hasattr(frame, 'startup'):
            frame.startup()
        frame.tkraise()
        self.ontop = page_name

class MenuCanvas(GameCanvas):

    def __init__(self, parent):
        self.controller = parent.controller

        GameCanvas.__init__(self, parent)

        self.initUI()
        self.pack()
        self.vol_checker = False

    def initUI(self):
        self.logo = GameLabel(self, font="Helvetica 20", text=". - --==[ The snak ]==-- - .", anchor=N)
        self.logo_window = self.create_window(globals.BOARD_WIDTH/2, 25, anchor=CENTER, window=self.logo)
        
        self.quick_play = GameButton(self, width=constants.UI_BUTTON_WIDTH, text="Quick play", command=lambda: self.controller.show_frame("Snak"), anchor=CENTER)
        self.qp_window = self.create_window(globals.BOARD_WIDTH/2, 7*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.quick_play)

        self.multiplayer = GameButton(self, width=constants.UI_BUTTON_WIDTH, text="Multiplayer", command=lambda: self.controller.show_frame("Multiplayer"), anchor=CENTER)
        self.mp_window = self.create_window(globals.BOARD_WIDTH/2, 12*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.multiplayer)

        self.stats = GameButton(self, width=constants.UI_BUTTON_WIDTH, text="Stats", command=lambda: self.controller.show_frame("Stats"), anchor=CENTER)
        self.stat_window = self.create_window(globals.BOARD_WIDTH/2, 17*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.stats)

        self.credits = GameButton(self, width=constants.UI_BUTTON_WIDTH, text="Credits", command=lambda: self.controller.show_frame("Credits"), anchor=CENTER)
        self.credits_window = self.create_window(globals.BOARD_WIDTH/2, 22*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.credits)

        self.settings = GameButton(self, width=constants.UI_BUTTON_WIDTH, text="Settings", command=self.sett, anchor=CENTER)
        self.settings_window = self.create_window(globals.BOARD_WIDTH/2, 27*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.settings)

        def set_git(inv=False, event=None):
            self.git_icon = ImageTk.PhotoImage(data=utils.Texture.GITHUB(inv))
            self.github.config(image=self.git_icon)

        self.github = GameButton(self, width=32, height=32, command=lambda: webbrowser.open(constants.GIT_URL), compound=CENTER)
        set_git()
        self.github_window = self.create_window(0, globals.BOARD_HEIGHT-self.github.winfo_width(), anchor=SW, window=self.github)
        self.github.bind("<Enter>", lambda event: set_git(True))
        self.github.bind("<Leave>", lambda event: set_git(False))

        def set_vol(inv=False, event=None):
            self.vol_icon = ImageTk.PhotoImage(data=(utils.Texture.VOLUME_ON(inv) if globals.volume.get() else utils.Texture.VOLUME_OFF(inv)))
            self.volume.config(image=self.vol_icon)

        self.volume = GameButton(self, width=32, height=32, command=self.vol, compound=CENTER)
        set_vol()
        self.volume_window = self.create_window(globals.BOARD_WIDTH-self.volume.winfo_width(),
                                                globals.BOARD_HEIGHT-self.volume.winfo_height(), anchor=SE, window=self.volume)
        self.volume.bind("<Enter>", lambda event: set_vol(True))
        self.volume.bind("<Leave>", lambda event: set_vol(False))

        def resetUI():
            set_git()
            set_vol(self.vol_checker)
            self.vol_checker = False

        globals.events.setting_change += resetUI

    def sett(self):
        global settings
        if settings is None:
            settings = Setup(root)

    def vol(self):
        self.vol_checker = True
        globals.volume.set(not globals.volume.get())

class Startup(GameFrame):

    def __init__(self, parent, controller):
        GameFrame.__init__(self, parent)
        self.controller = controller
        self.title = 'Welcome - The Snak'
        MenuCanvas(self)

def on_closing(controller):
    if controller.ontop == "Snak":
        if globals.gameStatus is globals.GameState.IN_GAME:
            globals.gamePaused = True
            # Wanna leave ongoing game?
            if messagebox.askokcancel("Quit?", "Do you want to quit?"):
                globals.stats['Games_exited'].set(globals.stats['Games_exited'].get()+1)
                globals.stats['Games_played'].set(globals.stats['Games_played'].get()-1)
                controller.show_frame("Startup")
            else:
                globals.gamePaused = False
                root.event_generate('<<Tick>>')
        else:  # After game over
            controller.show_frame("Startup")
    else:
        root.destroy()


def go_back():
    global startup
    game.board.destroy()
    game.destroy()
    globals.gameStatus = globals.GameState.NON

def update_data():
    with open('playerdata/stats.snakdata', 'wb') as handle:
        pickle.dump(globals.stats, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('playerdata/achievements.snakdata', 'wb') as handle:
        pickle.dump(globals.achievements, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    globals.events.data_changed += lambda: update_data()
    try:
        with open('playerdata/stats.snakdata', 'rb') as handle:
            globals.stats = pickle.load(handle)
        with open('playerdata/achievements.snakdata', 'rb') as handle:
            globals.achievements = pickle.load(handle)
    except Exception:
        logging.warn("Cannot load saved playerdata  -  generating new")
        if not os.path.exists("playerdata"):
            os.mkdir("playerdata")
        globals.stats = globals.stats_preset
        globals.achievements = globals.achievements_preset
        update_data()

    for key in globals.stats_preset.keys():
        if key not in globals.stats.keys():
            globals.stats[key] = globals.stats_preset[key]
    for key in globals.achievements_preset.keys():
        if key not in globals.achievements.keys():
            globals.achievements[key] = globals.achievements_preset[key]
    root = Main()
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    logging.info(_("Starting application mainloop."))
    root.mainloop()
