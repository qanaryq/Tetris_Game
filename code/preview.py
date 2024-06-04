from settings import * 
from pygame.image import load
from os import path
import os

class Preview:
	def __init__(self, block_settings):
		
		# general
		self.display_surface = pygame.display.get_surface()
		self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
		self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING,PADDING))

		# shapes
		script_path = os.path.abspath(__file__).split('\\')[:-1]
		script_path = '\\'.join(script_path)
		self.shape_surfaces = {}
		self.block_settings = block_settings
		for shape in list(list(self.block_settings.CURRENT_TETROMINOS.keys()) + list(self.block_settings.EXTRA_TETROMINOS.keys())):
                        full_path = path.join(script_path, '..','graphics',f'{shape}.png')
                        self.shape_surfaces.update({shape: load(full_path).convert_alpha()})
                        
		# image position data
		self.increment_height = self.surface.get_height() / 3

	def display_pieces(self, shapes):
		for i, shape in enumerate(shapes):
			shape_surface = self.shape_surfaces[shape]
			x = self.surface.get_width() / 2
			y = self.increment_height / 2 + i * self.increment_height
			rect = shape_surface.get_rect(center = (x,y))
			self.surface.blit(shape_surface,rect)

	def run(self, next_shapes):
		self.surface.fill(GRAY)
		self.display_pieces(next_shapes)
		self.display_surface.blit(self.surface, self.rect)
		pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
