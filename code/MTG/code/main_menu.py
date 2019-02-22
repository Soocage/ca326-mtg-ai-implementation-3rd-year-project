import sys

sys.path.insert(0, '../')
sys.path.insert(0, '../images')

sys.path.append('../personal_decks')
sys.path.append('../sound')
sys.path.append('../testing')

import time
import pygame
from button import Button
import game
import player

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


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Magic The Gathering")
pygame.mixer.music.load('sound/music_1.ogg')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()




def game_intro(gameDisplay, display_size):
    (display_width, display_height) = display_size
    
    logo = pygame.image.load('./images/logo.png')
    logo_width = int(display_width/2)
    logo_height = int(display_height/4)
    logo = pygame.transform.scale(logo, (logo_width, logo_height))

    #button dimentions
    button_width = (display_width/4)
    button_height = (display_height/8)

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


    (display_width, display_height) = display_size 
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

        gameDisplay.fill(bg_colour)
        gameDisplay.blit(logo, ((display_width/2 -(logo_width/2)),(display_height/15)))

        fight_vs_ai = Button("Fight Vs Ai",start_game_button_x, start_game_button_y, button_width, button_height, button_blue, hover_button_blue, "play_vs_ai")

        quit = Button("Quit", exit_game_button_x, exit_game_button_y, button_width, button_height, button_blue, hover_button_blue, "quit")

        option = Button("Option",option_button_x, option_button_y, button_width, button_height, button_blue, hover_button_blue, "options")

        deck_tool = Button("Deck Tools", deck_button_x, deck_button_y, button_width, button_height, button_blue, hover_button_blue, "deck tools")

        login = Button("Login",login_button_x, login_button_y, button_width, button_height, button_blue, hover_button_blue, "login")

        draw_button(fight_vs_ai, display_size, gameDisplay)
        draw_button(quit, display_size, gameDisplay)
        draw_button(option, display_size, gameDisplay)
        draw_button(deck_tool, display_size, gameDisplay)
        draw_button(login, display_size, gameDisplay)

        pygame.display.update()
        clock.tick(60)




