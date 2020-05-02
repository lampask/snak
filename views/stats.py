from tkinter import Frame, Scrollbar, Button, Listbox, RIGHT, Y, X, END, BOTH, FLAT, SINGLE
import globals.globals as globals


class Stats(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = 'Game Stats - The Snak'

        listbox = Listbox(self, bg=globals.BOARD_COLOR, fg=globals.UI_OUTLINE, selectbackground=globals.UI_OUTLINE,
                          selectforeground=globals.BOARD_COLOR, highlightbackground=globals.UI_OUTLINE, selectmode=SINGLE)
        listbox.pack(fill=BOTH, expand=1)

        self.startup = lambda: listbox.yview_moveto(0)

        scrollbar = Scrollbar(listbox, bg=globals.UI_OUTLINE, troughcolor=globals.BOARD_COLOR)
        scrollbar.pack(side=RIGHT, fill=Y)

        button = Button(self, text="Back", command=lambda: self.controller.show_frame("Startup"))
        button.configure(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE,
                         activebackground=globals.UI_OUTLINE, highlightthickness=5, relief=FLAT)
        button.pack(fill=X)

        for i in range(100):
            listbox.insert(END, i)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
