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
from screen_res import screen_res
import ai
import pickle

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

PAGE_COUNTER = 0


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Magic The Gathering")
pygame.mixer.music.load('sound/music_1.ogg')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

player_1_d_path = "./personal_decks/deck_1"
player_2_d_path = "./personal_decks/deck_1"


def game_intro():

    (screen_res.display_width, screen_res.display_height) = screen_res.display_size

    logo = pygame.image.load('./images/logo.png')
    logo_width = int(screen_res.display_width/2)
    logo_height = int(screen_res.display_height/4)
    logo = pygame.transform.scale(logo, (logo_width, logo_height))

    #button dimentions
    button_width = (screen_res.display_width/4)
    button_height = (screen_res.display_height/8)
    padding_h = button_height*(0.20)

    #main menu button positions
    start_game_button_x = (screen_res.display_width/2)- (button_width/2)
    start_game_button_y = (screen_res.display_height/2.5)

    option_button_x = (screen_res.display_width/2) - (button_width/2)
    option_button_y = start_game_button_y + button_height + padding_h

    deck_button_x = (screen_res.display_width/2) - (button_width/2)
    deck_button_y = option_button_y + button_height + padding_h

    exit_game_button_x = (screen_res.display_width/2) - (button_width/2)
    exit_game_button_y = deck_button_y + button_height + padding_h
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

        screen_res.gameDisplay.fill(bg_colour)
        screen_res.gameDisplay.blit(logo, ((screen_res.display_width/2 -(logo_width/2)),(screen_res.display_height/15)))

        fight_vs_ai = Button("Fight Vs Ai",start_game_button_x, start_game_button_y, button_width, button_height, button_blue, hover_button_blue, "play_vs_ai")

        quit = Button("Quit", exit_game_button_x, exit_game_button_y, button_width, button_height, button_blue, hover_button_blue, "quit")

        option = Button("Option",option_button_x, option_button_y, button_width, button_height, button_blue, hover_button_blue, "options")

        deck_tool = Button("Deck Tools", deck_button_x, deck_button_y, button_width, button_height, button_blue, hover_button_blue, "deck tools")



        draw_button(fight_vs_ai)
        draw_button(quit)
        draw_button(option)
        draw_button(deck_tool)

        pygame.display.update()
        clock.tick(60)




def option():
    (screen_res.display_width, screen_res.display_height) = screen_res.display_size

    #define option button dimentions
    option_button_width = (screen_res.display_width/4)
    option_button_height = (screen_res.display_height/8)

    #option border
    option_box_x = (screen_res.display_width/6) -10
    option_box_y = (screen_res.display_height/6)-10
    option_box_h = ((screen_res.display_height/3)*2)+20
    option_box_w = ((screen_res.display_width/3)*2)+20

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

    back_button_x = (screen_res.display_width/2) - option_button_width/2
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


        screen_res.gameDisplay.fill(bg_colour)

        pygame.draw.rect(screen_res.gameDisplay, black, (option_box_x, option_box_y, option_box_w, option_box_h))

        pygame.draw.rect(screen_res.gameDisplay, bright_red, (screen_res.display_width/6, screen_res.display_height/6, (screen_res.display_width/3)*2, (screen_res.display_height/3)*2))


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


        draw_button(change_res)
        draw_button(back)
        draw_button(volume)
        draw_button(slider)
        draw_button(plus)
        draw_button(minus)
        draw_button(res_2)
        draw_button(res_3)
        draw_button(res_4)
        draw_button(res_5)

        pygame.display.update()



