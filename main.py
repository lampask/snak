from tkinter import Tk, Frame, Canvas, Button, CENTER, N, FLAT, messagebox, SW, SE
from views.game import Snak
from views.setup import Setup
import globals.globals as globals
import globals.constants as constants

# Views
game = None
startup = None
root = None

class OptionsBoard(Canvas):
    
    def __init__(self):
        super().__init__(width=globals.BOARD_WIDTH, height=globals.BOARD_HEIGHT,
            background=globals.BOARD_COLOR, highlightthickness=0)

        self.initUI()
        self.pack()
    
    def initUI(self):
        
        self.logo = self.create_text(globals.BOARD_WIDTH/2, 10,fill=globals.UI_OUTLINE,font="Helvetica 20", text=". - --==[ The snak ]==-- - .", anchor=N)
        
        self.quick_play = Button(self, text="Quick play", command=self.play, anchor=CENTER)
        self.quick_play.configure(width = constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.qp_window = self.create_window(globals.BOARD_WIDTH/2, 7*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.quick_play)     
        
        self.multiplayer = Button(self, text="Multiplayer", command=self.sett, anchor=CENTER)
        self.multiplayer.configure(width = constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.mp_window = self.create_window(globals.BOARD_WIDTH/2, 12*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.multiplayer)
        
        self.stats = Button(self, text="Stats", command=self.sett, anchor=CENTER)
        self.stats.configure(width = constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.stat_window = self.create_window(globals.BOARD_WIDTH/2, 17*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.stats)   

        self.credits = Button(self, text="Credits", command=self.sett, anchor=CENTER)
        self.credits.configure(width = constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.credits_window = self.create_window(globals.BOARD_WIDTH/2, 22*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.credits)
        
        self.settings = Button(self, text="Settings", command=self.sett, anchor=CENTER)
        self.settings.configure(width = constants.UI_BUTTON_WIDTH, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.settings_window = self.create_window(globals.BOARD_WIDTH/2, 27*constants.UI_BUTTON_WIDTH, anchor=CENTER, window=self.settings)
    
        self.github = Button(self, text="S", command=self.sett, anchor=SW)
        self.github.configure(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.github_window = self.create_window(0,globals.BOARD_HEIGHT-self.github.winfo_width(), anchor=SW, window=self.github)

        self.volume = Button(self, text="V", command=self.sett, anchor=SE)
        self.volume.configure(background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightbackground=globals.UI_OUTLINE, activebackground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.volume_window = self.create_window(globals.BOARD_WIDTH-self.volume.winfo_width(),globals.BOARD_HEIGHT-self.volume.winfo_height(), anchor=SE, window=self.volume)
    
    def play(self):
        global game
        game = Snak()  
        self.destroy()  

    def sett(self):
        pass
class Startup(Frame):
    
    def __init__(self):
        super().__init__()

        self.master.title('Welcome - The Snak')
        self.board = OptionsBoard()
        self.pack()

def on_closing():
    if globals.gameStatus is not globals.GameState.NON:
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
    else:
        root.destroy()
        

def go_back():
    global startup
    game.board.destroy()
    game.destroy()
    globals.gameStatus = globals.GameState.NON
    startup = Startup()

def main():
    global root, startup
    root = Tk()
    startup = Startup()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()