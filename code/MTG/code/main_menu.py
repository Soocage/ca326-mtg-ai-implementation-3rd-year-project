import sys

sys.path.insert(0, '../')
sys.path.insert(0, '../images')
sys.path.append('../personal_decks')
sys.path.append('../sound')
sys.path.append('../testing')

import time
import pygame
import screen_res
from config import *
from button import Button

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Magic The Gathering")
clock = pygame.time.Clock()

(display_width, display_height) = display_size = screen_res.get_screen_res()
gameDisplay = pygame.display.set_mode(display_size)

logo = pygame.image.load('./images/logo.png')
logo_width = int(display_width/2)
logo_height = int(display_height/4)
logo = pygame.transform.scale(logo, (logo_width, logo_height))

def game_intro():
	time.sleep(1)

	in_intro = True
	while in_intro:

		(mx, my) = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				my_quit()
			
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					my_quit()

		gameDisplay.fill(bg_color)
		gameDisplay.blit(logo, ((display_width/2 -(logo_width/2)),(display_height/15)))

		fight_vs_ai = Button("Fight Vs Ai",start_game_button_x, start_game_button_y, button_length, button_height, button_blue, hover_button_blue, "play_vs_ai")

		quit = Button("Quit", exit_game_button_x, exit_game_button_y, button_length, button_height, button_blue, hover_button_blue, "quit")

		options = Button("Options",options_button_x, options_button_y, button_length, button_height, button_blue, hover_button_blue, "options")

		deck_tool = Button("Deck Tools", deck_button_x, deck_button_y, button_length, button_height, button_blue, hover_button_blue, "deck_tools")

		login = Button("Login",login_button_x, login_button_y, button_length, button_height, button_blue, hover_button_blue, "login")

		draw_button(fight_vs_ai)
		draw_button(quit)
		draw_button(options)
		draw_button(deck_tool)
		draw_button(login)

		pygame.display.update()
		clock.tick(60)




def options():
    time.sleep(1)
    in_options = True
    while in_options:
        (mx, my) = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myquit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    myquit()



        gameDisplay.fill(bg_color)     
        pygame.draw.rect(gameDisplay, black, (options_box_x, options_box_y, options_box_h, options_box_w))
        pygame.draw.rect(gameDisplay, bright_red, (display_width/6, display_height/6, (display_width/3)*2, (display_height/3)*2))

        
        chnage_res = Button("Change resolution",change_resolution_button_x, change_resolution_button_y, option_button_length, option_button_height, button_blue, button_blue)

        
        back = Button("Back", back_button_x, back_button_y, option_button_length, option_button_height, button_blue, hover_button_blue, "back")

                
        volume = Button("Volume", volume_button_x, volume_button_y, option_button_length, option_button_height, button_blue, button_blue)
        
        slider = Button("slider", volume_slider_x, volume_slider_y, volume_slider_length, volume_slider_height, volume_slider_color, volume_slider_color)

        plus = Button("+", plus_button_x, plus_button_y, plus_button_length, plus_button_height, button_blue, hover_button_blue, "plus")

        minus = Button("-", minus_button_x, minus_button_y, minus_button_length, minus_button_height, button_blue, hover_button_blue, "minus")

        pointer = Button(str(5), POINTER_BUTTON_X, POINTER_BUTTON_Y, pointer_button_length, pointer_button_height, pointer_color, pointer_color,)
        
        bg_colour_button = Button("Background color",background_color_button_x, background_color_button_y, option_button_length, option_button_height, button_blue, hover_button_blue)
    
        draw_button(change_res)
        draw_button(back)
        draw_button(volume)
        draw_button(slider)
        draw_button(plus)
        draw_button(minus)
        draw_button(pointer)
        draw_button(bg_colour_button)











def my_quit():
	pygame.quit()
	quit()


def draw_button(name):
	#Take in the co-ordinates of the mouse
	mouse = pygame.mouse.get_pos()
	
	#Check what buttons have been pressed by the mouse
	click = pygame.mouse.get_pressed()
	
	#Check if mouse position is within the boundry of the button
	if (name.x + name.w) > mouse[0] > name.x and (name.y + name.h) > mouse[1] > name.y:

		#Highlight the button with a lighter shad of blue
		pygame.draw.rect(gameDisplay, name.a_colour, (name.x, name.y, name.w, name.h))

		if click[0] == 1 and name.action != None:

			if name.action == "play vs ai":
				game.play_vs_ai()

			if name.action == "Quit":
				my_quit()
			
			if name.action == "Options":
				options()
				


	#Else we are not over the button so it stays as it is
	else:
		pygame.draw.rect(gameDisplay, name.i_colour, (name.x, name.y, name.w, name.h))
	
	smallFont = pygame.font.Font("freesansbold.ttf", int(name.h/2))
	smallText = smallFont.render(name.msg, False, black)
	smallRect = smallText.get_rect()
	smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
	gameDisplay.blit(smallText, smallRect)