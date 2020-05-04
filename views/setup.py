from tkinter import Toplevel, Frame, Entry, colorchooser
from helpers.utils import GameButton, GameLabel, GameFrame, GameEntry
import globals.globals as globals

class Setup(Toplevel):

    def __init__(self, *args, **kw):
        Toplevel.__init__(self)
        container = Frame(self, bg=globals.BOARD_COLOR.get())
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title('Snak Settings')

        self.frames = {}
        for F in (StartPage, ColorPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(GameFrame):

    def __init__(self, parent, controller):
        GameFrame.__init__(self, parent, bg=globals.BOARD_COLOR.get())
        self.controller = controller
        self.controller.title('Snak Settings')

        headline = GameFrame(self)
        headline.pack(side="top", fill="x", pady=10)

        GameLabel(headline, text="Settings", font='Helvetica 12 bold').pack(side="top")

        dimensions = GameFrame(self)
        dimensions.pack(side="top", fill="x", padx=20, pady=3)

        GameLabel(dimensions, text="Width: ").pack(side="left")
        width = GameEntry(dimensions)
        width.insert(0, globals.BOARD_WIDTH)
        width.pack(side="left")

        GameLabel(dimensions, text="Height: ").pack(side="left")
        height = GameEntry(dimensions)
        height.insert(0, globals.BOARD_HEIGHT)
        height.pack(side="left")

        game = GameFrame(self)
        game.pack(side="top", fill="x", padx=20, pady=3)

        GameLabel(game, text="Delay: ").pack(side="left")
        delay = GameEntry(game)
        delay.insert(0, globals.DELAY)
        delay.pack(side="left")

        GameLabel(game, text="Cell size: ").pack(side="left")
        size = GameEntry(game)
        size.insert(0, globals.DOT_SIZE)
        size.pack(side="left")

        more = GameFrame(self)
        more.pack(side="top", fill="x", padx=20, pady=3)

        GameButton(more, text="Change colors", highlightthickness=2, command=lambda: self.controller.show_frame("ColorPage")).pack(side="top")

        apply = GameFrame(self)
        apply.pack(side="top", pady=10)

        GameButton(apply, text="Apply").pack(side="left")
        GameButton(apply, text="Cancel", command=self.controller.destroy).pack(side="left")

class ColorPage(GameFrame):

    def __init__(self, parent, controller):
        GameFrame.__init__(self, parent, bg=globals.BOARD_COLOR.get())
        self.controller = controller

        headline = GameFrame(self)
        headline.pack(side="top", fill="x", pady=10)

        GameLabel(headline, text="Color chooser", font='Helvetica 12 bold').pack(side="top")

        dimensions = GameFrame(self)
        dimensions.pack(side="top", fill="x", padx=20, pady=3)

        GameLabel(dimensions, text="UI Color: ").pack(side="left")
        GameButton(dimensions, background=globals.UI_OUTLINE.get(), update=False, override=globals.UI_OUTLINE,
                   command=lambda: globals.UI_OUTLINE.set(colorchooser.askcolor(globals.UI_OUTLINE.get())[1])).pack(side="left")

        GameLabel(dimensions, text="BG Color: ").pack(side="left")
        GameButton(dimensions, background=globals.BOARD_COLOR.get(), update=False, override=globals.BOARD_COLOR,
                   command=lambda: globals.BOARD_COLOR.set(colorchooser.askcolor(globals.BOARD_COLOR.get())[1])).pack(side="left")

        game = GameFrame(self)
        game.pack(side="top", fill="x", padx=20, pady=3)

        # more

        more = GameFrame(self)
        more.pack(side="top", fill="x", padx=20, pady=3)

        GameButton(more, text="Go back", highlightthickness=2, command=lambda: self.controller.show_frame("StartPage")).pack(side="top")

        apply = GameFrame(self)
        apply.pack(side="top", pady=10)

        GameButton(apply, text="Cancel", command=self.controller.destroy).pack(side="left")
