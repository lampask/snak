from tkinter import Frame, Scrollbar, Listbox, RIGHT, Y, END, BOTH, CENTER, DISABLED
import globals.globals as globals


class Credits(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = 'Credits - The Snak'
        self.job = None

        scrollbar = Scrollbar(self, bg=globals.UI_OUTLINE, troughcolor=globals.BOARD_COLOR)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(self, bg=globals.BOARD_COLOR, fg=globals.UI_OUTLINE, disabledforeground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE)
        listbox.pack(fill=BOTH, expand=1)

        self.startup = lambda: (
            listbox.yview_moveto(0),
            self.after_cancel(self.job) if self.job is not None else '',
            scroll()
        )

        for i in range(30):
            listbox.insert(END, '')

        listbox.insert(END, '   ___ __  __   __  __  __')
        listbox.insert(END, ' /  __|   \\ | | /__\\ | | / /')
        listbox.insert(END, " \\__  \\  .`\\|  / __ \\| ' < ")
        listbox.insert(END, ' |____/__|"\\|_/  \\_\\_|\\_\\')
        listbox.insert(END, '')
        listbox.insert(END, '-=-==-=-')
        listbox.insert(END, '')
        listbox.insert(END, 'Game made by 「Lmpsk」 as a simple')
        listbox.insert(END, 'informatics project')
        listbox.insert(END, '')
        listbox.insert(END, 'Github: lampask')
        listbox.insert(END, 'Twitter: @Lampask_1')
        listbox.insert(END, '')
        listbox.insert(END, 'Thank you for playing ^-^')

        for i in range(3):
            listbox.insert(END, '')

        listbox.config(yscrollcommand=scrollbar.set, justify=CENTER, state=DISABLED)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack_forget()
        listbox.bind("<Button-1>", lambda event: self.controller.show_frame("Startup"))

        def scroll():
            listbox.yview_scroll(1, 'units')
            self.job = self.after("150", scroll)

        scrollbar.pack_forget()