def deck_tools():
    time.sleep(1)
    (screen_res.display_width, screen_res.display_height) = screen_res.display_size

    #define deck_tools button dimentions
    deck_tools_button_width = ((screen_res.display_width/4)/2)
    deck_tools_button_height = ((screen_res.display_height/8)/2)

    #deck_tools border
    deck_tools_box_x = (screen_res.display_width)*(1/20)
    deck_tools_box_h = ((screen_res.display_height)*(0.75))
    deck_tools_box_y =  (screen_res.display_height/2) - (deck_tools_box_h/2)
    deck_tools_box_w = ((screen_res.display_width)*(18/20))

    #deck tools button dimentions
    padding_w = (deck_tools_box_w/6)/6

    green_button_1_x = deck_tools_box_x + (deck_tools_box_w/2) - (deck_tools_button_width/2) - padding_w - deck_tools_button_width - padding_w - deck_tools_button_width
    green_button_1_y = (deck_tools_box_y) + (deck_tools_box_h*0.35) - (deck_tools_button_height/2)

    red_button_1_x = green_button_1_x + padding_w + deck_tools_button_width
    red_button_1_y = green_button_1_y

    blue_button_1_x = red_button_1_x + padding_w + deck_tools_button_width
    blue_button_1_y = red_button_1_y

    white_button_1_x = blue_button_1_x + padding_w + deck_tools_button_width
    white_button_1_y = blue_button_1_y

    black_button_1_x = white_button_1_x + padding_w + deck_tools_button_width
    black_button_1_y = white_button_1_y

    green_button_2_x = green_button_1_x
    green_button_2_y = (deck_tools_box_y) + (deck_tools_box_h*0.75) - (deck_tools_button_height/2)

    red_button_2_x = green_button_2_x + padding_w + deck_tools_button_width
    red_button_2_y = green_button_2_y

    blue_button_2_x = red_button_2_x + padding_w + deck_tools_button_width
    blue_button_2_y = red_button_2_y

    white_button_2_x = blue_button_2_x + padding_w + deck_tools_button_width
    white_button_2_y = blue_button_2_y

    black_button_2_x = white_button_2_x + padding_w + deck_tools_button_width
    black_button_2_y = white_button_2_y

    back_button_x = deck_tools_box_x + (deck_tools_box_w / 2) - (deck_tools_button_width / 2)
    back_button_y = deck_tools_box_y + (deck_tools_box_h*(6/7))

    creature_list = []
    land_list = []
    sorcery_list = []
    instant_list = []

    f = open("./personal_decks/deck_info", "rb")
    n = pickle.load(f)
    card_deck = []
    for i in range(n):
        ver = pickle.load(f)
        if ver.card_type == "Creature":
            creature_list.append(ver)
        elif ver.card_type == "Land":
            land_list.append(ver)
        elif ver.card_type == "Sorcery":
            sorcery_list.append(ver)
        elif ver.card_type == "instant":
            instant_list.append(ver)

    print(land_list)
    print("#####")
    print(creature_list)
    print("#####")
    print(sorcery_list)
    print("#####")
    print(instant_list)
    print("#####")



    in_deck_tools = True
    while in_deck_tools:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myquit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    myquit()


        pygame.draw.rect(screen_res.gameDisplay, white, (deck_tools_box_x, deck_tools_box_y, deck_tools_box_w, deck_tools_box_h))

        green_button_1 = Button("Green Deck", green_button_1_x, green_button_1_y, deck_tools_button_width, deck_tools_button_height, (138,186,54), (173,232,72), "green_deck_1")
        green_button_2 = Button("Green Deck", green_button_2_x, green_button_2_y, deck_tools_button_width, deck_tools_button_height, (138,186,54), (173,232,72), "green_deck_2")
        red_button_1 = Button("Red Deck", red_button_1_x, red_button_1_y, deck_tools_button_width, deck_tools_button_height, (199,50,50), (250,74,74), "red_deck_1")
        red_button_2 = Button("Red Deck", red_button_2_x, red_button_2_y, deck_tools_button_width, deck_tools_button_height, (199,50,50), (250,74,74), "red_deck_2")
        blue_button_1 = Button("Blue Deck", blue_button_1_x, blue_button_1_y, deck_tools_button_width, deck_tools_button_height, (65,165,195), (98,204,236), "blue_deck_1")
        blue_button_2 = Button("Blue Deck", blue_button_2_x, blue_button_2_y, deck_tools_button_width, deck_tools_button_height, (65,165,195), (98,204,236), "blue_deck_2")
        white_button_1 = Button("White Deck", white_button_1_x, white_button_1_y, deck_tools_button_width, deck_tools_button_height, (236,243,141), (254,255,223), "white_deck_1")
        white_button_2 = Button("White Deck", white_button_2_x, white_button_2_y, deck_tools_button_width, deck_tools_button_height, (236,243,141), (254,255,223), "white_deck_2")
        black_button_1 = Button("Black Deck", black_button_1_x, black_button_1_y, deck_tools_button_width, deck_tools_button_height, (171,104,239), (210,182,238), "black_deck_1")
        black_button_2 = Button("Black Deck", black_button_2_x, black_button_2_y, deck_tools_button_width, deck_tools_button_height, (171,104,239), (214,182,238), "black_deck_2")
        exit_button = Button("Exit", back_button_x, back_button_y, deck_tools_button_width, deck_tools_button_height, button_blue, hover_button_blue, "back")

        draw_button(green_button_1)
        draw_button(green_button_2)
        draw_button(red_button_1)
        draw_button(red_button_2)
        draw_button(blue_button_1)
        draw_button(blue_button_2)
        draw_button(white_button_1)
        draw_button(white_button_2)
        draw_button(black_button_1)
        draw_button(black_button_2)
        draw_button(exit_button)

        font = pygame.font.Font("freesansbold.ttf", int(deck_tools_button_height))

        text_1 = font.render("Choose Player 1 Deck", True, black)
        rect_1 = text_1.get_rect()
        rect_1.center = (screen_res.display_width/2, (deck_tools_box_y) + (deck_tools_box_h*0.20))
        screen_res.gameDisplay.blit(text_1, rect_1)

        text_2 = font.render("Choose Player 2 Deck", True, black)
        rect_2 = text_2.get_rect()
        rect_2.center = (screen_res.display_width/2, (deck_tools_box_y) + (deck_tools_box_h*0.60))
        screen_res.gameDisplay.blit(text_2, rect_2)

        pygame.display.update()