def option(gameDisplay, display_size):
    (display_width, display_height) = display_size

    #define option button dimentions
    option_button_width = (display_width/4)
    option_button_height = (display_height/8)

    #option border
    option_box_x = (display_width/6) -10
    option_box_y = (display_height/6)-10
    option_box_h = ((display_height/3)*2)+20
    option_box_w = ((display_width/3)*2)+20

    #option button dimentions
    volume_slider_height = option_box_h /10
    volume_slider_width = option_box_h /10

    plus_button_width = volume_slider_width
    plus_button_height = volume_slider_height

    minus_button_width = volume_slider_width
    minus_button_height = volume_slider_height

    #button orientation in option menu
    volume_button_x = (option_box_x) + option_box_w*(1/20)
    volume_button_y = option_box_y + (option_box_h*(3/6)) - (option_button_height/2)

    change_resolution_button_x = (option_box_x) + option_box_w*(1/20)
    change_resolution_button_y = option_box_y + (option_box_h*(1/6)) - (option_button_height/2)
     
    back_button_x = (display_width/2) - option_button_width/2
    back_button_y = option_box_y + (option_box_h*(5/6)) - (option_button_height/2) 

    volume_slider_x = (option_box_x + option_box_w - (volume_button_x + option_button_width) * 0.5) + (volume_slider_width/2)
    volume_slider_y = volume_button_y  + (option_button_height/2) - (volume_slider_height/2)

    plus_button_x = volume_slider_x + (volume_slider_width)
    plus_button_y = volume_slider_y + (volume_slider_height/2) - (plus_button_height/2)

    minus_button_x = volume_slider_x - minus_button_width
    minus_button_y = volume_slider_y + (volume_slider_height/2) - (minus_button_height/2)


    res_temp = (option_box_x + option_box_w - (change_resolution_button_x + option_button_width + option_box_w*(1/20)))

    res_button_width = res_temp/6
    res_button_height = res_button_width
    res_padding = ((res_temp/6)/6)

    res_1_x = (change_resolution_button_x + option_button_width) + res_padding
    res_1_y = change_resolution_button_y + (option_button_height/2) - (res_button_height/2)

    res_2_x = res_1_x + res_button_width + res_padding
    res_2_y = res_1_y

    res_3_x = res_2_x + res_button_width + res_padding
    res_3_y = res_1_y

    res_4_x = res_3_x + res_button_width + res_padding
    res_4_y = res_1_y

    res_5_x = res_4_x + res_button_width + res_padding
    res_5_y = res_1_y



    time.sleep(1)
    in_option = True
    while in_option:
        (mx, my) = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myquit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    myquit()

        current_vol = str(round(pygame.mixer.music.get_volume(), 1))


        gameDisplay.fill(bg_colour)     

        pygame.draw.rect(gameDisplay, black, (option_box_x, option_box_y, option_box_w, option_box_h))

        pygame.draw.rect(gameDisplay, bright_red, (display_width/6, display_height/6, (display_width/3)*2, (display_height/3)*2))

        
        change_res = Button("Change resolution",change_resolution_button_x, change_resolution_button_y, option_button_width, option_button_height, button_blue, button_blue)

        res_1 = Button("800x600", int(res_1_x), int(res_1_y), res_button_width, res_button_height, grey, white, "change_res")

        res_2 = Button("1024x768", int(res_2_x), int(res_2_y), res_button_width, res_button_height, grey, white, "change_res")

        res_3 = Button("1440x900", int(res_3_x), int(res_3_y),res_button_width, res_button_height, grey, white, "change_res")

        res_4 = Button("1600x900", int(res_4_x), int(res_4_y), res_button_width, res_button_height, grey, white, "change_res")

        res_5 = Button("1920x1080", int(res_5_x), int(res_5_y), res_button_width, res_button_height, grey, white, "change_res")

        
        back = Button("Back", back_button_x, back_button_y, option_button_width, option_button_height, button_blue, hover_button_blue, "back")

                
        volume = Button("Volume", volume_button_x, volume_button_y, option_button_width, option_button_height, button_blue, button_blue)
        
        slider = Button(current_vol, volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height, volume_slider_colour, volume_slider_colour)

        plus = Button("+", plus_button_x, plus_button_y, plus_button_width, plus_button_height, grey, white, "plus")

        minus = Button("-", minus_button_x, minus_button_y, minus_button_width, minus_button_height, grey, white, "minus")

    
        draw_button(change_res, display_size, gameDisplay)
        draw_button(back, display_size, gameDisplay)
        draw_button(volume, display_size, gameDisplay)
        draw_button(slider, display_size, gameDisplay)
        draw_button(plus, display_size, gameDisplay)
        draw_button(minus, display_size, gameDisplay)
        draw_button(res_1, display_size, gameDisplay)
        draw_button(res_2, display_size, gameDisplay)
        draw_button(res_3, display_size, gameDisplay)
        draw_button(res_4, display_size, gameDisplay)
        draw_button(res_5, display_size, gameDisplay)

        pygame.display.update()



