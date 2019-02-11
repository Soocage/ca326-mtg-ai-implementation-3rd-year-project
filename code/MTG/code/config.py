import pygame
import screen_res

pygame.init()

(display_width, display_height) = display_size = screen_res.get_screen_res()
gameDisplay = pygame.display.set_mode(display_size)



#Colours
volume_slider_colour = (125,137,240)

pointer_colour = (255,255,255)

button_blue = (125,137,240)
hover_button_blue = (175, 183, 245)

grey = (205,205,205)
black = (0,0,0)
white = (255,255,255)

dark_red = (200,0,0)
dark_green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

blue = (0,0,255)

bg_color = grey

#button dimentions

button_length = (display_width/4)
button_height = (display_height/8)

volume_slider_length = options_box_w / 1.3
volume_slider_height = options_box_h /20

plus_button_length = options_box_w / 30
plus_button_height = options_box_w / 30

minus_button_length = options_box_w / 30
minus_button_height = options_box_w / 30

pointer_button_length = options_box_w / 28
pointer_button_height = options_box_h / 20


#main menu button positions
start_game_button_x = (display_width/2)- (button_length + (display_width/10))
start_game_button_y = (display_height/2.5)

login_button_x = (display_width/2) + (display_width/10)
login_button_y = (display_height/2.5)

options_button_x = (display_width/2)- (button_length + (display_width/10))
options_button_y = (display_height/3)*1.75

deck_button_x = (display_width/2) + (display_width/10)
deck_button_y = (display_height/3)*1.75

exit_game_button_x = (display_width/2) - (button_length/2)
exit_game_button_y = (display_height/3)*2.25

button orientation in options menu
volume_button_x = (display_width/2 -(button_length + (options_box_w/8)))
volume_button_y = (display_height/3) + (display_height/7)

change_resolution_button_x = (display_width/2)- (button_length + (options_box_w/8))
change_resolution_button_y = (display_height/3) - (display_height/7)

back_button_x = (display_width/2)- (button_length + (options_box_w/8))
back_button_y = (display_height/3) + ((display_height/7)*2)

background_color_button_x  = (display_width/2)- (button_length + (options_box_w/8))
background_color_button_y = (display_height/3)

volume_slider_x = (display_width/2)
volume_slider_y = (display_height/3) + (display_height/7) + (button_height/3)

plus_button_x = (display_width/2) + (volume_slider_length)
plus_button_y = (display_height/3) + (display_height/7) + (volume_slider_height/3) + (button_height/3)

minus_button_x = (display_width/2) - minus_button_length
minus_button_y = (display_height/3) + (display_height/7) +(volume_slider_height/3) + (button_height/3)


POINTER_BUTTON_X = (display_width/2) + (volume_slider_length/2)
POINTER_BUTTON_Y = (display_height/3) + (display_height/7) + (button_height/3)


