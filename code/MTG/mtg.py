import sys

sys.path.append('./code')
sys.path.append('./images')
sys.path.append('./personal_decks')
sys.path.append('./sound')
sys.path.append('./testing')

import pygame
import random
import time
import main_menu

pygame.init()
pygame.mixer.init()

display_size = (display_width, display_height)= (1024, 768)
gameDisplay = pygame.display.set_mode(display_size)

#takes in dimentions of screen and draws the window
def my_quit():
	pygame.quit()
	quit()

main_menu.game_intro(gameDisplay, display_size)



