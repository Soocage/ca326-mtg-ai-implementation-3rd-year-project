import pygame
pygame.init()

class ScreenRes():
	def __init__(self, display_size, gameDisplay):
		self.display_size = display_size
		self.display_height = self.display_size[1]
		self.display_width = self.display_size[0]
		self.gameDisplay = gameDisplay


#screen_res = ScreenRes((1600, 900), pygame.display.set_mode((1600, 900)))
screen_res = ScreenRes((1024, 768), pygame.display.set_mode((1024, 768)))
