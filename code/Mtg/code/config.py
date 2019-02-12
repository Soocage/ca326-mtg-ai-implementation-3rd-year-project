import pygame
import screen_res

pygame.init()

(display_width, display_height) = display_size = screen_res.get_screen_res()
gameDisplay = pygame.display.set_mode(display_size)






#Colours

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

bg_colour = grey

volume_slider_colour = white


#define option button dimentions
option_button_width = (display_width/4)
option_button_height = (display_height/8)

#option border
option_box_x = (display_width/6) -10
option_box_y = (display_height/6)-10
option_box_h = ((display_height/3)*2)+20
option_box_w = ((display_width/3)*2)+20 


#button dimentions
button_width = (display_width/4)
button_height = (display_height/8)

volume_slider_height = option_box_h /10
volume_slider_width = option_box_h /10

plus_button_width = volume_slider_width
plus_button_height = volume_slider_height

minus_button_width = volume_slider_width
minus_button_height = volume_slider_height

pointer_button_width = option_box_w / 28
pointer_button_height = option_box_h / 20

res_button_width = option_box_h / 7
res_button_height = option_box_h / 7


#main menu button positions
start_game_button_x = (display_width/2)- (button_width + (display_width/10))
start_game_button_y = (display_height/2.5)

login_button_x = (display_width/2) + (display_width/10)
login_button_y = (display_height/2.5)

option_button_x = (display_width/2)- (button_width + (display_width/10))
option_button_y = (display_height/3)*1.75

deck_button_x = (display_width/2) + (display_width/10)
deck_button_y = (display_height/3)*1.75

exit_game_button_x = (display_width/2) - (button_width/2)
exit_game_button_y = (display_height/3)*2.25


#button orientation in option menu
volume_button_x = (option_box_x) + option_box_w*(1/20)
volume_button_y = option_box_y + (option_box_h*(3/6)) - (option_button_height/2)

change_resolution_button_x = (option_box_x) + option_box_w*(1/20)
change_resolution_button_y = option_box_y + (option_box_h*(1/6)) - (option_button_height/2)
 
back_button_x = (display_width/2) - button_width/2
back_button_y = option_box_y + (option_box_h*(5/6)) - (option_button_height/2) 

volume_slider_x = (option_box_x + option_box_w - (volume_button_x + option_button_width) * 0.5) + (volume_slider_width/2)
volume_slider_y = volume_button_y  + (option_button_height/2) - (volume_slider_height/2)

plus_button_x = volume_slider_x + (volume_slider_width)
plus_button_y = volume_slider_y + (volume_slider_height/2) - (plus_button_height/2)

minus_button_x = volume_slider_x - minus_button_width
minus_button_y = volume_slider_y + (volume_slider_height/2) - (minus_button_height/2)

POINTER_BUTTON_X = (display_width/2) + (volume_slider_width/2)
POINTER_BUTTON_Y = (display_height/3) + (display_height/7) + (button_height/3)

res_1_x = change_resolution_button_x + option_button_width + res_button_width/2
res_1_y = change_resolution_button_y

res_2_x = res_1_x + res_button_width + res_button_width/10
res_2_y = change_resolution_button_y

res_3_x = res_2_x + res_button_width + res_button_width/10
res_3_y = change_resolution_button_y

res_4_x = res_3_x + res_button_width + res_button_width/10
res_4_y = change_resolution_button_y

res_5_x = res_4_x + res_button_width + res_button_width/10
res_5_y = change_resolution_button_y