def deck_tools(gameDisplay, display_size):
    time.sleep(1)
    (display_width, display_height) = display_size

    #define deck_tools button dimentions
    deck_tools_button_width = ((display_width/4)/2)
    deck_tools_button_height = ((display_height/8)/2)

    #deck_tools border
    deck_tools_box_x = (display_width)*(1/20)
    deck_tools_box_y = (display_height)*(1/20)
    deck_tools_box_h = ((display_height)*(18/20))
    deck_tools_box_w = ((display_width)*(18/20))

    #deck tools button dimentions
    back_button_x = deck_tools_box_x + (deck_tools_box_w / 2) - (deck_tools_button_width / 2)
    back_button_y = deck_tools_box_y + (deck_tools_box_h*(6/7))

    next_button_x = back_button_x + deck_tools_button_width + (deck_tools_button_width/10)
    next_button_y = back_button_y

    previous_button_x = back_button_x - deck_tools_button_width - (deck_tools_button_width/10)
    previous_button_y = back_button_y

    in_deck_tools = True
    while in_deck_tools:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myquit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    myquit()





        pygame.draw.rect(gameDisplay, white, (deck_tools_box_x, deck_tools_box_y, deck_tools_box_w, deck_tools_box_h))

        exit_button = Button("Exit", back_button_x, back_button_y, deck_tools_button_width, deck_tools_button_height, button_blue, hover_button_blue, "back")

        next_button = Button("Next", next_button_x, next_button_y, deck_tools_button_width, deck_tools_button_height, button_blue, hover_button_blue, "next")

        previous_button = Button("Previous", previous_button_x, previous_button_y, deck_tools_button_width, deck_tools_button_height, button_blue, hover_button_blue, "previous")

        draw_button(exit_button, display_size, gameDisplay)
        draw_button(previous_button, display_size, gameDisplay)
        draw_button(next_button, display_size, gameDisplay)
        pygame.display.update()


def my_quit():
    pygame.quit()
    quit()


def draw_button(name, display_size, gameDisplay):
    #list of possible resolutions
    res_list = ["1920x1080", "800x600", "1440x900", "1024x768", "1600x900"]

    #Take in the co-ordinates of the mouse
    mouse = pygame.mouse.get_pos()
    
    #Check what buttons have been pressed by the mouse
    click = pygame.mouse.get_pressed()
    
    #Check if mouse position is within the boundry of the button
    if (name.x + name.w) > mouse[0] > name.x and (name.y + name.h) > mouse[1] > name.y:

        #Highlight the button with a lighter shad of blue
        pygame.draw.rect(gameDisplay, name.a_colour, (name.x, name.y, name.w, name.h))

        if click[0] == 1 and name.action != None:

            if name.action == "play_vs_ai":
                player_1 = player.Player("Sean")
                player_2 = player.Player("AI_Dusty")
                game_1 = game.Game(gameDisplay, display_size, player_1, player_2)
                game_1.run_game()

            elif name.action == "quit":
                my_quit()
            
            elif name.action == "options":
                option(gameDisplay, display_size)

            elif name.action == "back":
                game_intro(gameDisplay, display_size)

            elif name.action == "plus":
                increase_volume()

            elif name.action == "minus":
                decrease_volume()

            elif name.action == "change_res":
                for res in res_list:
                    if name.msg == res:
                        new_res = res.split("x")
                        display_size = (int(new_res[0]) ,int(new_res[1]))
                        pygame.display.set_mode(display_size)
                        option(gameDisplay, display_size)

            elif name.action == "deck tools":
                deck_tools(gameDisplay, display_size)




    #Else we are not over the button so it stays as it is
    else:
        pygame.draw.rect(gameDisplay, name.i_colour, (name.x, name.y, name.w, name.h))

    if  name.msg in res_list:
        smallFont = pygame.font.Font("freesansbold.ttf", int(name.h/7))
        smallText = smallFont.render(name.msg, False, black)
        smallRect = smallText.get_rect()
        smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
        gameDisplay.blit(smallText, smallRect)

    else:
        if name.w > name.h:
            font_size = name.h/4
        else:
            font_size = name.w/4
        smallFont = pygame.font.Font("freesansbold.ttf", int(font_size))
        smallText = smallFont.render(name.msg, False, black)
        smallRect = smallText.get_rect()
        smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
        gameDisplay.blit(smallText, smallRect)


def increase_volume():
    time.sleep(0.2)
    if pygame.mixer.music.get_volume() < 1.0:
        curr_vol = pygame.mixer.music.get_volume()
        curr_vol += 0.1
        pygame.mixer.music.set_volume(curr_vol)

def decrease_volume():
    time.sleep(0.2)
    if pygame.mixer.music.get_volume() > 0:
        curr_vol = pygame.mixer.music.get_volume()
        curr_vol -= 0.1
        pygame.mixer.music.set_volume(curr_vol)

    
