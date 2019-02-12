import time
import pygame
from config import *
from button import Button



def options(gameDisplay):
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





        pygame.display.update()

def draw_button(name):
	#Take in the co-ordinates of the mouse
	mouse = pygame.mouse.get_pos()
	
	#Check what buttons have been pressed by the mouse
	click = pygame.mouse.get_pressed()
	
	#Check if mouse position is within the boundry of the button
	if (name.x + name.w) > mouse[0] > name.x and (name.y + name.h) > mouse[1] > name.y:

		#Highlight the button with a lighter shad of blue
		pygame.draw.rect(gameDisplay, name.a_colour, (name.x, name.y, name.w, name.h))

		if click[0] == 1 and action != None:

			if action == "play vs ai":
				game.play_vs_ai()

			if action == "Quit":
				my_quit()
			
			if action == "Options":
				options_menu.options(gameDisplay)
				


	#Else we are not over the button so it stays as it is
	else:
		pygame.draw.rect(gameDisplay, name.i_colour, (name.x, name.y, name.w, name.h))
	
	smallFont = pygame.font.Font("freesansbold.ttf", int(name.h/2))
	smallText = smallFont.render(name.msg, False, black)
	smallRect = smallText.get_rect()
	smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
	gameDisplay.blit(smallText, smallRect)
