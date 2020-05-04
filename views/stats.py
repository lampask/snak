from tkinter import Scrollbar, Listbox, RIGHT, Y, X, END, BOTH, SINGLE, CENTER
from helpers.utils import GameFrame, GameButton, GameListbox, GameScrollbar
import globals.globals as globals


class Stats(GameFrame):

    def __init__(self, parent, controller):
        GameFrame.__init__(self, parent)
        self.controller = controller
        self.title = 'Game Stats - The Snak'

        self.listbox = GameListbox(self)
        self.listbox.pack(fill=BOTH, expand=1)

        self.startup = lambda: self.listbox.yview_moveto(0)

        scrollbar = GameScrollbar(self.listbox)
        scrollbar.pack(side=RIGHT, fill=Y)

        GameButton(self, text="Back", command=lambda: self.controller.show_frame("Startup")).pack(fill=X)

        self.update()

        self.listbox.config(yscrollcommand=scrollbar.set, justify=CENTER)
        scrollbar.config(command=self.listbox.yview)

        globals.events.data_changed += self.update

    def update(self):
        self.listbox.delete(0, END)
        self.listbox.insert(END, '')
        self.listbox.insert(END, '\\/ -=_=-     Stats     -=_=- \\/')
        self.listbox.insert(END, '')
        for (k, v) in globals.stats.items():
            self.listbox.insert(END, f"{k.replace('_', ' ')}: {v.get()}")
        self.listbox.insert(END, '')
        self.listbox.insert(END, '\\/ -=_=- Achievements -=_=- \\/')
        self.listbox.insert(END, '')
        for (k, v) in globals.achievements.items():
            self.listbox.insert(END, f"{k.replace('_', ' ')}:   {'(Obtained)' if v.get() else '(Not obtained)'}")
