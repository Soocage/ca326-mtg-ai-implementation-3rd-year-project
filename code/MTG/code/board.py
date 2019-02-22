import pygame
import re
import button
import time
import main_menu

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

    def __init__(self, screen, name, x, y, w, h, colour, is_border=True):
        self.screen = screen
        self.colour = colour
        self.name = name
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

    def draw_hand(self, player):
        cards = player.hand
        if player == self.player_1:
            PLAYER_1_HAND_SPRITE_CARD_GROUP.empty()
            if len(cards) <= 8:
                padding_w = (self.player_1_hand_box.w/8)/8
                card_h = (self.player_1_hand_box.h/10)*8
                card_w = (card_h*63)/88
            else:
                padding_w = (self.player_1_hand_box.w/(len(cards)+1))/(len(cards)+2)
                card_w = (self.player_1_hand_box.w/(len(cards)+1))
                card_h = card_w * (88/63)

            temp_sprite_list = []
            i = 0
            while i < len(cards):
                if i == 0:
                    x = (self.display_size[0]/2) - ((len(cards)-1)*(padding_w/2)) - ((len(cards)-1)*(card_w/2)) - (card_w/2)
                else:
                    x = temp_sprite_list[i-1].rect.x + card_w + padding_w
                y = self.player_1_hand_box.y + (self.player_1_hand_box.h - card_h)/2
                card_sprite = CardSprite(cards[i] , x, y, card_w, card_h)
                temp_sprite_list.append(card_sprite)
                PLAYER_1_HAND_SPRITE_CARD_GROUP.add(card_sprite)
                i += 1
            PLAYER_1_HAND_SPRITE_CARD_GROUP.draw(self.display)
        else:
            PLAYER_2_HAND_SPRITE_CARD_GROUP.empty()
            if len(cards) <= 8:
                padding_w = (self.player_1_hand_box.w/8)/8
                card_h = (self.player_1_hand_box.h/10)*8
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

        padding_w = (self.draw_search_box_w/11)/11
        upper_padding_h = (self.draw_search_box_h/7)/7
        card_h = (self.draw_search_box_h/7)
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
            x = (padding_w*i+1) + (card_w*i)
            y = (upper_padding_h)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.ADD(land_sprite)
        i = 0
        while i < len(row_2):
            land_card = row_1[i]
            x = (padding_w*i+1) + (card_w*i)
            y = (upper_padding_h*2) + card_h 
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.ADD(land_sprite)
        i = 0
        while i < len(row_3):
            land_card = row_1[i]
            x = (padding_w*i+1) + (card_w*i)
            y = (upper_padding_h*3) + (card_h*2)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.ADD(land_sprite)
        i = 0
        while i < len(row_4):
            land_card = row_1[i]
            x = (padding_w*i+1) + (card_w*i)
            y = (upper_padding_h*4) + (card_h*3)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.ADD(land_sprite)
        i = 0
        while i < len(row_5):
            land_card = row_1[i]
            x = (padding_w*i+1) + (card_w*i)
            y = (upper_padding_h*5) + (card_h*4)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.ADD(land_sprite)
        i = 0
        while i < len(row_6):
            land_card = row_1[i]
            x = (padding_w*i+1) + (card_w*i)
            y = (upper_padding_h*5) + (card_h*4)
            land_sprite = CardSprite(row_1[i], x, y, card_w, card_h)
            LAND_CARD_SPRITE_GROUP.ADD(land_sprite)
            
        LAND_CARD_SPRITE_GROUP.draw()

        pygame.display.update()


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
        (display_w, display_h) = self.display_size

        display.fill((255,255,255))



        ## Graveyards##########################################################################
        player_1_graveyard_x = 0
        player_1_graveyard_y = (display_h/16)*13
        player_1_graveyard_w = (display_w/8)
        player_1_graveyard_h = (display_h/16)*3
        player_1_graveyard_colour = (165, 165, 165)

        player_1_graveyard = BoardSection(display, "graveyard", player_1_graveyard_x, player_1_graveyard_y, player_1_graveyard_w, player_1_graveyard_h, player_1_graveyard_colour)
        self.player_1_graveyard = player_1_graveyard
        player_1_graveyard.draw()

        player_2_graveyard_x = player_1_graveyard_x
        player_2_graveyard_y = 0
        player_2_graveyard_w = player_1_graveyard_w
        player_2_graveyard_h = player_1_graveyard_h
        player_2_graveyard_colour = player_1_graveyard_colour

        player_2_graveyard = BoardSection(display, "graveyard", player_2_graveyard_x, player_2_graveyard_y, player_2_graveyard_w, player_2_graveyard_h, player_2_graveyard_colour)
        self.player_2_graveyard = player_2_graveyard
        player_2_graveyard.draw()

        player_1_graveyard_box_w = player_1_graveyard_w*(0.33)
        player_1_graveyard_box_h = player_1_graveyard_box_w*(88/63)
        player_1_graveyard_box_x = player_1_graveyard_x + (player_1_graveyard_w*(0.5))
        player_1_graveyard_box_y = player_1_graveyard_y + ((player_1_graveyard_h-player_1_graveyard_box_h)/2)
        player_1_graveyard_box_colour = (255,255,255)

        player_1_graveyard_box = BoardSection(display, "graveyard_box", player_1_graveyard_box_x, player_1_graveyard_box_y, player_1_graveyard_box_w, player_1_graveyard_box_h, player_1_graveyard_box_colour)
        player_1_graveyard_box.draw()

        player_2_graveyard_box_w = player_1_graveyard_box_w
        player_2_graveyard_box_h = player_1_graveyard_box_h
        player_2_graveyard_box_x = player_1_graveyard_box_x
        player_2_graveyard_box_y = player_2_graveyard_y + ((player_2_graveyard_h-player_2_graveyard_box_h)/2)
        player_2_graveyard_box_colour = player_1_graveyard_box_colour

        player_2_graveyard_box = BoardSection(display, "graveyard_box", player_2_graveyard_box_x, player_2_graveyard_box_y, player_2_graveyard_box_w, player_2_graveyard_box_h, player_2_graveyard_box_colour)
        player_2_graveyard_box.draw()

        graveyard_font = pygame.font.Font(pygame.font.get_default_font(), int(player_1_graveyard_h*0.5))

        player_1_graveyard_text = graveyard_font.render(str(len(player_1.graveyard)), False, (0,0,0))
        player_1_graveyard_text_rec = player_1_graveyard_text.get_rect()
        player_1_graveyard_text_rec.center = ((player_1_graveyard_x+(player_1_graveyard_w/4)), (player_1_graveyard_y+(player_1_graveyard_h/2)))
        display.blit(player_1_graveyard_text, player_1_graveyard_text_rec)

        player_2_graveyard_text = graveyard_font.render(str(len(player_2.graveyard)), False, (0,0,0))
        player_2_graveyard_text_rec = player_2_graveyard_text.get_rect()
        player_2_graveyard_text_rec.center = ((player_2_graveyard_x+(player_2_graveyard_w/4)), (player_2_graveyard_y+(player_2_graveyard_h/2)))
        display.blit(player_2_graveyard_text, player_2_graveyard_text_rec)

        #### Hands ####################################################
        player_1_hand_x = player_1_graveyard_x + player_1_graveyard_w
        player_1_hand_y = player_1_graveyard_y
        player_1_hand_w = (display_w/8)*6
        player_1_hand_h = player_1_graveyard_h
        player_1_hand_colour = (37, 236, 247)

        player_1_hand = BoardSection(display, "hand", player_1_hand_x, player_1_hand_y, player_1_hand_w, player_1_hand_h, player_1_hand_colour)
        self.player_1_hand_box = player_1_hand
        player_1_hand.draw()

        player_2_hand_x = player_2_graveyard_x + player_2_graveyard_w
        player_2_hand_y = player_2_graveyard_y
        player_2_hand_w = player_1_hand_w
        player_2_hand_h = player_1_hand_h
        player_2_hand_colour = player_1_hand_colour

        player_2_hand = BoardSection(display, "hand", player_2_hand_x, player_2_hand_y, player_2_hand_w, player_2_hand_h, player_2_hand_colour)
        self.player_2_hand_box = player_2_hand
        player_2_hand.draw()
        ###################################################################

       ## Decks ######################################################################################
        player_1_deck_x = player_1_hand_x + player_1_hand_w
        player_1_deck_y = player_1_hand_y
        player_1_deck_w = player_1_graveyard_w
        player_1_deck_h = player_1_graveyard_h
        player_1_deck_colour = (0, 165, 165)

        player_1_deck = BoardSection(display, "deck", player_1_deck_x, player_1_deck_y, player_1_deck_w, player_1_deck_h, player_1_deck_colour)
        self.player_1_deck = player_1_deck
        player_1_deck.draw()
        
        player_2_deck_x = player_1_deck_x
        player_2_deck_y = player_2_hand_y
        player_2_deck_w = player_1_deck_w
        player_2_deck_h = player_1_deck_h
        player_2_deck_colour = player_1_deck_colour

        player_2_deck = BoardSection(display, "deck", player_2_deck_x, player_2_deck_y, player_2_deck_w, player_2_deck_h, player_2_deck_colour)
        player_2_deck.draw()

        player_1_deck_box_w = player_1_graveyard_box_w
        player_1_deck_box_h = player_1_graveyard_box_h
        player_1_deck_box_x = player_1_deck_x + (player_1_deck_w*(0.5))
        player_1_deck_box_y = player_1_deck_y + ((player_1_deck_h-player_1_deck_box_h)/2)
        player_1_deck_box_colour = (255,255,255)

        player_1_deck_box = BoardSection(display, "deck_box", player_1_deck_box_x, player_1_deck_box_y, player_1_deck_box_w, player_1_deck_box_h, player_1_deck_box_colour)
        player_1_deck_box.draw()

        player_2_deck_box_w = player_1_deck_box_w
        player_2_deck_box_h = player_1_deck_box_h
        player_2_deck_box_x = player_1_deck_box_x
        player_2_deck_box_y = player_2_deck_y + ((player_2_deck_h-player_2_deck_box_h)/2)
        player_2_deck_box_colour = player_1_deck_box_colour

        player_2_deck_box = BoardSection(display, "deck_box", player_2_deck_box_x, player_2_deck_box_y, player_2_deck_box_w, player_2_deck_box_h, player_2_deck_box_colour)
        player_2_deck_box.draw()

        deck_font = pygame.font.Font(pygame.font.get_default_font(), int(player_1_deck_w*0.4))

        player_1_deck_text = deck_font.render(str(len(player_1.deck.cards)), False, (0,0,0))
        player_1_deck_text_rec = player_1_deck_text.get_rect()
        player_1_deck_text_rec.center = ((player_1_deck_x+(player_1_deck_w/4)), (player_1_deck_y+(player_1_deck_h/2)))
        display.blit(player_1_deck_text, player_1_deck_text_rec)

        player_2_deck_text = deck_font.render(str(len(player_2.deck.cards)), False, (0,0,0))
        player_2_deck_text_rec = player_2_deck_text.get_rect()
        player_2_deck_text_rec.center = ((player_2_deck_x+(player_2_deck_w/4)), (player_2_deck_y+(player_2_deck_h/2)))
        display.blit(player_2_deck_text, player_2_deck_text_rec)
        #############################################################################################################################

        ## Lands ###########################################################
        player_1_lands_x = 0
        player_1_lands_y = (display_h/16)*11
        player_1_lands_w = (display_w/8)*7
        player_1_lands_h = display_h - player_1_lands_y - player_1_graveyard_h
        player_1_lands_colour = (178, 255, 102)

        player_1_lands = BoardSection(display, "lands", player_1_lands_x, player_1_lands_y, player_1_lands_w, player_1_lands_h, player_1_lands_colour)
        self.player_1_land_box = player_1_lands
        player_1_lands.draw()

        player_2_lands_x = 0
        player_2_lands_y = (display_h/16)*3
        player_2_lands_w = player_1_lands_w
        player_2_lands_h = player_1_lands_h
        player_2_lands_colour = player_1_lands_colour

        player_2_lands = BoardSection(display, "lands", player_1_lands_x, player_2_lands_y, player_2_lands_w, player_2_lands_h, player_2_lands_colour)
        self.player_2_land_box = player_2_lands
        player_2_lands.draw()
        #######################################################################

       ## Life Sections ####################################################################################################
        player_1_life_sec_x = player_1_lands_x + player_1_lands_w
        player_1_life_sec_y = player_1_lands_y
        player_1_life_sec_w = player_1_deck_w
        player_1_life_sec_h = player_1_lands_h
        player_1_life_sec_colour = (91, 252, 177)

        player_1_life_sec = BoardSection(display, "life_sec", player_1_life_sec_x, player_1_life_sec_y, player_1_life_sec_w, player_1_life_sec_h, player_1_life_sec_colour)
        self.player_1_life_sec = player_1_life_sec
        player_1_life_sec.draw()

        player_2_life_sec_x = player_1_life_sec_x
        player_2_life_sec_y = player_2_lands_y
        player_2_life_sec_w = player_1_life_sec_w
        player_2_life_sec_h = player_1_life_sec_h
        player_2_life_sec_colour = player_1_life_sec_colour

        player_2_life_sec = BoardSection(display, "life_sec", player_2_life_sec_x, player_2_life_sec_y, player_2_life_sec_w, player_2_life_sec_h, player_2_life_sec_colour)
        self.player_2_life_sec = player_2_life_sec
        player_2_life_sec.draw()

        player_1_life_w = (player_1_life_sec_w*0.5)
        player_1_life_h = player_1_life_w
        player_1_life_x = player_1_life_sec_x + (player_1_life_w/2)
        player_1_life_y = player_1_life_sec.y + ((player_1_life_sec.h - player_1_life_h) / 2)
        player_1_life_colour = (255, 255, 255)

        player_1_life = BoardSection(display, "life", player_1_life_x, player_1_life_y, player_1_life_w, player_1_life_h, player_1_life_colour)
        player_1_life.draw()

        player_2_life_w = player_1_life_w
        player_2_life_h = player_2_life_w
        player_2_life_x = player_1_life_x
        player_2_life_y = player_2_life_sec_y + ((player_2_life_sec_h - player_2_life_h) / 2)
        player_2_life_colour = player_1_life_colour

        player_2_life = BoardSection(display, "life", player_2_life_x, player_2_life_y, player_2_life_w, player_2_life_h, player_2_life_colour)
        player_2_life.draw()

        life_font = pygame.font.Font(pygame.font.get_default_font(), int(player_1_life.h*0.5))

        player_1_life_text = life_font.render(str(player_1.life), False, (0,0,0))
        player_1_life_rec = player_1_life_text.get_rect()
        player_1_life_rec.center = ((player_1_life_sec_x+(player_1_life_sec_w/2)), (player_1_life_sec_y+(player_1_life_sec_h/2)))
        display.blit(player_1_life_text, player_1_life_rec)

        player_2_life_text = life_font.render(str(player_2.life), False, (0,0,0))
        player_2_life_rec = player_2_life_text.get_rect()
        player_2_life_rec.center = ((player_2_life_sec_x+(player_2_life_sec_w/2)), (player_2_life_sec_y+(player_2_life_sec_h/2)))
        display.blit(player_2_life_text, player_2_life_rec)
        ###################################################################################################################

        ## Battlefields####################################################################
        player_1_battlefield_x = 0
        player_1_battlefield_y = display_h/2
        player_1_battlefield_w = display_w
        player_1_battlefield_h = (display_h/2) - player_1_graveyard_h - player_1_lands_h
        player_1_battlefield_colour = (211, 132, 6)

        player_1_battlefield = BoardSection(display, "battlefield", player_1_battlefield_x, player_1_battlefield_y, player_1_battlefield_w, player_1_battlefield_h, player_1_battlefield_colour)
        self.player_1_battlefield_box = player_1_battlefield
        player_1_battlefield.draw()

        player_2_battlefield_x = 0
        player_2_battlefield_y = player_2_graveyard_h + player_2_lands_h
        player_2_battlefield_w = player_1_battlefield_w
        player_2_battlefield_h = player_1_battlefield_h
        player_2_battlefield_colour = player_1_battlefield_colour

        player_2_battlefield = BoardSection(display, "battlefield", player_2_battlefield_x, player_2_battlefield_y, player_2_battlefield_w, player_2_battlefield_h, player_2_battlefield_colour)
        self.player_2_battlefield_box = player_2_battlefield
        player_2_battlefield.draw()
        ##############

        ## MANA POOL ##################################################################

        mana_pool_h = (player_1_battlefield_h/5)
        mana_pool_w = ((player_1_battlefield_w/4)/5)
        player_1_r_mana_pool_x = ((player_1_battlefield_w - (mana_pool_w*5))/2)
        player_1_r_mana_pool_y = player_1_lands_y - mana_pool_h

        player_1_g_mana_pool_x = player_1_r_mana_pool_x + mana_pool_w
        player_1_g_mana_pool_y = player_1_r_mana_pool_y

        player_1_u_mana_pool_x = player_1_g_mana_pool_x + mana_pool_w
        player_1_u_mana_pool_y = player_1_g_mana_pool_y

        player_1_w_mana_pool_x = player_1_u_mana_pool_x + mana_pool_w
        player_1_w_mana_pool_y = player_1_u_mana_pool_y

        player_1_b_mana_pool_x = player_1_w_mana_pool_x + mana_pool_w
        player_1_b_mana_pool_y = player_1_w_mana_pool_y

        player_1_r_mana_pool_sec = BoardSection(display, "mana_r", player_1_r_mana_pool_x, player_1_r_mana_pool_y, mana_pool_w, mana_pool_h, (200,0,0))
        player_1_r_mana_pool_sec.draw()

        player_1_g_mana_pool_sec = BoardSection(display, "mana_r", player_1_g_mana_pool_x, player_1_g_mana_pool_y, mana_pool_w, mana_pool_h, (0,200,0))
        player_1_g_mana_pool_sec.draw()

        player_1_u_mana_pool_sec = BoardSection(display, "mana_r", player_1_u_mana_pool_x, player_1_u_mana_pool_y, mana_pool_w, mana_pool_h, (0,102,204))
        player_1_u_mana_pool_sec.draw()

        player_1_w_mana_pool_sec = BoardSection(display, "mana_r", player_1_w_mana_pool_x, player_1_w_mana_pool_y, mana_pool_w, mana_pool_h, (255,255,204))
        player_1_w_mana_pool_sec.draw()

        player_1_b_mana_pool_sec = BoardSection(display, "mana_r", player_1_b_mana_pool_x, player_1_b_mana_pool_y, mana_pool_w, mana_pool_h, (122,0,122))
        player_1_b_mana_pool_sec.draw()

        player_2_r_mana_pool_x = player_1_r_mana_pool_x
        player_2_r_mana_pool_y = player_2_battlefield_y

        player_2_g_mana_pool_x = player_2_r_mana_pool_x + mana_pool_w
        player_2_g_mana_pool_y = player_2_r_mana_pool_y

        player_2_u_mana_pool_x = player_2_g_mana_pool_x + mana_pool_w
        player_2_u_mana_pool_y = player_2_g_mana_pool_y

        player_2_w_mana_pool_x = player_2_u_mana_pool_x + mana_pool_w
        player_2_w_mana_pool_y = player_2_u_mana_pool_y

        player_2_b_mana_pool_x = player_2_w_mana_pool_x + mana_pool_w
        player_2_b_mana_pool_y = player_2_w_mana_pool_y

        player_2_r_mana_pool_sec = BoardSection(display, "mana_r", player_2_r_mana_pool_x, player_2_r_mana_pool_y, mana_pool_w, mana_pool_h, (200,0,0))
        player_2_r_mana_pool_sec.draw()

        player_2_g_mana_pool_sec = BoardSection(display, "mana_r", player_2_g_mana_pool_x, player_2_g_mana_pool_y, mana_pool_w, mana_pool_h, (0,200,0))
        player_2_g_mana_pool_sec.draw()

        player_2_u_mana_pool_sec = BoardSection(display, "mana_r", player_2_u_mana_pool_x, player_2_u_mana_pool_y, mana_pool_w, mana_pool_h, (0,102,204))
        player_2_u_mana_pool_sec.draw()

        player_2_w_mana_pool_sec = BoardSection(display, "mana_r", player_2_w_mana_pool_x, player_2_w_mana_pool_y, mana_pool_w, mana_pool_h, (255,255,204))
        player_2_w_mana_pool_sec.draw()

        player_2_b_mana_pool_sec = BoardSection(display, "mana_r", player_2_b_mana_pool_x, player_2_b_mana_pool_y, mana_pool_w, mana_pool_h, (122,0,122))
        player_2_b_mana_pool_sec.draw()

        mana_font = pygame.font.Font(pygame.font.get_default_font(), int(mana_pool_h*0.45))


        player_1_mana = self.player_1.mana

        player_1_r = len(re.findall("R", player_1_mana))

        player_1_r_mana_text = life_font.render(str(player_1_r), False, (0,0,0))
        player_1_r_mana_rec = player_1_r_mana_text.get_rect()
        player_1_r_mana_rec.center = ((player_1_r_mana_pool_x+(mana_pool_w/2)), (player_1_r_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_1_r_mana_text, player_1_r_mana_rec)

        player_1_g = len(re.findall("G", player_1_mana))

        player_1_g_mana_text = life_font.render(str(player_1_g), False, (0,0,0))
        player_1_g_mana_rec = player_1_g_mana_text.get_rect()
        player_1_g_mana_rec.center = ((player_1_g_mana_pool_x+(mana_pool_w/2)), (player_1_g_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_1_g_mana_text, player_1_g_mana_rec)

        player_1_u = len(re.findall("U", player_1_mana))

        player_1_u_mana_text = life_font.render(str(player_1_u), False, (0,0,0))
        player_1_u_mana_rec = player_1_u_mana_text.get_rect()
        player_1_u_mana_rec.center = ((player_1_u_mana_pool_x+(mana_pool_w/2)), (player_1_u_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_1_u_mana_text, player_1_u_mana_rec)

        player_1_w = len(re.findall("W", player_1_mana))

        player_1_w_mana_text = life_font.render(str(player_1_w), False, (0,0,0))
        player_1_w_mana_rec = player_1_w_mana_text.get_rect()
        player_1_w_mana_rec.center = ((player_1_w_mana_pool_x+(mana_pool_w/2)), (player_1_w_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_1_w_mana_text, player_1_w_mana_rec)

        player_1_b = len(re.findall("B", player_1_mana))

        player_1_b_mana_text = life_font.render(str(player_1_b), False, (0,0,0))
        player_1_b_mana_rec = player_1_b_mana_text.get_rect()
        player_1_b_mana_rec.center = ((player_1_b_mana_pool_x+(mana_pool_w/2)), (player_1_b_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_1_b_mana_text, player_1_b_mana_rec)

        player_2_mana = self.player_2.mana

        player_2_r = len(re.findall("R", player_2_mana))

        player_2_r_mana_text = life_font.render(str(player_2_r), False, (0,0,0))
        player_2_r_mana_rec = player_2_r_mana_text.get_rect()
        player_2_r_mana_rec.center = ((player_2_r_mana_pool_x+(mana_pool_w/2)), (player_2_r_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_2_r_mana_text, player_2_r_mana_rec)

        player_2_g = len(re.findall("G", player_2_mana))

        player_2_g_mana_text = life_font.render(str(player_2_g), False, (0,0,0))
        player_2_g_mana_rec = player_2_g_mana_text.get_rect()
        player_2_g_mana_rec.center = ((player_2_g_mana_pool_x+(mana_pool_w/2)), (player_2_g_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_2_g_mana_text, player_2_g_mana_rec)

        player_2_u = len(re.findall("U", player_2_mana))

        player_2_u_mana_text = life_font.render(str(player_2_u), False, (0,0,0))
        player_2_u_mana_rec = player_2_u_mana_text.get_rect()
        player_2_u_mana_rec.center = ((player_2_u_mana_pool_x+(mana_pool_w/2)), (player_2_u_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_2_u_mana_text, player_2_u_mana_rec)

        player_2_w = len(re.findall("W", player_2_mana))

        player_2_w_mana_text = life_font.render(str(player_2_w), False, (0,0,0))
        player_2_w_mana_rec = player_2_w_mana_text.get_rect()
        player_2_w_mana_rec.center = ((player_2_w_mana_pool_x+(mana_pool_w/2)), (player_2_w_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_2_w_mana_text, player_2_w_mana_rec)

        player_2_b = len(re.findall("B", player_2_mana))

        player_2_b_mana_text = life_font.render(str(player_2_b), False, (0,0,0))
        player_2_b_mana_rec = player_2_b_mana_text.get_rect()
        player_2_b_mana_rec.center = ((player_2_b_mana_pool_x+(mana_pool_w/2)), (player_2_b_mana_pool_y+(mana_pool_h/2)))
        display.blit(player_2_b_mana_text, player_2_b_mana_rec)










