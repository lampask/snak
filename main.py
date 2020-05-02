from tkinter import Tk, Frame, Canvas, Button, CENTER, N, FLAT, SW, SE, DISABLED
from PIL import ImageTk
import webbrowser
from views.game import Snak
from views.setup import Setup
from views.credits import Credits
from views.stats import Stats
import globals.globals as globals
import globals.constants as constants
import helpers.utils as utils
import logging
import coloredlogs
import gettext

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

class MenuCanvas(Canvas):

    def __init__(self, parent):
        self.controller = parent.controller

        Canvas.__init__(self, master=parent, width=globals.BOARD_WIDTH, height=globals.BOARD_HEIGHT,
                        background=globals.BOARD_COLOR, highlightthickness=0)

        self.initUI()
        self.pack()
        self.vol_checker = False

    def initUI(self):
        self.logo = self.create_text(globals.BOARD_WIDTH/2, 10, fill=globals.UI_OUTLINE, font="Helvetica 20", text=". - --==[ The snak ]==-- - .", anchor=N)

        self.quick_play = Button(self, text="Quick play", command=lambda: self.controller.show_frame("Snak"), anchor=CENTER)
        self.quick_play.configure(width=constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                                  highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.qp_window = self.create_window(globals.BOARD_WIDTH/2, 7*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.quick_play)

        self.multiplayer = Button(self, text="Multiplayer", command=lambda: self.controller.show_frame("Multiplayer"), anchor=CENTER, state=DISABLED)
        self.multiplayer.configure(width=constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                                   highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.mp_window = self.create_window(globals.BOARD_WIDTH/2, 12*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.multiplayer)

        self.stats = Button(self, text="Stats", command=lambda: self.controller.show_frame("Stats"), anchor=CENTER)
        self.stats.configure(width=constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                             highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.stat_window = self.create_window(globals.BOARD_WIDTH/2, 17*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.stats)

        self.credits = Button(self, text="Credits", command=lambda: self.controller.show_frame("Credits"), anchor=CENTER)
        self.credits.configure(width=constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                               highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.credits_window = self.create_window(globals.BOARD_WIDTH/2, 22*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.credits)

        self.settings = Button(self, text="Settings", command=self.sett, anchor=CENTER)
        self.settings.configure(width=constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                                highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.settings_window = self.create_window(globals.BOARD_WIDTH/2, 27*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.settings)

        def set_git(inv=False, event=None):
            self.git_icon = ImageTk.PhotoImage(data=utils.Texture.GITHUB(inv))
            self.github.config(image=self.git_icon)

        self.github = Button(self, width=32, height=32, command=lambda: webbrowser.open(constants.GIT_URL), compound=CENTER)
        set_git()
        self.github.configure(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE,
                              activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.github_window = self.create_window(0, globals.BOARD_HEIGHT-self.github.winfo_width(), anchor=SW, window=self.github)
        self.github.bind("<Enter>", lambda event: set_git(True))
        self.github.bind("<Leave>", lambda event: set_git(False))

        def set_vol(inv=False, event=None):
            self.vol_icon = ImageTk.PhotoImage(data=(utils.Texture.VOLUME_ON(inv) if globals.volume.get() else utils.Texture.VOLUME_OFF(inv)))
            self.volume.config(image=self.vol_icon)

        self.volume = Button(self, width=32, height=32, command=self.vol, compound=CENTER)
        set_vol()
        self.volume.configure(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE,
                              activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        self.volume_window = self.create_window(globals.BOARD_WIDTH-self.volume.winfo_width(),
                                                globals.BOARD_HEIGHT-self.volume.winfo_height(), anchor=SE, window=self.volume)
        self.volume.bind("<Enter>", lambda event: set_vol(True))
        self.volume.bind("<Leave>", lambda event: set_vol(False))

        def resetUI():
            self.github.winfo_pointerxy
            set_git()
            set_vol(self.vol_checker)
            self.vol_checker = False
            self.github.config(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                               highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE)
            self.volume.config(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE,
                               highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE)

        globals.events.setting_change += resetUI

    def sett(self):
        global settings
        if settings is None:
            settings = Setup(root)

    def vol(self):
        self.vol_checker = True
        globals.volume.set(not globals.volume.get())

class Startup(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = 'Welcome - The Snak'
        MenuCanvas(self)

class Multiplayer(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = 'Multiplayer rooms - The Snak'

def on_closing():
    """ if globals.gameStatus is not globals.GameState.NON:
        if globals.gameStatus is globals.GameState.IN_GAME:
            globals.gamePaused = True
            # Wanna leave ongoing game?
            if messagebox.askokcancel("Quit?", "Do you want to quit?"):
                go_back()
            else:
                globals.gamePaused = False
                root.event_generate('<<Tick>>')
        else: # After game over
            go_back()
    else:"""
    root.destroy()


def go_back():
    global startup
    game.board.destroy()
    game.destroy()
    globals.gameStatus = globals.GameState.NON


if __name__ == '__main__':
    root = Main()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    logging.info(_("Starting application mainloop."))
    root.mainloop()
