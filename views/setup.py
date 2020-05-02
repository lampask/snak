from tkinter import Toplevel, Frame, Button, Label

class Setup(Toplevel):

    def __init__(self, *args, **kw):
        Toplevel.__init__(self)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, NextPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title('Snak Settings')
        label = Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to Page One",
                         command=lambda: controller.show_frame("NextPage"))
        button2 = Button(self, text="Go to Page Two",
                         command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()

class NextPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is the next page")
        label.pack(side="top", fill="x", pady=10)
