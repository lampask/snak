from tkinter import Tk, Frame, Canvas, Button, CENTER, NW, FLAT, messagebox
from views.game import Snak
from views.setup import Setup
import globals

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
        self.quick_play = Button(self, text="Quick play", command=self.play, anchor=CENTER)
        self.quick_play.configure(width = 10, background=globals.BOARD_COLOR, foreground=globals.UI_OUTLINE, highlightthickness=5, relief = FLAT)
        self.qp_window = self.create_window(10, 10, anchor=NW, window=self.quick_play)
    
    def play(self):
        global game
        game = Snak()  
        self.destroy()  

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