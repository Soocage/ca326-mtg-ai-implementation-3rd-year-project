import sys
sys.path.append('./code')
sys.path.append('./images')
sys.path.append('./personal_decks')
sys.path.append('./sound')
sys.path.append('./testing')



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
                card_texture = pygame.image.load(card.texture)
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
        self.player_1_battlefield_sec = None
        self.player_2_battlefield_sec = None


    def draw_hand(self, player):
        cards = player.hand
        print(cards)
        for card in cards:
            print(card.name)
        if player == self.player_1:
            PLAYER_1_HAND_SPRITE_CARD_GROUP.empty()
            if len(cards) <= 8:
                padding_w = (self.player_hand_sec.w/8)/8
                card_h = (self.player_hand_sec.h/10)*8
                card_w = (card_h*63)/88
            else:
                padding_w = (self.player_hand_sec.w/(len(cards)+1))/(len(cards)+2)
                card_w = (self.player_hand_sec.w/(len(cards)+1))
                card_h = card_w * (88/63)

            temp_sprite_list = []
            i = 0
            while i < len(cards):
                if i == 0:
                    x = (self.display_size[0]/2) - ((len(cards)-1)*(padding_w/2)) - ((len(cards)-1)*(card_w/2)) - (card_w/2)
                else:
                    x = temp_sprite_list[i-1].rect.x + card_w + padding_w
                y = self.player_hand_sec.y + (self.player_hand_sec.h - card_h)/2
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
        self.draw_player_1_battlefield()
        self.draw_player_2_battlefield()
        self.draw_hand(player_1)
        self.





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
        hand_section_y = self.display_h * (3/4)
        hand_section_w = self.display_w - self.menu_box_sec.w
        hand_section_h = self.display_h * (1/4)
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

    def draw_player_1_battlefield(self):
        player_1_battlefield_x = self.player_hand_sec.x
        player_1_battlefield_h = (self.display_h - (self.player_hand_sec.h + self.phase_box_sec.h)) / 2
        player_1_battlefield_y = self.phase_box_sec.y - player_1_battlefield_h
        player_1_battlefield_w = self.player_hand_sec.w
        player_1_battlefield_colour = RED

        self.player_1_battlefield_sec = BoardSection(self.display, player_1_battlefield_x, player_1_battlefield_y, player_1_battlefield_w, player_1_battlefield_h, player_1_battlefield_colour)
        self.player_1_battlefield_sec.draw()

    def draw_player_2_battlefield(self):
        player_2_battlefield_x = self.player_hand_sec.x
        player_2_battlefield_h = (self.display_h - (self.player_hand_sec.h + self.phase_box_sec.h)) / 2
        player_2_battlefield_y = 0
        player_2_battlefield_w = self.player_hand_sec.w
        player_2_battlefield_colour = RED

        self.player_2_battlefield_sec = BoardSection(self.display, player_2_battlefield_x, player_2_battlefield_y, player_2_battlefield_w, player_2_battlefield_h, player_2_battlefield_colour)
        self.player_2_battlefield_sec.draw()





def main():
    display_size = display_width, display_height= (1600, 900)
    gameDisplay = pygame.display.set_mode(display_size)
    player_1 = player.Player("Sean")
    player_2 = player.Player("Kacper")

    f = open("./personal_decks/deck_3", "rb")
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
