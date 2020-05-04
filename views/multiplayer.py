from helpers.utils import GameFrame, GameButton

class Multiplayer(GameFrame):

    def __init__(self, parent, controller):
        GameFrame.__init__(self, parent)
        self.controller = controller
        self.title = 'Multiplayer rooms - The Snak'

        create = GameButton(self, text="Create room")
        create.pack()

        join = GameButton(self, text="Join room")
        join.pack()
