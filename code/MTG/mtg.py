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


#takes in dimentions of screen and draws the window
def my_quit():
	pygame.quit()
	quit()

main_menu.game_intro()



