import pygame
import re
import time
import copy
import random
from button import Button

import player
import pickle
import deck

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
PLAYER_1_HAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_2_HAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_1_LAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_2_LAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_1_SEARCH_SPRITES = pygame.sprite.Group()
PLAYER_2_SEARCH_SPRITES = pygame.sprite.Group()
VIEWED_CARD = pygame.sprite.Group()





WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

button_blue = (125,137,240)
hover_button_blue = (175, 183, 245)
grey = (205,205,205)
dark_red = (200,0,0)
dark_green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
bg_colour = grey
volume_slider_colour = WHITE

class CardSprite(pygame.sprite.Sprite):
    # sprite class for all teh cards
    def __init__(self, card, x, y, w, h, back_texture = None):
            pygame.sprite.Sprite.__init__(self)
            if back_texture == None:
                card_texture = pygame.image.load("."+ card.texture)
            else:
                card_texture = pygame.image.load(back_texture)
            self.image = pygame.transform.smoothscale(card_texture,(int(w), int(h)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False
            self.card = card
            self.viewed = False


class BoardSection():

    def __init__(self, screen, x, y, w, h, colour, is_border=True):
        self.screen = screen
        self.colour = colour
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.is_border = is_border
        self.border_size = int(screen.get_width()*0.002)

    def draw(self):
        if self.is_border:
            pygame.draw.rect(self.screen, (0,0,0), [self.x, self.y, self.w , self.h])
            pygame.draw.rect(self.screen, self.colour, [self.x + self.border_size, self.y + self.border_size, self.w - (2*self.border_size), self.h - (2* self.border_size)])
        
        else:
            pygame.draw.rect(self.screen, self.colour, [self.x, self.y, self.w, self.h])


class PhaseSection(BoardSection):
    def __init__(self, screen, x, y, w, h, colour, is_border=True, active = False):
        BoardSection.__init__(self, screen, x, y, w, h, colour, is_border=True)
        self.active = active
        if self.active == True:
            self.colour = (175,123,188)


class Board():

    def __init__(self, display, display_size, player_1, player_2):
        self.display = display
        self.display_size = display_size
        self.display_w = self.display_size[0]
        self.display_h = self.display_size[1]
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_hand_box = None
        self.player_2_hand_box = None
        self.player_1_land_box = None
        self.player_2_land_box = None
        self.player_1_graveyard = None
        self.player_2_graveyard = None
        self.player_1_battlefield_box = None
        self.player_2_battlefield_box = None
        self.player_1_deck = None
        self.player_2_deck = None
        self.player_1_life_sec = None
        self.player_2_life_sec = None

        self.menu_box_sec = None
        self.player_hand_sec = None
        self.phase_box_sec = None
        self.info_box_sec = None
        self.player_1_play_sec = None
        self.player_2_play_sec = None
        self.player_1_land_sec = None
        self.player_2_land_sec = None
        self.player_1_battlefield_sec = None
        self.player_2_battlefield_sec = None
        self.player_1_mana_box_r = None
        self.player_2_mana_box_r = None
        self.player_1_player_sec = None
        self.player_2_player_sec = None
        self.player_1_name_sec = None
        self.player_2_name_sec = None
        self.card_display_sec = None
        self.concede_button_sec = None
        self.options_button_sec = None 
        self.in_options = True

    def draw_hand(self, player):
        cards = player.hand
        for card in cards:
            if player == self.player_1:
                PLAYER_1_HAND_SPRITE_CARD_GROUP.empty()
                if len(cards) <= 8:
                    padding_w = (self.player_hand_sec.w/8)/8
                    ##card_w = (card_h*63)/88
                    card_w = self.player_hand_sec.w/8
                    card_h = card_w* (88/63)
                else:
                    padding_w = (self.player_hand_sec.w/(len(cards)+1))/(len(cards)+2)
                    card_w = (self.player_hand_sec.w/(len(cards)+1))
                    card_h = card_w * (88/63)

                temp_sprite_list = []
                i = 0
                while i < len(cards):
                    if i == 0:
                        x = (self.player_hand_sec.x + (self.player_hand_sec.w/2)) - ((len(cards)-1)*(padding_w/2)) - ((len(cards)-1)*(card_w/2)) - (card_w/2)
                    else:
                        x = temp_sprite_list[i-1].rect.x + card_w + padding_w
                    y = self.player_hand_sec.y + (self.player_hand_sec.h - (card_h*(13/20)))
                    card_sprite = CardSprite(cards[i] , x, y, card_w, card_h)
                    temp_sprite_list.append(card_sprite)
                    PLAYER_1_HAND_SPRITE_CARD_GROUP.add(card_sprite)
                    i += 1
                PLAYER_1_HAND_SPRITE_CARD_GROUP.draw(self.display)
            else:
                PLAYER_2_HAND_SPRITE_CARD_GROUP.empty()
                if len(cards) <= 8:
                    padding_w = (self.player_hand_sec.w/8)/8
                    card_h = (self.player_hand_sec.h/10)*8
                    card_w = (card_h*63)/88
                    i = 0
                    while i < len(cards):
                        x = self.player_2_hand_box.x + (padding_w*(i+1)) + (card_w*(i))
                        y = self.player_2_hand_box.y + (self.player_2_hand_box.h - card_h)/2
                        card_sprite = CardSprite(cards[i], x, y, card_w, card_h, "./images/cardback.jpg")
                        PLAYER_2_HAND_SPRITE_CARD_GROUP.add(card_sprite)
                        i += 1
                PLAYER_2_HAND_SPRITE_CARD_GROUP.draw(self.display)


    def draw_land(self, player):
        lands = player.land_zone

        if player == self.player_1:
            PLAYER_1_LAND_SPRITE_CARD_GROUP.empty()
            if len(lands) <= 15:
                padding_w = (self.player_1_land_box.w/16)/16
                card_h = (self.player_1_land_box.h/10)*8
                card_w = (card_h*63)/88
            else:
                padding_w = (self.player_1_land_box.w/(len(lands)+1))/(len(lands)+2)
                card_w = (self.player_1_land_box.w/(len(lands)+1))
                card_h = card_w * (88/63)

            temp_sprite_list = []
            i = 0
            while i < len(lands):
                if i == 0:
                    x = (self.display_size[0]/2) - ((len(lands)-1)*(padding_w/2)) - ((len(lands)-1)*(card_w/2)) - (card_w/2)
                else:
                    x = temp_sprite_list[i-1].rect.x + card_w + padding_w
                y = self.player_1_land_box.y + (self.player_1_land_box.h - card_h)/2
                land_sprite = CardSprite(lands[i], x, y, card_w, card_h)
                temp_sprite_list.append(land_sprite)
                if lands[i].tapped == True:
                    land_sprite.image = pygame.transform.rotate(land_sprite.image, 90)
                PLAYER_1_LAND_SPRITE_CARD_GROUP.add(land_sprite)
                i += 1
            PLAYER_1_LAND_SPRITE_CARD_GROUP.draw(self.display)
        else:
            PLAYER_2_LAND_SPRITE_CARD_GROUP.empty()
            if len(lands) <= 15:
                padding_w = (self.player_2_land_box.w/16)/16
                card_h = (self.player_2_land_box.h/10)*8
                card_w = (card_h*63)/88
            else:
                padding_w = (self.player_2_land_box.w/(len(lands)+1))/(len(lands)+2)
                card_w = (self.player_2_land_box.w/(len(lands)+1))
                card_h = card_w * (88/63)
            i = 0
            while i < len(lands):
                x = self.player_2_land_box.x + (padding_w*(i+1)) + (card_w*(i))
                y = self.player_2_land_box.y + (self.player_2_land_box.h - card_h)/2
                land_sprite = CardSprite(lands[i], x, y, card_w, card_h)
                if lands[i].tapped == True:
                    land_sprite.image = pygame.transform.rotate(land_sprite.image, 90)
                PLAYER_2_LAND_SPRITE_CARD_GROUP.add(land_sprite)
                i += 1
            PLAYER_2_LAND_SPRITE_CARD_GROUP.draw(self.display)

    def draw_new_battlefield(self, player):
        battlefield_cards = player.battlefield
        if player == self.player_1:
            PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP.empty()
            if len(battlefield_cards) <= 20:
                padding_w = (self.player_1_battlefield_box.w/16)/16
                card_h = (self.player_1_battlefield_box.h/10)*7
                card_w = (card_h*63)/88
            else:
                padding_w = (self.player_1_battlefield_box.w/(len(battlefield_cards)+1))/(len(battlefield_cards)+2)
                card_w = (self.player_1_battlefield_box.w/(len(battlefield_cards)+1))
                card_h = card_w * (88/63)

            temp_sprite_list = []
            i = 0
            while i < len(battlefield_cards):
                if i == 0:
                    x = (self.display_size[0]/2) - ((len(battlefield_cards)-1)*(padding_w/2)) - ((len(battlefield_cards)-1)*(card_w/2)) - (card_w/2)
                else:
                    x = temp_sprite_list[i-1].rect.x + card_w + padding_w
                y = self.player_1_battlefield_box.y + (self.player_1_battlefield_box.h/20)
                battlefield_card_sprite = CardSprite(battlefield_cards[i], x, y, card_w, card_h)
                temp_sprite_list.append(battlefield_card_sprite)
                PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP.add(battlefield_card_sprite)
                i += 1
            PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP.draw(self.display)
        else:
            PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP.empty()
            if len(battlefield_cards) <= 20:
                padding_w = (self.player_2_battlefield_box.w/16)/16
                card_h = (self.player_2_battlefield_box.h/10)*8
                card_w = (card_h*63)/88
            else:
                padding_w = (self.player_2_battlefield_box.w/(len(battlefield_cards)+1))/(len(battlefield_cards)+2)
                card_w = (self.player_2_battlefield_box.w/(len(battlefield_cards)+1))
                card_h = card_w * (88/63)
            i = 0
            while i < len(battlefield_cards):
                x = self.player_2_battlefield_box.x + (padding_w*(i+1)) + (card_w*(i))
                y = self.player_2_battlefield_box.y + (self.player_2_battlefield_box.h - card_h)/2
                battlefield_card_sprite = CardSprite(battlefield_cards[i], x, y, card_w, card_h)
                PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP.add(battlefield_card_sprite)
                i += 1
            PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP.draw(self.display)

    def draw_search_land(self, player):
        LAND_CARD_SPRITE_GROUP = pygame.sprite.Group()
        pygame.mouse.set_visible(True)
        (display_width, display_height) = self.display_size


        #draw_search border
        draw_search_box_x = (display_width)*(1/20)
        draw_search_box_y = (display_height)*(1/20)
        draw_search_box_h = ((display_height)*(18/20))
        draw_search_box_w = ((display_width)*(18/20))

        padding_w = (draw_search_box_w/11)/11
        upper_padding_h = (draw_search_box_h/7)/7
        card_h = (draw_search_box_h/7)
        card_w = card_h*(63/88)

        in_draw_search = True
        land_cards = []
        for card in player.deck.cards:
            if card.card_type == "Land":
                land_cards.append(card)

        pygame.draw.rect(self.display, (255,255,255), (draw_search_box_x, draw_search_box_y, draw_search_box_w, draw_search_box_h))

        row_1 = []
        row_2 = []
        row_3 = []
        row_4 = []
        row_5 = []
        row_6 = []
        for i in range(len(land_cards)):
            if i < 10:
                row_1.append(land_cards[i])
            elif 10 < i < 20:
                row_2.append(land_cards[i])
            elif 20 < i < 30:
                row_3.append(land_cards[i])
            elif 30 < i < 40:
                row_4.append(land_cards[i])
            elif 40 < i < 50:
                row_5.append(land_cards[i])
            elif 50 < i < 60:
                row_6.append(land_cards[i])


        i = 0
        while i < len(row_1):
            land_card = row_1[i]
            x = draw_search_box_x + (padding_w*i+1) + (card_w*i)
            y = draw_search_box_y + (upper_padding_h)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.add(land_sprite)
            i += 1
        i = 0
        while i < len(row_2):
            land_card = row_1[i]
            x = draw_search_box_x + (padding_w*i+1) + (card_w*i)
            y = draw_search_box_y + (upper_padding_h*2) + card_h
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.addd(land_sprite)
            i += 1
        i = 0
        while i < len(row_3):
            land_card = row_1[i]
            x = draw_search_box_x + (padding_w*i+1) + (card_w*i)
            y = draw_search_box_y + (upper_padding_h*3) + (card_h*2)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.add(land_sprite)
            i += 1
        i = 0
        while i < len(row_4):
            land_card = row_1[i]
            x = draw_search_box_x + (padding_w*i+1) + (card_w*i)
            y = draw_search_box_y + (upper_padding_h*4) + (card_h*3)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.add(land_sprite)
            i += 1
        i = 0
        while i < len(row_5):
            land_card = row_1[i]
            x = draw_search_box_x + (padding_w*i+1) + (card_w*i)
            y = draw_search_box_y + (upper_padding_h*5) + (card_h*4)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.add(land_sprite)
            i += 1
        i = 0
        while i < len(row_6):
            land_card = row_1[i]
            x = draw_search_box_x + (padding_w*i+1) + (card_w*i)
            y = draw_search_box_y + (upper_padding_h*5) + (card_h*4)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.add(land_sprite)
            i += 1

        LAND_CARD_SPRITE_GROUP.draw(self.display)

        pygame.display.update()
        return LAND_CARD_SPRITE_GROUP


    def view_card(self, card_sprite):
        VIEWED_CARD.empty()
        card_copy = copy.copy(card_sprite.card)
        card_texture = pygame.image.load("." + card_copy.texture)
        x = self.card_display_sec.x
        y = self.card_display_sec.y
        w = self.card_display_sec.w
        h = self.card_display_sec.h
        viewed_sprite = CardSprite(card_copy, x, y, w, h)
        VIEWED_CARD.add(viewed_sprite)

        


    def tap_mana(self, land):
        land.image = pygame.transform.rotate(land.image, 90)

    def tap_creature(self, creature):
        creature.image = pygame.transform.rotate(creature.image, 90)


    def draw_board(self, active_phase):
        print(self.display_size)
        print(self.display)
        player_1 = self.player_1
        player_2 = self.player_2
        display = self.display

        display.fill((255,255,255))

        self.draw_menu_box_section()
        self.draw_player_hand_section()
        self.draw_phase_box()
        self.draw_info_box()
        self.draw_player_1_mana_sec()
        self.draw_player_1_play_sec()
        self.draw_player_1_land_sec()
        self.draw_player_1_battlefield()
        self.draw_player_2_mana_sec()
        self.draw_player_2_play_sec()
        self.draw_player_2_land_sec()
        self.draw_player_2_battlefield()
        self.draw_player_1_player_sec()
        self.draw_player_2_player_sec()
        self.draw_player_1_name()
        self.draw_player_2_name()
        self.draw_card_display_sec()
        self.draw_hand(player_1)
        self.draw_phase_section(active_phase)

    def draw_phase_section(self, active_phase):
        phase_button_w = self.phase_box_sec.w/7
        phase_button_h = self.phase_box_sec.h

        untap_phase_sec_x = self.phase_box_sec.x
        untap_phase_sec_y = self.phase_box_sec.y

        draw_phase_sec_x = untap_phase_sec_x + phase_button_w
        draw_phase_sec_y = untap_phase_sec_y

        main_1_phase_sec_x = draw_phase_sec_x + phase_button_w
        main_1_phase_sec_y = draw_phase_sec_y

        combat_phase_sec_x = main_1_phase_sec_x + phase_button_w
        combat_phase_sec_y = main_1_phase_sec_y

        main_2_phase_sec_x = combat_phase_sec_x + phase_button_w
        main_2_phase_sec_y = combat_phase_sec_y

        end_phase_sec_x = main_2_phase_sec_x + phase_button_w
        end_phase_sec_y = main_2_phase_sec_y


        phase_button_colour = (104,58,116)
        active = False

        if active_phase == "untap":
            active = True
        untap_button = PhaseSection(self.display, untap_phase_sec_x, untap_phase_sec_y, phase_button_w, phase_button_h, phase_button_colour, True, active)
        untap_button.draw()
        active = False

        if active_phase == "draw":
            active = True
        draw_button = PhaseSection(self.display, draw_phase_sec_x, draw_phase_sec_y, phase_button_w, phase_button_h, phase_button_colour, True, active)
        draw_button.draw()
        active = False

        if active_phase == "main_1":
            active = True
        main_1_button = PhaseSection(self.display, main_1_phase_sec_x, main_1_phase_sec_y, phase_button_w, phase_button_h, phase_button_colour, True, active)
        main_1_button.draw()
        active = False

        if active_phase == "combat":
            active = True
        combat_button = PhaseSection(self.display, combat_phase_sec_x, combat_phase_sec_y, phase_button_w, phase_button_h, phase_button_colour, True, active)
        combat_button.draw()
        active = False

        if active_phase == "main_2":
            active = True
        main_2_button = PhaseSection(self.display, main_2_phase_sec_x, main_2_phase_sec_y, phase_button_w, phase_button_h, phase_button_colour, True, active)
        main_2_button.draw()
        active = False

        if active_phase == "end":
            active = True
        end_button = PhaseSection(self.display, end_phase_sec_x, end_phase_sec_y, phase_button_w, phase_button_h, phase_button_colour, True, active)
        end_button.draw()
        active = False

        phase_font = pygame.font.Font(pygame.font.get_default_font(), int(phase_button_h*0.6))

        untap_phase_text = phase_font.render(("Untap"), True, (0,0,0))
        untap_phase_rec = untap_phase_text.get_rect()
        untap_phase_rec.center = ((untap_phase_sec_x+(phase_button_w/2)), (untap_phase_sec_y+(phase_button_h/2)))
        self.display.blit(untap_phase_text, untap_phase_rec)

        draw_phase_text = phase_font.render(("Draw"), True, (0,0,0))
        draw_phase_rec = draw_phase_text.get_rect()
        draw_phase_rec.center = ((draw_phase_sec_x+(phase_button_w/2)), (draw_phase_sec_y+(phase_button_h/2)))
        self.display.blit(draw_phase_text, draw_phase_rec)

        main_1_phase_text = phase_font.render(("Main 1"), True, (0,0,0))
        main_1_phase_rec = main_1_phase_text.get_rect()
        main_1_phase_rec.center = ((main_1_phase_sec_x+(phase_button_w/2)), (main_1_phase_sec_y+(phase_button_h/2)))
        self.display.blit(main_1_phase_text, main_1_phase_rec)

        combat_phase_text = phase_font.render(("Combat"), True, (0,0,0))
        combat_phase_rec = combat_phase_text.get_rect()
        combat_phase_rec.center = ((combat_phase_sec_x+(phase_button_w/2)), (combat_phase_sec_y+(phase_button_h/2)))
        self.display.blit(combat_phase_text, combat_phase_rec)

        main_2_phase_text = phase_font.render(("Main 2"), True, (0,0,0))
        main_2_phase_rec = main_2_phase_text.get_rect()
        main_2_phase_rec.center = ((main_2_phase_sec_x+(phase_button_w/2)), (main_2_phase_sec_y+(phase_button_h/2)))
        self.display.blit(main_2_phase_text, main_2_phase_rec)

        end_phase_text = phase_font.render(("End"), True, (0,0,0))
        end_phase_rec = end_phase_text.get_rect()
        end_phase_rec.center = ((end_phase_sec_x+(phase_button_w/2)), (end_phase_sec_y+(phase_button_h/2)))
        self.display.blit(end_phase_text, end_phase_rec)








    def draw_menu_box_section(self):
        menu_box_x = 0
        menu_box_y = self.display_h * (13/16)
        menu_box_w = self.display_w * (1/7)
        menu_box_h = self.display_h * (3/16)
        menu_box_colour = (125,80,2)

        self.menu_box_sec = BoardSection(self.display, menu_box_x, menu_box_y, menu_box_w, menu_box_h, menu_box_colour, False)
        self.menu_box_sec.draw()

        self.draw_concede_button()
        self.draw_options_button()

    def draw_options_button(self):
        options_button_x = (self.menu_box_sec.x + self.menu_box_sec.w * (1/8))
        options_button_y = (self.menu_box_sec.y + self.menu_box_sec.h * (1/5))
        options_button_w = self.menu_box_sec.w * (3/4)
        options_button_h = self.menu_box_sec.h * (1/4)
        options_button_colour = (177,177,177)

        self.options_button_sec = BoardSection(self.display, options_button_x, options_button_y, options_button_w, options_button_h, options_button_colour, True)
        self.options_button_sec.draw()

        menu_font = pygame.font.Font(pygame.font.get_default_font(), int(options_button_h*0.6))

        options_button_text = menu_font.render(("Options"), True, (0,0,0))
        options_button_rec = options_button_text.get_rect()
        options_button_rec.center = ((options_button_x+(options_button_w /2)), (options_button_y+(options_button_h/2)))
        self.display.blit(options_button_text, options_button_rec)


    def draw_concede_button(self):
        concede_button_x = (self.menu_box_sec.x + self.menu_box_sec.w * (1/8))
        concede_button_y = (self.menu_box_sec.y + self.menu_box_sec.h * (3/5))
        concede_button_w = self.menu_box_sec.w * (3/4)
        concede_button_h = self.menu_box_sec.h * (1/4)
        concede_button_colour = (177,177,177)

        self.concede_button_sec = BoardSection(self.display, concede_button_x, concede_button_y, concede_button_w, concede_button_h, concede_button_colour, True)
        self.concede_button_sec.draw()

        menu_font = pygame.font.Font(pygame.font.get_default_font(), int(concede_button_h*0.6))

        concede_button_text = menu_font.render(("Concede"), True, (0,0,0))
        concede_button_rec = concede_button_text.get_rect()
        concede_button_rec.center = ((concede_button_x+(concede_button_w /2)), (concede_button_y+(concede_button_h/2)))
        self.display.blit(concede_button_text, concede_button_rec)

    def draw_player_hand_section(self):
        hand_section_x = self.menu_box_sec.x + self.menu_box_sec.w
        hand_section_y = self.menu_box_sec.y
        hand_section_w = self.display_w - self.menu_box_sec.w
        hand_section_h = self.menu_box_sec.h
        hand_section_colour = (199,125,3)

        self.player_hand_sec = BoardSection(self.display, hand_section_x, hand_section_y, hand_section_w, hand_section_h, hand_section_colour)
        self.player_hand_sec.draw()

    def draw_phase_box(self):
        phase_box_x = self.player_hand_sec.x
        phase_box_h = self.display_h * (1/16)
        phase_box_y = self.player_hand_sec.y - phase_box_h
        phase_box_w = self.player_hand_sec.w
        phase_box_colour = WHITE

        self.phase_box_sec = BoardSection(self.display, phase_box_x, phase_box_y, phase_box_w, phase_box_h, phase_box_colour)
        self.phase_box_sec.draw()

    def draw_info_box(self):
        info_box_x = 0
        info_box_y = 0
        info_box_h = self.display_h * (13/16)
        info_box_w = self.menu_box_sec.w
        info_box_colour = (125,80,2)

        self.info_box_sec = BoardSection(self.display, info_box_x, info_box_y, info_box_w, info_box_h, info_box_colour)
        self.info_box_sec.draw()

    def draw_player_1_play_sec(self):
        x = self.player_hand_sec.x
        h = ((self.display_h - (self.player_hand_sec.h + self.phase_box_sec.h)) / 2)
        y = self.phase_box_sec.y - h
        w = self.phase_box_sec.w

        self.player_1_play_sec = BoardSection(self.display, x, y, w, h, (120,120,120))
        self.player_1_play_sec.draw()

    def draw_player_1_land_sec(self):
        x = self.phase_box_sec.x + (self.phase_box_sec.border_size)
        h = ((self.display_h - (self.player_hand_sec.h + self.phase_box_sec.h))/2)*(7/20)
        y = self.phase_box_sec.y - h
        w = self.phase_box_sec.w - (self.phase_box_sec.border_size*2)
        colour = (251,185,74)

        self.player_1_land_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_land_sec.draw()

    def draw_player_1_battlefield(self):
        player_1_battlefield_x = self.player_1_land_sec.x
        player_1_battlefield_h = ((self.display_h - (self.player_hand_sec.h + self.phase_box_sec.h)) / 2) - self.player_1_land_sec.h - self.player_1_play_sec.border_size
        player_1_battlefield_y = self.player_1_land_sec.y - player_1_battlefield_h
        player_1_battlefield_w = self.player_1_land_sec.w
        player_1_battlefield_colour = colour = (251,185,74)

        self.player_1_battlefield_sec = BoardSection(self.display, player_1_battlefield_x, player_1_battlefield_y, player_1_battlefield_w, player_1_battlefield_h, player_1_battlefield_colour, False)
        self.player_1_battlefield_sec.draw()

    def draw_player_2_play_sec(self):
        x = self.player_1_play_sec.x
        y = 0
        w = self.player_1_play_sec.w
        h = self.player_1_play_sec.h

        self.player_2_play_sec = BoardSection(self.display, x, y, w, h, (11,11,11))
        self.player_2_play_sec.draw()

    def draw_player_2_land_sec(self):
        x = self.player_1_land_sec.x
        y = 0
        w = self.player_1_land_sec.w
        h = self.player_1_land_sec.h
        colour = (251,185,74)

        self.player_2_land_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_land_sec.draw()

    def draw_player_2_battlefield(self):
        player_2_battlefield_x = self.player_2_land_sec.x
        player_2_battlefield_h = self.player_1_battlefield_sec.h
        player_2_battlefield_y = self.player_2_land_sec.y + self.player_2_land_sec.h
        player_2_battlefield_w = self.player_2_land_sec.w
        player_2_battlefield_colour = (251,185,74)

        self.player_2_battlefield_sec = BoardSection(self.display, player_2_battlefield_x, player_2_battlefield_y, player_2_battlefield_w, player_2_battlefield_h, player_2_battlefield_colour, False)
        self.player_2_battlefield_sec.draw()

    def draw_player_1_mana_sec(self):
        mana_w = (self.info_box_sec.w*(0.90))/5
        mana_h = mana_w
        mana_y = self.menu_box_sec.y - self.info_box_sec.w*(0.05) - mana_h

        x = self.info_box_sec.x + self.info_box_sec.w*(0.05)


        player_1_r_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (200,0,0))
        self.player_1_mana_box_r = player_1_r_mana_sec
        player_1_r_mana_sec.draw()

        x = player_1_r_mana_sec.x + mana_w

        player_1_g_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (0,200,0))
        player_1_g_mana_sec.draw()

        x = player_1_g_mana_sec.x + mana_w

        player_1_u_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h,(0,102,204))
        player_1_u_mana_sec.draw()

        x = player_1_u_mana_sec.x + mana_w

        player_1_w_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (255,255,204))
        player_1_w_mana_sec.draw()

        x = player_1_w_mana_sec.x + mana_w

        player_1_b_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (122,0,122))
        player_1_b_mana_sec.draw()

        mana_font = pygame.font.Font(pygame.font.get_default_font(), int(mana_h*0.7))

        player_1_mana = self.player_1.mana

        player_1_r = len(re.findall("R", player_1_mana))

        player_1_r_mana_text = mana_font.render(str(player_1_r), True, (0,0,0))
        player_1_r_mana_rec = player_1_r_mana_text.get_rect()
        player_1_r_mana_rec.center = ((player_1_r_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_1_r_mana_text, player_1_r_mana_rec)

        player_1_g = len(re.findall("G", player_1_mana))

        player_1_g_mana_text = mana_font.render(str(player_1_g), True, (0,0,0))
        player_1_g_mana_rec = player_1_g_mana_text.get_rect()
        player_1_g_mana_rec.center = ((player_1_g_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_1_g_mana_text, player_1_g_mana_rec)

        player_1_u = len(re.findall("U", player_1_mana))

        player_1_u_mana_text = mana_font.render(str(player_1_u), True, (0,0,0))
        player_1_u_mana_rec = player_1_u_mana_text.get_rect()
        player_1_u_mana_rec.center = ((player_1_u_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_1_u_mana_text, player_1_u_mana_rec)

        player_1_w = len(re.findall("W", player_1_mana))

        player_1_w_mana_text = mana_font.render(str(player_1_w), True, (0,0,0))
        player_1_w_mana_rec = player_1_w_mana_text.get_rect()
        player_1_w_mana_rec.center = ((player_1_w_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_1_w_mana_text, player_1_w_mana_rec)

        player_1_b = len(re.findall("B", player_1_mana))

        player_1_b_mana_text = mana_font.render(str(player_1_b), True, (0,0,0))
        player_1_b_mana_rec = player_1_b_mana_text.get_rect()
        player_1_b_mana_rec.center = ((player_1_b_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_1_b_mana_text, player_1_b_mana_rec)


    def draw_player_2_mana_sec(self):
        mana_w = (self.info_box_sec.w*(0.90))/5
        mana_h = mana_w
        mana_y = self.info_box_sec.w*(0.05)

        x = self.info_box_sec.x + self.info_box_sec.w*(0.05)

        player_2_r_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (200,0,0))
        self.player_2_mana_box_r = player_2_r_mana_sec
        player_2_r_mana_sec.draw()

        x = player_2_r_mana_sec.x + mana_w

        player_2_g_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (0,200,0))
        player_2_g_mana_sec.draw()

        x = player_2_g_mana_sec.x + mana_w

        player_2_u_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h,(0,102,204))
        player_2_u_mana_sec.draw()

        x = player_2_u_mana_sec.x + mana_w

        player_2_w_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (255,255,204))
        player_2_w_mana_sec.draw()

        x = player_2_w_mana_sec.x + mana_w

        player_2_b_mana_sec = BoardSection(self.display, x, mana_y, mana_w, mana_h, (122,0,122))
        player_2_b_mana_sec.draw()

        mana_font = pygame.font.Font(pygame.font.get_default_font(), int(mana_h*0.7))

        player_2_mana = self.player_1.mana

        player_2_r = len(re.findall("R", player_2_mana))

        player_2_r_mana_text = mana_font.render(str(player_2_r), True, (0,0,0))
        player_2_r_mana_rec = player_2_r_mana_text.get_rect()
        player_2_r_mana_rec.center = ((player_2_r_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_2_r_mana_text, player_2_r_mana_rec)

        player_2_g = len(re.findall("G", player_2_mana))

        player_2_g_mana_text = mana_font.render(str(player_2_g), True, (0,0,0))
        player_2_g_mana_rec = player_2_g_mana_text.get_rect()
        player_2_g_mana_rec.center = ((player_2_g_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_2_g_mana_text, player_2_g_mana_rec)

        player_2_u = len(re.findall("U", player_2_mana))

        player_2_u_mana_text = mana_font.render(str(player_2_u), True, (0,0,0))
        player_2_u_mana_rec = player_2_u_mana_text.get_rect()
        player_2_u_mana_rec.center = ((player_2_u_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_2_u_mana_text, player_2_u_mana_rec)

        player_2_w = len(re.findall("W", player_2_mana))

        player_2_w_mana_text = mana_font.render(str(player_2_w), True, (0,0,0))
        player_2_w_mana_rec = player_2_w_mana_text.get_rect()
        player_2_w_mana_rec.center = ((player_2_w_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_2_w_mana_text, player_2_w_mana_rec)

        player_2_b = len(re.findall("B", player_2_mana))

        player_2_b_mana_text = mana_font.render(str(player_2_b), True, (0,0,0))
        player_2_b_mana_rec = player_2_b_mana_text.get_rect()
        player_2_b_mana_rec.center = ((player_2_b_mana_sec.x+(mana_w/2)), (mana_y+(mana_h/2)))
        self.display.blit(player_2_b_mana_text, player_2_b_mana_rec)

    def draw_player_1_player_sec(self):
        x = self.player_1_mana_box_r.x
        w = self.player_1_mana_box_r.w*5
        h = w*(0.7)
        y = self.player_1_mana_box_r.y - self.info_box_sec.w*(0.05) - h
        colour = (122,122,122)

        self.player_1_player_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_1_player_sec.draw()

    def draw_player_1_name(self):
        x = self.player_1_player_sec.x + self.player_1_player_sec.border_size
        h = self.player_1_player_sec.h*(3/10)
        y = self.player_1_player_sec.y + self.player_1_player_sec.border_size
        w = (self.player_1_player_sec.w - (2*self.player_1_player_sec.border_size)) * (0.7)
        colour = (80,80,80)

        self.player_1_name_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_name_sec.draw()

        name_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.5))
        string = self.player_1.name
        name_text = name_font.render(string, True, (0,0,0))
        name_rec = name_text.get_rect()
        name_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(name_text, name_rec)

    def draw_player_2_name(self):
        x = self.player_1_name_sec.x
        y = self.player_2_player_sec.y + self.player_2_player_sec.border_size
        w = self.player_1_name_sec.w
        h = self.player_1_name_sec.h
        colour = self.player_1_name_sec.colour

        self.player_2_name_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_name_sec.draw()

        name_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.5))
        string = self.player_2.name
        name_text = name_font.render(string, True, (0,0,0))
        name_rec = name_text.get_rect()
        name_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(name_text, name_rec)

    def draw_player_1_life(self):
        x = self.player_1_name_sec.x + self.player_1_name_sec.w

    def draw_player_2_player_sec(self):
        x = self.player_1_player_sec.x
        y = self.player_2_mana_box_r.y + self.player_2_mana_box_r.h + self.info_box_sec.w*(0.05)
        w = self.player_1_player_sec.w
        h = self.player_1_player_sec.h
        colour = self.player_1_player_sec.colour

        self.player_2_player_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_2_player_sec.draw()

    def draw_card_display_sec(self):
        w = self.player_1_player_sec.w
        h = w*(88/63)
        x = self.player_1_player_sec.x
        y = (self.info_box_sec.y + self.info_box_sec.h)/2 - (h/2)
        colour = (100,0,100)

        self.card_display_sec = BoardSection(self.display, x, y, w, h, colour)
        self.card_display_sec.draw()

    def draw_options_menu(self):
        display_width, display_height = self.display_size

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

        self.in_options = True
        while self.in_options:
            (mx, my) = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    myquit()

            current_vol = str(round(pygame.mixer.music.get_volume(), 1))

            self.display.fill(bg_colour)     

            pygame.draw.rect(self.display, BLACK, (option_box_x, option_box_y, option_box_w, option_box_h))

            pygame.draw.rect(self.display, bright_red, (display_width/6, display_height/6, (display_width/3)*2, (display_height/3)*2))

            change_res = Button("Change resolution",change_resolution_button_x, change_resolution_button_y, option_button_width, option_button_height, button_blue, button_blue)

            res_1 = Button("800x600", int(res_1_x), int(res_1_y), res_button_width, res_button_height, grey, WHITE, "change_res")

            res_2 = Button("1024x768", int(res_2_x), int(res_2_y), res_button_width, res_button_height, grey, WHITE, "change_res")

            res_3 = Button("1440x900", int(res_3_x), int(res_3_y),res_button_width, res_button_height, grey, WHITE, "change_res")

            res_4 = Button("1600x900", int(res_4_x), int(res_4_y), res_button_width, res_button_height, grey, WHITE, "change_res")

            res_5 = Button("1920x1080", int(res_5_x), int(res_5_y), res_button_width, res_button_height, grey, WHITE, "change_res")

            
            back = Button("Back", back_button_x, back_button_y, option_button_width, option_button_height, button_blue, hover_button_blue, "back")

                    
            volume = Button("Volume", volume_button_x, volume_button_y, option_button_width, option_button_height, button_blue, button_blue)
            
            slider = Button(current_vol, volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height, volume_slider_colour, volume_slider_colour)

            plus = Button("+", plus_button_x, plus_button_y, plus_button_width, plus_button_height, grey, WHITE, "plus")

            minus = Button("-", minus_button_x, minus_button_y, minus_button_width, minus_button_height, grey, WHITE, "minus")

            self.draw_button(change_res)
            self.draw_button(back)
            self.draw_button(volume)
            self.draw_button(slider)
            self.draw_button(plus)
            self.draw_button(minus)
            self.draw_button(res_1)
            self.draw_button(res_2)
            self.draw_button(res_3)
            self.draw_button(res_4)
            self.draw_button(res_5)

            pygame.display.update()

    def draw_button(self, name):
         #list of possible resolutions
        res_list = ["1920x1080", "800x600", "1440x900", "1024x768", "1600x900"]

        #Take in the co-ordinates of the mouse
        mouse = pygame.mouse.get_pos()
        
        #Check what buttons have been pressed by the mouse
        click = pygame.mouse.get_pressed()

        #Check if mouse position is within the boundry of the button
        if (name.x + name.w) > mouse[0] > name.x and (name.y + name.h) > mouse[1] > name.y:
            
            #Highlight the button with a lighter shad of blue
            pygame.draw.rect(self.display, name.a_colour, (name.x, name.y, name.w, name.h))

            if click[0] == 1 and name.action != None:
                if name.action == "change_res":
                    for res in res_list:
                        if name.msg == res:
                            new_res = res.split("x")
                            self.display_h = int(new_res[1])
                            self.display_w = int(new_res[0])
                            self.display_size = self.display_w , self.display_h
                            self.display = pygame.display.set_mode(self.display_size)
                            self.draw_board("untap")
                            self.draw_options_menu()

                elif name.action == "plus":
                    self.increase_volume()

                elif name.action == "minus":
                    self.decrease_volume()

                elif name.action == "back":
                    self.in_options = False
        else:
            pygame.draw.rect(self.display, name.i_colour, (name.x, name.y, name.w, name.h))

        if  name.msg in res_list:
            smallFont = pygame.font.Font("freesansbold.ttf", int(name.h/7))
            smallText = smallFont.render(name.msg, False, BLACK)
            smallRect = smallText.get_rect()
            smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
            self.display.blit(smallText, smallRect)

        else:
            if name.w > name.h:
                font_size = name.h/4
            else:
                font_size = name.w/4
            smallFont = pygame.font.Font("freesansbold.ttf", int(font_size))
            smallText = smallFont.render(name.msg, False, BLACK)
            smallRect = smallText.get_rect()
            smallRect.center = (name.x + (name.w/2), name.y + (name.h/2))
            self.display.blit(smallText, smallRect)


    def increase_volume(self):
        time.sleep(0.2)
        if pygame.mixer.music.get_volume() < 1.0:
            curr_vol = pygame.mixer.music.get_volume()
            curr_vol += 0.1
            pygame.mixer.music.set_volume(curr_vol)

    def decrease_volume(self):
        time.sleep(0.2)
        if pygame.mixer.music.get_volume() > 0:
            curr_vol = pygame.mixer.music.get_volume()
            curr_vol -= 0.1
            pygame.mixer.music.set_volume(curr_vol)



def main():
    display_size = display_width, display_height= (1600, 900)
    gameDisplay = pygame.display.set_mode(display_size)
    player_1 = player.Player("Sean")
    player_2 = player.Player("Kacper")

    f = open("../personal_decks/deck_3", "rb")
    player_deck = pickle.load(f)
    f.close()

    random.shuffle(player_deck)

    player_1.deck = deck.Deck("gablins", player_deck)
    player_2.deck = deck.Deck("gibluns", player_deck)

    for i in range(7):
        player_1.hand.append(player_1.deck.cards.pop(0))


    gameBoard = Board(gameDisplay, display_size, player_1, player_2)
    phases = ["untap", "draw", "main_1", "combat", "main_2", "end"]
    gameBoard.draw_board("untap")
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

            pos = pygame.mouse.get_pos()

            for card in PLAYER_1_HAND_SPRITE_CARD_GROUP:
                if card.rect.collidepoint(pos):
                    gameBoard.view_card(card)
                    VIEWED_CARD.draw(gameDisplay)
                    pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if gameBoard.concede_button_sec.x < pos[0] < gameBoard.concede_button_sec.x + gameBoard.concede_button_sec.w and gameBoard.concede_button_sec.y < pos[1] < gameBoard.concede_button_sec.y + gameBoard.concede_button_sec.h:
                        quit = True
                    if gameBoard.options_button_sec.x < pos[0] < gameBoard.options_button_sec.x + gameBoard.options_button_sec.w and gameBoard.options_button_sec.y < pos[1] < gameBoard.options_button_sec.y + gameBoard.options_button_sec.h:
                        gameBoard.draw_options_menu()
                        gameBoard.draw_board("untap")


            for phase in phases:
                gameBoard.draw_phase_section(phase)
                pygame.display.update()
            clock.tick(60)




if __name__ == "__main__":
    main()
