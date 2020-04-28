import sys
import random
from PIL import Image, ImageTk
from tkinter import Frame, Canvas, ALL, NW
import utils
import views
import globals

class Board(Canvas):

    def __init__(self):
        super().__init__(width=globals.BOARD_WIDTH, height=globals.BOARD_HEIGHT,
            background="black", highlightthickness=0)
        
        self.bind_all('<<Tick>>', self.tickEvent)
        self.initGame()
        self.pack()


    def initGame(self):
        '''initializes game'''

        self.inGame = True
        self.dots = 3
        self.score = 0

        # variables used to move snake object
        self.moveX = globals.DOT_SIZE
        self.moveY = 0

        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        self.loadImages()

        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(globals.DELAY, self.onTimer)


    def loadImages(self):
        '''loads images from utils or disk'''

        try:
            self.dot = ImageTk.PhotoImage(utils.Texture.SNAK_BODY())
            self.head = ImageTk.PhotoImage(utils.Texture.SNAK_HEAD())
            self.apple = ImageTk.PhotoImage(utils.Texture.SNAK_SNACK())

        except Exception as e:
            
            print(e)
            sys.exit(1)


    def createObjects(self):
        '''creates objects on Canvas'''

        self.create_text(30, 10, text="Score: {0}".format(self.score),
                         tag="score", fill="white")
        self.create_image(self.appleX, self.appleY, image=self.apple,
            anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW,  tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")


    def checkAppleCollision(self):
        '''checks if the head of snake collides with apple'''

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if apple[0] == ovr:

                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locateApple()


    def moveSnake(self):
        '''moves the Snake object'''

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        items = dots + head

        z = 0
        while z < len(items)-1:

            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1

        self.move(head, self.moveX, self.moveY)


    def checkCollisions(self):
        '''checks for collisions'''

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for over in overlap:
                if over == dot:
                  self.inGame = False

        if x1 < 0:
            self.inGame = False

        if x1 > globals.BOARD_WIDTH - globals.DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > globals.BOARD_HEIGHT - globals.DOT_SIZE:
            self.inGame = False


    def locateApple(self):
        '''places the apple object on Canvas'''

        apple = self.find_withtag("apple")
        self.delete(apple[0])

        r = random.randint(0, globals.MAX_RAND_POS)
        self.appleX = r * globals.DOT_SIZE
        r = random.randint(0, globals.MAX_RAND_POS)
        self.appleY = r * globals.DOT_SIZE

        self.create_image(self.appleX, self.appleY, anchor=NW,
            image=self.apple, tag="apple")


    def onKeyPressed(self, e):
        '''controls direction variables with cursor keys'''

        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:

            self.moveX = -globals.DOT_SIZE
            self.moveY = 0

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:

            self.moveX = globals.DOT_SIZE
            self.moveY = 0

        RIGHT_CURSOR_KEY = "Up"
        if key == RIGHT_CURSOR_KEY and self.moveY <= 0:

            self.moveX = 0
            self.moveY = -globals.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:

            self.moveX = 0
            self.moveY = globals.DOT_SIZE


    def onTimer(self):
        '''creates a game cycle each timer event'''

        self.drawScore()
        self.checkCollisions()

        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            if not globals.gamePaused:
                self.event_generate('<<Tick>>')
            else:
                self.create_text(self.winfo_width() /2, self.winfo_height()/2,
            text="Game is Paused", fill=globals.UI_OUTLINE, tag="pause")
        else:
            self.gameOver()

    def tickEvent(self, event):
        for ui in self.find_withtag("pause"):
            self.delete(ui)
        self.after(globals.DELAY, self.onTimer)
    
    def drawScore(self):
        '''draws score'''

        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))


    def gameOver(self):
        '''deletes all objects and draws game over message'''

        globals.gameStatus = globals.GameState.GAME_OVER
        self.delete(ALL)
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,
            text="Game Over with score {0}".format(self.score), fill=globals.UI_OUTLINE)


class Snak(Frame):

    def __init__(self):
        super().__init__()

        self.master.title('The Snak game')
        globals.gameStatus = globals.GameState.IN_GAME
        globals.gamePaused = False
        self.board = Board()
        self.pack()