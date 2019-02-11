import time
import pygame
import screen_res
import game
from config import *

pygame.init()
pygame.mixer.init()

class Button():

	def __init__ (self, msg, x, y, w, h, i_colour, a_colour, action = None):
		self.msg = msg
		self.x = int(x)
		self.y = int(y)
		self.w = int(w)
		self.h = int(h)
		self.i_colour = i_colour
		self.a_colour = a_colour
		self.action = action


