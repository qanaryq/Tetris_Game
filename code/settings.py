import pygame

# Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# side_ bar size
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# game behaviour
UPDATE_START_SPEED = 200
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# Colors
THISTLE = '#d8bfd8'
DARK_SALMON = '#e9967a'
CADET_BLUE = '#5f9ea0'
ROSY_BROWN = '#bc8f8f'
DARK_KHAKI = '#bdb76b'
FIREBRICK = '#b22222'
PALE_GOLDENROD = '#eee8aa'
GRAY = '#696969'
LINE_COLOR = '#000000'

CYAN = '#00FFFF'

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}

class BLOCK_SETTINGS:
	def __init__(self):
		# shapes
		self.TETROMINOS = {
			'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': THISTLE},
			'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': DARK_SALMON},
			'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': CADET_BLUE},
			'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ROSY_BROWN},
			'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': DARK_KHAKI},
			'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': FIREBRICK},
			'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': PALE_GOLDENROD}
		}

		self.EXTRA_TETROMINOS = {
			'+': {'shape': [(0, 0), (1, 0), (0, 1), (0, -1), (-1, 0)], 'color': CYAN}
		}

		self.CURRENT_TETROMINOS = {
		}

		self.CURRENT_EXTRA_TETROMINOS = {
		}

		self.reset()
		return

	def reset(self):
		self.CURRENT_TETROMINOS = self.TETROMINOS.copy()
		self.CURRENT_EXTRA_TETROMINOS = self.EXTRA_TETROMINOS.copy()

	def shift_to_current(self, key):
		value = self.CURRENT_EXTRA_TETROMINOS[key]
		self.CURRENT_TETROMINOS.update({key: value})
		del self.CURRENT_EXTRA_TETROMINOS[key]