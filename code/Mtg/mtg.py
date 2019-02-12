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
import screen_res

pygame.init()
pygame.mixer.init()

(display_width, display_height) = display_size = screen_res.get_screen_res()
gameDisplay = pygame.display.set_mode(display_size)

#takes in dimentions of screen and draws the window
def my_quit():
	pygame.quit()
	quit()

main_menu.game_intro(gameDisplay, display_size)