def my_quit():
    pygame.quit()
    quit()


def draw_button(name):
    #list of possible resolutions
    res_list = ["1920x1080", "800x600", "1440x900", "1024x768", "1600x900"]

    #Take in the co-ordinates of the mouse
    mouse = pygame.mouse.get_pos()

    #Check what buttons have been pressed by the mouse
    click = pygame.mouse.get_pressed()

    #Check if mouse position is within the boundry of the button
    if (name.x + name.w) > mouse[0] > name.x and (name.y + name.h) > mouse[1] > name.y:

        #Highlight the button with a lighter shad of blue
        pygame.draw.rect(screen_res.gameDisplay, name.a_colour, (name.x, name.y, name.w, name.h))

        if click[0] == 1 and name.action != None:
            global player_1_d_path
            global player_2_d_path
            if name.action == "play_vs_ai":
                player_1 = player.Player("Sean")

                ai_mode = "red"
                if player_2_d_path == "./personal_decks/deck_1":
                    ai_mode = "red"
                elif player_2_d_path == "./personal_decks/deck_2":
                    ai_mode = "black"
                elif player_2_d_path == "./personal_decks/deck_3":
                    ai_mode == "green"
                elif player_2_d_path == "./personal_decks/deck_4":
                    ai_mode == "white"
                elif player_2_d_path == "./personal_decks/deck_5":
                    ai_mode == "blue"


                player_2 = ai.Ai("AI_Dusty", ai_mode)
                game_1 = game.Game(player_1, player_2, player_1_d_path, player_2_d_path)
                game_1.run_game(player_1_d_path, player_2_d_path)
                game_intro()

            elif name.action == "quit":
                my_quit()

            elif name.action == "options":
                option()

            elif name.action == "back":
                game_intro()

            elif name.action == "plus":
                increase_volume()

            elif name.action == "minus":
                decrease_volume()

            elif name.action == "change_res":
                for res in res_list:
                    if name.msg == res:
                        new_res = res.split("x")
                        screen_res.display_size = (int(new_res[0]) ,int(new_res[1]))
                        pygame.display.set_mode(screen_res.display_size)
                        option()

            elif name.action == "deck tools":
                deck_tools()

            elif name.action == "green_deck_1":
                player_1_d_path = "./personal_decks/deck_3"

            elif name.action == "green_deck_2":
                player_2_d_path = "./personal_decks/deck_3"

            elif name.action == "red_deck_1":
                player_1_d_path = "./personal_decks/deck_1"

            elif name.action == "red_deck_2":
                player_2_d_path = "./personal_decks/deck_1"

            elif name.action == "blue_deck_1":
                player_1_d_path = "./personal_decks/deck_5"

            elif name.action == "blue_deck_2":
                player_2_d_path = "./personal_decks/deck_5"

            elif name.action == "white_deck_1":
                player_1_d_path = "./personal_decks/deck_4"

            elif name.action == "white_deck_2":
                player_2_d_path= "./personal_decks/deck_4"

            elif name.action == "black_deck_1":
                player_1_d_path = "./personal_decks/deck_2"

            elif name.action == "black_deck_2":
                player_2_d_path = "./personal_decks/deck_2"



    #Else we are not over the button so it stays as it is
    else:
        pygame.draw.rect(screen_res.gameDisplay, name.i_colour, (name.x, name.y, name.w, name.h))

    if  name.msg in res_list:
        smallFont = pygame.font.Font("freesansbold.ttf", int(name.h/7))
        smallText = smallFont.render(name.msg, True, black)
        smallRect = smallText.get_rect()
        smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
        screen_res.gameDisplay.blit(smallText, smallRect)

    else:
        if name.w > name.h:
            font_size = name.h/4
        else:
            font_size = name.w/4
        smallFont = pygame.font.Font("freesansbold.ttf", int(font_size))
        smallText = smallFont.render(name.msg, True, black)
        smallRect = smallText.get_rect()
        smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
        screen_res.gameDisplay.blit(smallText, smallRect)


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
