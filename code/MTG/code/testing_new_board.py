import pygame
import re
import time

import player
import pickle
import deck

pygame.init()
pygame.mixer.init()
PLAYER_1_HAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_2_HAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_1_LAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_2_LAND_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP = pygame.sprite.Group()
PLAYER_1_SEARCH_SPRITES = pygame.sprite.Group()
PLAYER_2_SEARCH_SPRITES = pygame.sprite.Group()



WHITE = (255,255,255)
Black = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


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
        self.player_1_name_info_sec = None
        self.player_2_name_info_sec = None
        self.player_1_name_sec = None
        self.player_2_name_sec = None
        self.player_1_life_sec = None
        self.player_2_life_sec = None
        self.card_display_sec = None
        self.player_1_hand_info_sec = None
        self.player_2_hand_info_sec = None
        self.player_1_hand_name = None
        self.player_2_hand_name = None
        self.player_1_hand_size = None
        self.player_2_hand_size = None
        self.player_1_deck_info_sec = None
        self.player_2_deck_info_sec = None
        self.player_1_deck_name = None
        self.player_2_deck_name = None
        self.player_1_deck_size = None
        self.player_2_deck_size = None
        self.player_1_grave_info_sec = None
        self.player_2_grave_info_sec = None
        self.player_1_grave_name = None
        self.player_2_grave_name = None
        self.player_1_grave_size = None
        self.player_2_grave_size = None

    def draw_hand(self, player):
        cards = player.hand
        print(cards)
        for card in cards:
            print(card.name)
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
            print("1")
            PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP.empty()
            if len(battlefield_cards) <= 20:
                print("2")
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
        time.sleep(1)
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


    def view_card(self, card):
        card_texture = pygame.image.load(card.card.texture)
        card.image = card_texture
        card.rect = card.image.get_rect()
        new_w = int(card.rect.w * (3/5))
        new_h = int(card.rect.h * (3/5))
        card.image = pygame.transform.smoothscale(card_texture,(int(new_w), int(new_h)))
        card.rect = card.image.get_rect()
        card.rect.x = 0
        card.rect.y = self.display_size[1] - new_h



    def tap_mana(self, land):
        land.image = pygame.transform.rotate(land.image, 90)

    def tap_creature(self, creature):
        creature.image = pygame.transform.rotate(creature.image, 90)


    def draw_board(self):
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
        self.draw_player_1_name_info_sec()
        self.draw_player_2_name_info_sec()
        self.draw_player_1_name()
        self.draw_player_2_name()
        self.draw_card_display_sec()
        self.draw_player_1_life()
        self.draw_player_2_life()
        self.draw_hand(player_1)
        self.draw_player_1_hand_info_sec()
        self.draw_player_2_hand_info_sec()
        self.draw_player_1_hand_name()
        self.draw_player_2_hand_name()
        self.draw_player_1_hand_size()
        self.draw_player_2_hand_size()
        self.draw_player_1_deck_info_sec()
        self.draw_player_2_deck_info_sec()
        self.draw_player_1_deck_name()
        self.draw_player_2_deck_name()
        self.draw_player_1_deck_size()
        self.draw_player_2_deck_size()
        self.draw_player_1_grave_info_sec()
        self.draw_player_2_grave_info_sec()
        self.draw_player_1_grave_name()
        self.draw_player_2_grave_name()
        self.draw_player_1_grave_size()
        self.draw_player_2_grave_size()



    def draw_menu_box_section(self):
        menu_box_x = 0
        menu_box_y = self.display_h * (13/16)
        menu_box_w = self.display_w * (1/7)
        menu_box_h = self.display_h * (3/16)
        menu_box_colour = RED

        self.menu_box_sec = BoardSection(self.display, menu_box_x, menu_box_y, menu_box_w, menu_box_h, menu_box_colour, False)
        self.menu_box_sec.draw()

    def draw_player_hand_section(self):
        hand_section_x = self.menu_box_sec.x + self.menu_box_sec.w
        hand_section_y = self.menu_box_sec.y
        hand_section_w = self.display_w - self.menu_box_sec.w
        hand_section_h = self.menu_box_sec.h
        hand_section_colour = GREEN

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
        info_box_colour = BLUE

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
        colour = (255,120,120)

        self.player_1_land_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_land_sec.draw()

    def draw_player_1_battlefield(self):
        player_1_battlefield_x = self.player_1_land_sec.x
        player_1_battlefield_h = ((self.display_h - (self.player_hand_sec.h + self.phase_box_sec.h)) / 2) - self.player_1_land_sec.h - self.player_1_play_sec.border_size
        player_1_battlefield_y = self.player_1_land_sec.y - player_1_battlefield_h
        player_1_battlefield_w = self.player_1_land_sec.w
        player_1_battlefield_colour = RED

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
        colour = self.player_1_land_sec.colour

        self.player_2_land_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_land_sec.draw()

    def draw_player_2_battlefield(self):
        player_2_battlefield_x = self.player_2_land_sec.x
        player_2_battlefield_h = self.player_1_battlefield_sec.h
        player_2_battlefield_y = self.player_2_land_sec.y + self.player_2_land_sec.h
        player_2_battlefield_w = self.player_2_land_sec.w
        player_2_battlefield_colour = RED

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

    def draw_player_1_name_info_sec(self):
        x = self.player_1_player_sec.x
        y = self.player_1_player_sec.y
        w = self.player_1_player_sec.w
        h = self.player_1_player_sec.h/4
        colour = (255,255,255)

        self.player_1_name_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_1_name_info_sec.draw()

    def draw_player_2_name_info_sec(self):
        x = self.player_1_name_info_sec.x
        y = self.player_2_player_sec.y
        w = self.player_2_player_sec.w
        h = self.player_1_name_info_sec.h
        colour = self.player_1_name_info_sec.colour

        self.player_2_name_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_2_name_info_sec.draw()

    def draw_player_1_name(self):
        x = self.player_1_name_info_sec.x + self.player_1_player_sec.border_size
        h = self.player_1_name_info_sec.h - (2*self.player_1_name_info_sec.border_size)
        y = self.player_1_name_info_sec.y + self.player_1_name_info_sec.border_size
        w = (self.player_1_name_info_sec.w - (2*self.player_1_name_info_sec.border_size)) * (0.7)
        colour = (80,80,80)

        self.player_1_name_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_name_sec.draw()

        name_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = self.player_1.name
        name_text = name_font.render(string, True, (0,0,0))
        name_rec = name_text.get_rect()
        name_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(name_text, name_rec)

    def draw_player_2_name(self):
        x = self.player_1_name_sec.x
        y = self.player_2_name_info_sec.y + self.player_2_name_info_sec.border_size
        w = self.player_1_name_sec.w
        h = self.player_1_name_sec.h
        colour = self.player_1_name_sec.colour

        self.player_2_name_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_name_sec.draw()

        name_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = self.player_2.name
        name_text = name_font.render(string, True, (0,0,0))
        name_rec = name_text.get_rect()
        name_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(name_text, name_rec)

    def draw_player_1_life(self):
        x = self.player_1_name_sec.x + self.player_1_name_sec.w
        y = self.player_1_name_sec.y
        w = self.player_1_player_sec.w - self.player_1_name_sec.w - (self.player_1_player_sec.border_size*2)
        h = self.player_1_name_sec.h
        colour = (255, 255, 255)

        self.player_1_life_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_life_sec.draw()

        life_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(self.player_1.life)
        life_text = life_font.render(string, True, (0,0,0))
        life_rec = life_text.get_rect()
        life_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(life_text, life_rec)

    def draw_player_2_life(self):
        x = self.player_1_life_sec.x
        y = self.player_2_name_sec.y
        w = self.player_1_life_sec.w
        h = self.player_1_life_sec.h
        colour = self.player_1_life_sec.colour

        self.player_2_life_sec = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_life_sec.draw()

        life_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(self.player_2.life)
        life_text = life_font.render(string, True, (0,0,0))
        life_rec = life_text.get_rect()
        life_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(life_text, life_rec)

    def draw_player_2_player_sec(self):
        x = self.player_1_player_sec.x
        y = self.player_2_mana_box_r.y + self.player_2_mana_box_r.h + self.info_box_sec.w*(0.05)
        w = self.player_1_player_sec.w
        h = self.player_1_player_sec.h
        colour = self.player_1_player_sec.colour

        self.player_2_player_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_2_player_sec.draw()

    def draw_player_1_hand_info_sec(self):
        x = self.player_1_player_sec.x
        y = self.player_1_name_info_sec.y +self.player_1_name_info_sec.h
        w = self.player_1_name_info_sec.w
        h = self.player_1_name_info_sec.h
        colour = self.player_1_name_info_sec.colour

        self.player_1_hand_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_1_hand_info_sec.draw()

    def draw_player_2_hand_info_sec(self):
        x = self.player_1_hand_info_sec.x
        y = self.player_2_name_info_sec.y + self.player_2_name_info_sec.h
        w = self.player_1_hand_info_sec.w
        h = self.player_1_hand_info_sec.h
        colour = self.player_1_hand_info_sec.colour

        self.player_2_hand_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_2_hand_info_sec.draw()

    def draw_player_1_hand_name(self):
        x = self.player_1_name_sec.x
        y = self.player_1_hand_info_sec.y + self.player_1_hand_info_sec.border_size
        w = self.player_1_name_sec.w
        h = self.player_2_name_sec.h
        colour = self.player_1_name_sec.colour

        self.player_1_hand_name = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_hand_name.draw()

        name_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = "Hand"
        name_text = name_font.render(string, True, (0,0,0))
        name_rec = name_text.get_rect()
        name_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(name_text, name_rec)

    def draw_player_2_hand_name(self):
        x = self.player_1_hand_name.x
        y = self.player_2_hand_info_sec.y + self.player_2_hand_info_sec.border_size
        w = self.player_1_hand_name.w
        h = self.player_1_hand_name.h
        colour = self.player_1_hand_name.colour

        self.player_2_hand_name = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_hand_name.draw()

        name_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = "Hand"
        name_text = name_font.render(string, True, (0,0,0))
        name_rec = name_text.get_rect()
        name_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(name_text, name_rec)

    def draw_player_1_hand_size(self):
        x = self.player_1_life_sec.x
        y = self.player_1_hand_name.y
        w = self.player_1_life_sec.w
        h = self.player_1_life_sec.h
        colour = self.player_1_life_sec.colour

        self.player_1_hand_size = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_hand_size.draw()

        hand_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(len(self.player_1.hand))
        hand_text = hand_font.render(string, True, (0,0,0))
        hand_rec = hand_text.get_rect()
        hand_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(hand_text, hand_rec)

    def draw_player_2_hand_size(self):
        x = self.player_2_life_sec.x
        y = self.player_2_hand_name.y
        w = self.player_2_life_sec.w
        h = self.player_2_life_sec.h
        colour = self.player_2_life_sec.colour

        self.player_2_hand_size = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_hand_size.draw()

        hand_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(len(self.player_2.hand))
        hand_text = hand_font.render(string, True, (0,0,0))
        hand_rec = hand_text.get_rect()
        hand_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(hand_text, hand_rec)

    def draw_player_1_deck_info_sec(self):
        x = self.player_1_hand_info_sec.x
        y = self.player_1_hand_info_sec.y + self.player_1_hand_info_sec.h
        w = self.player_1_hand_info_sec.w
        h = self.player_1_hand_info_sec.h
        colour = self.player_1_hand_info_sec.colour

        self.player_1_deck_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_1_deck_info_sec.draw()

    def draw_player_2_deck_info_sec(self):
        x = self.player_2_hand_info_sec.x
        y = self.player_2_hand_info_sec.y + self.player_2_hand_info_sec.h
        w = self.player_2_hand_info_sec.w
        h = self.player_2_hand_info_sec.h
        colour = self.player_2_hand_info_sec.colour

        self.player_2_deck_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_2_deck_info_sec.draw()

    def draw_player_1_deck_name(self):
        x = self.player_1_hand_name.x
        y = self.player_1_deck_info_sec.y + self.player_1_deck_info_sec.border_size
        w = self.player_1_hand_name.w
        h = self.player_1_hand_name.h
        colour = self.player_1_hand_name.colour

        self.player_1_deck_name = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_deck_name.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = "Deck"
        deck_text = deck_font.render(string, True, (0,0,0))
        deck_rec = deck_text.get_rect()
        deck_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(deck_text, deck_rec)

    def draw_player_2_deck_name(self):
        x = self.player_2_hand_name.x
        y = self.player_2_deck_info_sec.y + self.player_2_deck_info_sec.border_size
        w = self.player_2_hand_name.w
        h = self.player_2_hand_name.h
        colour = self.player_2_hand_name.colour

        self.player_2_deck_name = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_deck_name.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = "Deck"
        deck_text = deck_font.render(string, True, (0,0,0))
        deck_rec = deck_text.get_rect()
        deck_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(deck_text, deck_rec)

    def draw_player_1_deck_size(self):
        x = self.player_1_life_sec.x
        y = self.player_1_deck_name.y
        w = self.player_1_life_sec.w
        h = self.player_1_life_sec.h
        colour = self.player_1_life_sec.colour

        self.player_1_deck_size = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_deck_size.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(len(self.player_1.deck.cards))
        deck_text = deck_font.render(string, True, (0,0,0))
        deck_rec = deck_text.get_rect()
        deck_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(deck_text, deck_rec)

    def draw_player_2_deck_size(self):
        x = self.player_2_life_sec.x
        y = self.player_2_deck_name.y
        w = self.player_2_life_sec.w
        h = self.player_2_life_sec.h
        colour = self.player_2_life_sec.colour

        self.player_2_deck_size = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_deck_size.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(len(self.player_2.deck.cards))
        deck_text = deck_font.render(string, True, (0,0,0))
        deck_rec = deck_text.get_rect()
        deck_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(deck_text, deck_rec)

    def draw_player_1_grave_info_sec(self):
        x = self.player_1_hand_info_sec.x
        y = self.player_1_deck_info_sec.y + self.player_1_deck_info_sec.h
        w = self.player_1_hand_info_sec.w
        h = self.player_1_hand_info_sec.h
        colour = self.player_1_hand_info_sec.colour

        self.player_1_grave_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_1_grave_info_sec.draw()

    def draw_player_2_grave_info_sec(self):
        x = self.player_2_hand_info_sec.x
        y = self.player_2_deck_info_sec.y + self.player_2_deck_info_sec.h
        w = self.player_2_hand_info_sec.w
        h = self.player_2_hand_info_sec.h
        colour = self.player_2_hand_info_sec.colour

        self.player_2_grave_info_sec = BoardSection(self.display, x, y, w, h, colour)
        self.player_2_grave_info_sec.draw()

    def draw_player_1_grave_name(self):
        x = self.player_1_hand_name.x
        y = self.player_1_grave_info_sec.y + self.player_1_grave_info_sec.border_size
        w = self.player_1_hand_name.w
        h = self.player_1_hand_name.h
        colour = self.player_1_hand_name.colour

        self.player_1_grave_name = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_grave_name.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = "Grave"
        deck_text = deck_font.render(string, True, (0,0,0))
        deck_rec = deck_text.get_rect()
        deck_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(deck_text, deck_rec)


    def draw_player_2_grave_name(self):
        x = self.player_2_hand_name.x
        y = self.player_2_grave_info_sec.y + self.player_2_grave_info_sec.border_size
        w = self.player_2_hand_name.w
        h = self.player_2_hand_name.h
        colour = self.player_2_hand_name.colour

        self.player_2_grave_name = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_grave_name.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = "Grave"
        deck_text = deck_font.render(string, True, (0,0,0))
        deck_rec = deck_text.get_rect()
        deck_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(deck_text, deck_rec)

    def draw_player_1_grave_size(self):
        x = self.player_1_life_sec.x
        y = self.player_1_grave_name.y
        w = self.player_1_life_sec.w
        h = self.player_1_life_sec.h
        colour = self.player_1_life_sec.colour

        self.player_1_grave_size = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_1_grave_size.draw()

        hand_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(len(self.player_1.graveyard))
        hand_text = hand_font.render(string, True, (0,0,0))
        hand_rec = hand_text.get_rect()
        hand_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(hand_text, hand_rec)

    def draw_player_2_grave_size(self):
        x = self.player_2_life_sec.x
        y = self.player_2_grave_name.y
        w = self.player_2_life_sec.w
        h = self.player_2_life_sec.h
        colour = self.player_2_life_sec.colour

        self.player_2_grave_size = BoardSection(self.display, x, y, w, h, colour, False)
        self.player_2_grave_size.draw()

        hand_font = pygame.font.Font(pygame.font.get_default_font(), int(h*0.7))
        string = str(len(self.player_2.graveyard))
        hand_text = hand_font.render(string, True, (0,0,0))
        hand_rec = hand_text.get_rect()
        hand_rec.center = (x + (w/2), y + (h/2))
        self.display.blit(hand_text, hand_rec)



    def draw_card_display_sec(self):
        w = self.player_1_player_sec.w
        h = w*(88/63)
        x = self.player_1_player_sec.x
        y = (self.info_box_sec.y + self.info_box_sec.h)/2 - (h/2)
        colour = (100,0,100)

        self.card_display_sec = BoardSection(self.display, x, y, w, h, colour)
        self.card_display_sec.draw()



def main():
    display_size = display_width, display_height= (1600, 900)
    gameDisplay = pygame.display.set_mode(display_size)
    player_1 = player.Player("Sean")
    player_2 = player.Player("Kacper")

    f = open("../personal_decks/deck_3", "rb")
    player_deck = pickle.load(f)
    f.close()

    player_1.deck = deck.Deck("gablins", player_deck)
    player_2.deck = deck.Deck("gibluns", player_deck)

    for i in range(7):
        player_1.hand.append(player_1.deck.cards.pop(0))


    gameBoard = Board(gameDisplay, display_size, player_1, player_2)

    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        gameBoard.draw_board()
        pygame.display.update()



if __name__ == "__main__":
    main()
