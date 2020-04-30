from colour import Color
from enum import Enum

BOARD_WIDTH = 300
BOARD_HEIGHT = 300

DELAY = 100
DOT_SIZE = 10
MAX_RAND_POS = 27

BOARD_COLOR = Color('#000')
UI_OUTLINE = Color('#067')
SNAK_COLOR = Color('#fff')
SNAK_OUTLINE = Color('#666')
SNAK_SNACK_COLOR = Color('#212121')
SNAK_SNACK_OUTLINE = Color('#232323')

class GameState(Enum):
    NON = 0,
    IN_GAME = 1,
    GAME_OVER = 2

gamePaused = False
gameStatus = GameState.NON