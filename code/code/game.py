import pygame
import sys
import player
import board
import deck
import pickle
import card
from random import shuffle
import random
import time
import copy
from screen_res import screen_res
import ai


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
cusror = None
bounce_icon = None



cursor = pygame.image.load('./images/crosshair.png')
cursor_w = 100
cursor_h = 100
cursor = pygame.transform.smoothscale(cursor, (cursor_w, cursor_h))




class Game():

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.phase = "untap"
        self.turn = 0
        self.current_player = None
        self.quit = False
        self.stacked_card = None

    def run_game(self):
        player_1_deck_list = self.deck_selection(self.player_1)
        player_2_deck_list = self.deck_selection(self.player_2)

        self.player_1.deck = deck.Deck("gablins", player_1_deck_list)
        self.player_2.deck = deck.Deck("gibluns", player_2_deck_list)

        self.shuffle_deck(self.player_1)
        self.shuffle_deck(self.player_2)

        gameBoard = board.Board(self.player_1, self.player_2)

        mulligan_counter = 7

        self.deal_cards(self.player_1, mulligan_counter)
        self.deal_cards(self.player_2, mulligan_counter)

        gameBoard.calc_board()
        self.draw_screen(gameBoard)
        gameBoard.draw_hand()
        self.mulligan(gameBoard, self.player_1, mulligan_counter, self.player_2)
        gameBoard.draw_indicator(self.player_1)
        pygame.display.update()

        self.current_player = random.choice([self.player_1, self.player_2])


        turn_counter = 1
        self.game_loop(gameBoard, turn_counter)
    def game_loop(self, gameBoard, turn_counter):
        while self.check_game_status():


            ########### TURNS LOGIC ################
            gameBoard.draw_indicator(self.player_1)
            self.untap(self.player_1, gameBoard)
            time.sleep(0.5)
            if turn_counter != 1:
                self.draw(self.player_1, gameBoard)
            time.sleep(0.5)
            self.main_phase(self.player_1, self.player_2, gameBoard)
            self.combat_phase(self.player_1, self.player_2, gameBoard)
            self.main_phase(self.player_1, self.player_2, gameBoard)
            self.end_step(gameBoard, self.player_1)


            gameBoard.draw_indicator(self.player_2)
            self.untap(self.player_2,gameBoard)
            time.sleep(0.5)
            self.draw(self.player_2, gameBoard)
            time.sleep(0.5)
            self.main_phase(self.player_2, self.player_1, gameBoard)
            time.sleep(0.5)
            self.combat_phase(self.player_2, self.player_1, gameBoard)
            board.BATTELING_CREATURE_ATT.empty()
            board.BATTELING_CREATURE_DEF.empty()
            time.sleep(0.5)
            self.end_step(gameBoard, self.player_2)
            time.sleep(0.5)
            turn_counter += 1

############################# UPDATING SCREEN ######################################


    def mulligan(self, gameBoard, player, mulligan_counter, next_player):
        resolved = False
        while not resolved:
            gameBoard.draw_mulligan()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.my_quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:

                        if gameBoard.concede_button_sec.x < pos[0] < gameBoard.concede_button_sec.x + gameBoard.concede_button_sec.w and gameBoard.concede_button_sec.y < pos[1] < gameBoard.concede_button_sec.y + gameBoard.concede_button_sec.h:
                            self.quit = True
                            resolved = True

                        if gameBoard.options_button_sec.x < pos[0] < gameBoard.options_button_sec.x + gameBoard.options_button_sec.w and gameBoard.options_button_sec.y < pos[1] < gameBoard.options_button_sec.y + gameBoard.options_button_sec.h:

                            gameBoard.draw_options_menu()
                            gameBoard.calc_board()
                            gameBoard.draw_board(self.phase)
                            gameBoard.draw_hand()
                            gameBoard.draw_land(player)
                            gameBoard.draw_land(next_player)
                            gameBoard.draw_new_battlefield(player)
                            gameBoard.draw_new_battlefield(next_player)
                            pygame.display.update()


                        for button in board.MULLIGAN_BUTTONS:
                            if button.rect.collidepoint(pos):
                                if button.action == "yes":
                                    for card in player.hand:
                                        player.deck.cards.append(card)
                                    player.hand = []
                                    self.shuffle_deck(player)
                                    mulligan_counter -= 1
                                    self.deal_cards(player, mulligan_counter)
                                    gameBoard.draw_hand()
                                    if mulligan_counter != 1:
                                        self.mulligan(gameBoard, player, mulligan_counter, next_player)
                                    return
                                if button.action == "no":
                                    resolved = True
                gameBoard.draw_player_hand_section()
                gameBoard.draw_hand()
                pygame.display.update()

    def end_step(self, gameBoard, player):
        self.phase = "end"
        gameBoard.draw_phase_section(self.phase)
        pygame.display.update()
        self.player_1.state = ""
        self.player_2.state = ""
        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            card.card.toughness_modifier = 0
            card.card.power_modifier = 0
            card.card.tmp_keyword = ""
            card.card.combat_state = ""
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            card.card.toughness_modifier = 0
            card.card.power_modifier = 0
            card.card.tmp_keyword = ""
            card.card.combat_state = ""

        while len(player.hand) > 7:
            self.discard_down(player, gameBoard)

    def discard_down(self, player, gameBoard):
        if player.name != "AI_Dusty":
            resolved = False
            gameBoard.draw_discard()
            pygame.display.update()
            while not resolved:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()

                            for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos):
                                    player.graveyard.append(card.card)
                                    player.hand.remove(card.card)
                                    gameBoard.draw_board(self.phase)
                                    resolved = True
        else:
            player.graveyard.append(player.hand[0])
            player.hand.remove(player.hand[0])
            gameBoard.draw_board(self.phase)
        gameBoard.draw_hand()
        gameBoard.draw_land(self.player_1)
        gameBoard.draw_land(self.player_2)
        gameBoard.draw_new_battlefield(self.player_1)
        gameBoard.draw_new_battlefield(self.player_2)




    def check_game_status(self):
        lives = self.check_life()
        deck_1 = self.check_not_mill(self.player_1)
        deck_2 = self.check_not_mill(self.player_2)

        return lives and (deck_1 and deck_2) and self.quit != True

    def check_life(self):
        return self.player_1.life > 0 and self.player_2.life > 0

    def check_not_mill(self, player):
        return len(player.deck.cards) > 0


    def deck_selection(self, player):

        f = open("./personal_decks/deck_2", "rb")

        player_deck = pickle.load(f)
        print(player_deck)
        f.close()
        return player_deck

    def shuffle_deck(self, player):
        shuffle(player.deck.cards)

    def deal_cards(self, player, mulligan_counter):
        for i in range(mulligan_counter):
            player.hand.append(player.deck.cards.pop(0))

    def draw(self, player, gameBoard):
        self.phase = "draw"
        gameBoard.draw_phase_section(self.phase)
        if self.stacked_card != None:
            gameBoard.stacked_card(self.stacked_card)
        pygame.display.update()


        if self.check_not_mill(player):
            player.hand.append(player.deck.cards.pop(0))
            gameBoard.draw_hand()
            gameBoard.draw_player_hand_section()

    def untap(self, player, gameBoard):
        self.phase = "untap"
        gameBoard.draw_phase_section(self.phase)
        if self.stacked_card != None:
            gameBoard.stacked_card(self.stacked_card)
        pygame.display.update()


        for creature in player.battlefield:
            creature.tapped = False
            creature.summon_sick = False

        for land in player.land_zone:
            land.tapped = False



        gameBoard.draw_land(player)
        gameBoard.draw_new_battlefield(player)
        player.land_flag = False
        self.clear_mana(player)

    def add_mana(self, player, land):
        land.tapped = True
        player.mana += land.colour
        player.mana = "".join(sorted(player.mana))

    def main_phase(self, current_player, next_player, gameBoard):
        if self.phase == "combat":
            self.phase = "main_2"
        else:
            self.phase = "main_1"
        self.draw_screen(gameBoard)
        if self.stacked_card != None:
            gameBoard.stacked_card(self.stacked_card)
        gameBoard.draw_indicator(current_player)
        pygame.display.update()
        if self.check_life() and not self.quit:
            if current_player.name != "AI_Dusty":
                pass_phase = False
                while not pass_phase:
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()

                        if event.type == pygame.QUIT:
                            self.my_quit()

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_SPACE:
                                pass_phase = True

                            if event.key == pygame.K_ESCAPE:
                                self.quit = True
                                return

                        if event.type == pygame.MOUSEBUTTONDOWN:

                            if event.button == 1:
                                if gameBoard.concede_button_sec.x < pos[0] < gameBoard.concede_button_sec.x + gameBoard.concede_button_sec.w and gameBoard.concede_button_sec.y < pos[1] < gameBoard.concede_button_sec.y + gameBoard.concede_button_sec.h:
                                    self.quit = True
                                    pass_phase = True

                                if gameBoard.options_button_sec.x < pos[0] < gameBoard.options_button_sec.x + gameBoard.options_button_sec.w and gameBoard.options_button_sec.y < pos[1] < gameBoard.options_button_sec.y + gameBoard.options_button_sec.h:

                                    gameBoard.draw_options_menu()
                                    gameBoard.calc_board()
                                    gameBoard.draw_board(self.phase)
                                    gameBoard.draw_hand()
                                    gameBoard.draw_land(current_player)
                                    gameBoard.draw_land(next_player)
                                    gameBoard.draw_new_battlefield(current_player)
                                    gameBoard.draw_new_battlefield(next_player)
                                    pygame.display.update()

                                if gameBoard.pass_button_sec.x < pos[0] < gameBoard.pass_button_sec.x + gameBoard.pass_button_sec.w and gameBoard.pass_button_sec.y < pos[1] < gameBoard.pass_button_sec.y + gameBoard.pass_button_sec.h:
                                    pass_phase = True

                                for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        card.clicked = True

                                if gameBoard.player_1_land_sec.x + gameBoard.player_1_land_sec.w > pos[0] > gameBoard.player_1_land_sec.x and gameBoard.player_1_land_sec.y + gameBoard.player_1_land_sec.h > pos[1] > gameBoard.player_1_land_sec.y:
                                    for land in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:

                                        if land.rect.collidepoint(pos) and land.card.tapped == False:
                                            self.add_mana(current_player, land.card)
                                            gameBoard.tap_mana(land)

                        if event.type == pygame.MOUSEBUTTONUP:

                            for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                if card.clicked == True:
                                    self.draw_screen(gameBoard)
                                    gameBoard.draw_indicator(self.player_1)
                                    card.clicked = False

                                    if ((gameBoard.player_hand_sec.x > card.rect.x) or (card.rect.x > gameBoard.player_hand_sec.x + gameBoard.player_hand_sec.w)) or gameBoard.player_hand_sec.y > card.rect.y:

                                        if card.card.card_type == "Land":
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            pygame.display.update()
                                            self.play_a_land(card.card, current_player, gameBoard)


                                        if card.card.card_type == "Creature" and self.check_mana(current_player, card.card):
                                            indx = current_player.hand.index(card.card)
                                            current_player.hand.pop(indx)
                                            self.response(next_player, current_player, gameBoard)
                                            current_player.battlefield.append(card.card)
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            gameBoard.draw_indicator(self.player_1)
                                            self.play_a_creature(card.card, current_player,next_player, gameBoard)

                                        if (card.card.card_type == "Sorcery" or card.card.card_type == "Instant") and self.check_mana(current_player, card.card):
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            current_player.hand.remove(card.card) #####
                                            current_player.graveyard.append(card.card)######
                                            gameBoard.draw_hand()
                                            self.response(next_player, current_player, gameBoard)
                                            self.play_a_sorcery_or_instant(card.card, current_player, next_player, gameBoard)
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            gameBoard.draw_indicator(self.player_1)

                                        if self.check_life() == False:
                                            return

                                        self.draw_screen(gameBoard)
                                        gameBoard.stacked_card(self.stacked_card)
                                        gameBoard.draw_indicator(self.player_1)
                                        pygame.display.update()
                                    gameBoard.draw_hand()


                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                            if card.clicked == True:
                                pos = pygame.mouse.get_pos()
                                card.rect.x = pos[0] - (card.rect.width/2)
                                card.rect.y = pos[1] - (card.rect.height/2)
                                pos, card.rect.x, card.rect.y

                        self.draw_screen(gameBoard)
                        if self.stacked_card != None:
                            gameBoard.stacked_card(self.stacked_card)
                        gameBoard.draw_indicator(self.player_1)
                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()


                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                        for card in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                        for card in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                    clock.tick(60)
            else:
                self.player_2.play_land()
                gameBoard.draw_land(current_player)
                cards_to_be_played = self.player_2.play_a_card(gameBoard, next_player)
                for card in cards_to_be_played:
                    if card.card_type == "Creature" and self.player_2.check_card_playable(card):
                        mana_to_be_tapped = self.player_2.check_card_cost(card)
                        i = 0
                        for land_sprite in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
                            if i < mana_to_be_tapped and land_sprite.card.tapped == False:
                                self.add_mana(current_player, land_sprite.card)
                                gameBoard.tap_mana(land_sprite)
                                gameBoard.draw_board(self.phase)
                                gameBoard.draw_land(current_player)
                                i += 1
                        self.stacked_card = card
                        gameBoard.stacked_card(self.stacked_card)
                        current_player.hand.remove(card)
                        self.response(next_player, current_player, gameBoard)
                        current_player.battlefield.append(card)
                        self.play_a_creature(card, current_player, next_player, gameBoard)
                        self.clear_mana(current_player)
                        self.stacked_card = card
                        gameBoard.stacked_card(self.stacked_card)
                        gameBoard.draw_indicator(self.player_2)

                    elif (card.card_type == "Instant" or card.card_type == "Sorcery") and self.player_2.check_card_playable(card):
                        mana_to_be_tapped = self.player_2.check_card_cost(card)
                        i = 0
                        for land_sprite in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
                            if i < mana_to_be_tapped and land_sprite.card.tapped == False:
                                self.add_mana(current_player, land_sprite.card)
                                gameBoard.tap_mana(land_sprite)
                                gameBoard.draw_board(self.phase)
                                gameBoard.draw_land(current_player)
                                i += 1
                        self.stacked_card = card
                        gameBoard.stacked_card(self.stacked_card)
                        current_player.hand.remove(card) #####
                        current_player.graveyard.append(card)######
                        self.response(next_player, current_player, gameBoard)
                        self.play_a_sorcery_or_instant(card, current_player, next_player, gameBoard, cards_to_be_played)
                        self.clear_mana(current_player)
                        self.stacked_card = card
                        gameBoard.stacked_card(self.stacked_card)
                        gameBoard.draw_indicator(self.player_2)

            self.clear_mana(current_player)


    def response(self, current_player, opponent, gameBoard):
        self.draw_screen(gameBoard)
        if self.stacked_card != None:
            gameBoard.stacked_card(self.stacked_card)
        gameBoard.draw_indicator(current_player, True)
        pygame.display.update()
        if current_player.name != "AI_Dusty":
            if self.check_instant(current_player.hand):
                pass_phase = False
                while not pass_phase:
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()

                        if event.type == pygame.QUIT:
                            self.my_quit()

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_SPACE:
                                pass_phase = True

                            if event.key == pygame.K_ESCAPE:
                                self.quit = True
                                return

                        if event.type == pygame.MOUSEBUTTONDOWN:

                            if event.button == 1:
                                if gameBoard.concede_button_sec.x < pos[0] < gameBoard.concede_button_sec.x + gameBoard.concede_button_sec.w and gameBoard.concede_button_sec.y < pos[1] < gameBoard.concede_button_sec.y + gameBoard.concede_button_sec.h:
                                    self.quit = True
                                    pass_phase = True

                                if gameBoard.options_button_sec.x < pos[0] < gameBoard.options_button_sec.x + gameBoard.options_button_sec.w and gameBoard.options_button_sec.y < pos[1] < gameBoard.options_button_sec.y + gameBoard.options_button_sec.h:

                                    gameBoard.draw_options_menu()
                                    gameBoard.calc_board()
                                    gameBoard.draw_board(self.phase)
                                    gameBoard.draw_hand()
                                    gameBoard.draw_land(current_player)
                                    gameBoard.draw_land(opponent)
                                    gameBoard.draw_new_battlefield(current_player)
                                    gameBoard.draw_new_battlefield(opponent)
                                    pygame.display.update()

                                if gameBoard.pass_button_sec.x < pos[0] < gameBoard.pass_button_sec.x + gameBoard.pass_button_sec.w and gameBoard.pass_button_sec.y < pos[1] < gameBoard.pass_button_sec.y + gameBoard.pass_button_sec.h:
                                    pass_phase = True

                                for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        card.clicked = True

                                if gameBoard.player_1_land_sec.x + gameBoard.player_1_land_sec.w > pos[0] > gameBoard.player_1_land_sec.x and gameBoard.player_1_land_sec.y + gameBoard.player_1_land_sec.h > pos[1] > gameBoard.player_1_land_sec.y:
                                    for land in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:

                                        if land.rect.collidepoint(pos) and land.card.tapped == False:
                                            self.add_mana(current_player, land.card)
                                            gameBoard.tap_mana(land)

                        if event.type == pygame.MOUSEBUTTONUP:

                            for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                if card.clicked == True:
                                    self.draw_screen(gameBoard)
                                    gameBoard.stacked_card(self.stacked_card)
                                    gameBoard.draw_indicator(self.player_1, True)
                                    card.clicked = False

                                    if ((gameBoard.player_hand_sec.x > card.rect.x) or (card.rect.x > gameBoard.player_hand_sec.x + gameBoard.player_hand_sec.w)) or gameBoard.player_hand_sec.y > card.rect.y:


                                        if card.card.card_type == "Instant" and self.check_mana(current_player, card.card):
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            current_player.hand.remove(card.card) #####
                                            current_player.graveyard.append(card.card)######
                                            gameBoard.draw_hand()
                                            self.response(opponent, current_player, gameBoard)
                                            self.stacked_card = card.card
                                            gameBoard.stacked_card(self.stacked_card)
                                            self.play_a_sorcery_or_instant(card.card, current_player, opponent, gameBoard)

                                            pass_phase = True

                                        if self.check_life() == False:
                                            return

                                        self.draw_screen(gameBoard)
                                        gameBoard.stacked_card(self.stacked_card)
                                        gameBoard.draw_indicator(self.player_1, True)
                                        pygame.display.update()
                                    gameBoard.draw_hand()


                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                            if card.clicked == True:
                                pos = pygame.mouse.get_pos()
                                card.rect.x = pos[0] - (card.rect.width/2)
                                card.rect.y = pos[1] - (card.rect.height/2)
                                pos, card.rect.x, card.rect.y

                        self.draw_screen(gameBoard)
                        gameBoard.stacked_card(self.stacked_card)
                        gameBoard.draw_indicator(self.player_1, True)
                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()


                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                        for card in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

                        for card in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                gameBoard.view_card(card.card)
                                pygame.display.update()

        else:

            if self.check_instant(current_player.hand):
                valid_cards = [card for card in self.player_2.hand if card.card_type == "Instant"]
                card = self.select_card(valid_cards)
                if card.effect == "Exile":
                    if len(self.player_1.battlefield) > 0:
                        if self.check_lands(card, gameBoard):
                            self.clear_mana(self.player_2)
                            self.stacked_card = card
                            gameBoard.stacked_card(self.stacked_card)
                            current_player.hand.remove(card)
                            current_player.graveyard.append(card)
                            self.response(self.player_1, self.player_2, gameBoard)
                            gameBoard.draw_board(self.phase)
                            self.stacked_card = card
                            gameBoard.stacked_card(self.stacked_card)
                            self.play_a_sorcery_or_instant(card, current_player, opponent, gameBoard)
                else:
                    if self.check_lands(card, gameBoard):
                        self.clear_mana(self.player_2)
                        self.stacked_card = card
                        gameBoard.stacked_card(self.stacked_card)
                        current_player.hand.remove(card)
                        current_player.graveyard.append(card)
                        self.response(self.player_1, self.player_2, gameBoard)
                        gameBoard.draw_board(self.phase)
                        self.stacked_card = card
                        gameBoard.stacked_card(self.stacked_card)
                        self.play_a_sorcery_or_instant(card, current_player, opponent, gameBoard)



    def select_card(self, valid_cards):
        return valid_cards[0]


    def check_instant(self, hand):
        for card in hand:
            if card.card_type == "Instant":
                return True
        return False


    def check_lands(self, card, gameBoard):
        cards_cost = card.mana_cost[:]
        required_land_amt = self.check_card_cost(card)
        mana_copy = []
        for land in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
            if land.card.tapped == False:
                mana_copy.append(land)

        if len(mana_copy) >= required_land_amt:
            i = 0
            while i < required_land_amt:
                self.add_mana(self.player_2, mana_copy[i].card)
                gameBoard.tap_mana(mana_copy[i])
                gameBoard.draw_land(self.player_2)
                pygame.display.update()
                time.sleep(0.2)
                i += 1

            return True

        else:
            return False


    def check_card_cost(self, card):
        cards_cost = card.mana_cost
        cards_cost = list(cards_cost)
        cost_as_integer = 0
        i = 0
        while i < len(cards_cost):
            if cards_cost[0].isdigit():
                cost_as_integer += int(cards_cost[0])
            else:
                cost_as_integer += 1
            i += 1
        return cost_as_integer



    def combat_phase(self, current_player, next_player, gameBoard):

        self.phase = "combat"
        gameBoard.draw_phase_section(self.phase)
        gameBoard.draw_indicator(self.player_1)
        pygame.display.update()


        if self.check_life() and not self.quit:
            attackers = self.select_attackers(current_player, gameBoard, next_player)
            defenders = self.select_defenders(next_player, attackers, gameBoard)
            self.damage_step(attackers, defenders,current_player, next_player, gameBoard)
            if attackers != None:
                for attacker in attackers:
                    attacker.combat_state = ""
            if defenders != None:
                for defenders in defenders:
                    combat_state = ""

    def damage_step(self, attackers, defenders, current_player, next_player, gameBoard):
        if attackers != None:
            i = 0
            while i < len(attackers):
                if type(defenders[i]) != int and ((defenders[i].keyword != "Flying" and attackers[i].keyword != "Flying") or (defenders[i].keyword == "Flying" and attackers[i].keyword != "Flying") or (defenders[i].keyword == "Flying" and attackers[i].keyword == "Flying")):
                        attackers[i].toughness_modifier -= (defenders[i].power + defenders[i].power_modifier)
                        defenders[i].toughness_modifier -= (attackers[i].power + attackers[i].power_modifier)
<<<<<<< HEAD
                        print(defenders[i].keyword, attackers[i].keyword)
                        if attackers[i].toughness + attackers[i].toughness_modifier <= 0 or defenders[i].keyword == "Deathtouch":
=======

                        if attackers[i].toughness + attackers[i].toughness_modifier <= 0:
>>>>>>> 0fec254bd535196a22cbfefc78c7349b1005890e
                            current_player.graveyard.append(attackers[i])
                            current_player.battlefield.remove(attackers[i])
                        if attackers[i].keyword == "Trample":
                            next_player.life += (attackers[i].toughness + attackers[i].toughness_modifier)
                        if attackers[i].keyword == "LifeLink":
                            current_player.life += (attackers[i].power + attackers[i].power_modifier)
<<<<<<< HEAD
                        if defenders[i].toughness + defenders[i].toughness_modifier <= 0 or attackers[i].keyword == "Deathtouch":
=======
                        if defenders[i].toughness + defenders[i].toughness_modifier <= 0:
>>>>>>> 0fec254bd535196a22cbfefc78c7349b1005890e
                            next_player.graveyard.append(defenders[i])
                            next_player.battlefield.remove(defenders[i])
                        if defenders[i].keyword == "LifeLink":
                            next_player.life += (defenders[i].power + defenders[i].power_modifier)
                else:
                    if attackers[i].keyword == "LifeLink":
                        current_player.life += (attackers[i].power + attackers[i].power_modifier)
                    next_player.life -= attackers[i].power
                i += 1
            gameBoard.draw_new_battlefield(current_player)
            gameBoard.draw_new_battlefield(next_player)


    def select_attackers(self, player, gameBoard, next_player):
        if player.name != "AI_Dusty":
            list_of_attackers = []
            resolved = False
            while not resolved:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        self.my_quit()

                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            if gameBoard.concede_button_sec.x < pos[0] < gameBoard.concede_button_sec.x + gameBoard.concede_button_sec.w and gameBoard.concede_button_sec.y < pos[1] < gameBoard.concede_button_sec.y + gameBoard.concede_button_sec.h:
                                self.quit = True
                                resolved = True

                            if gameBoard.pass_button_sec.x < pos[0] < gameBoard.pass_button_sec.x + gameBoard.pass_button_sec.w and gameBoard.pass_button_sec.y < pos[1] < gameBoard.pass_button_sec.y + gameBoard.pass_button_sec.h:
                                resolved = True


                            for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos):
                                    if card.card.combat_state != "attacking" and (card.card.summon_sick != True or card.card.keyword == "Haste"):
                                        card.card.combat_state = "attacking"
                                        if "Vigilance" not in card.card.keyword and "Vigilance" not in card.card.tmp_keyword:
                                            card.card.tapped = True
                                            gameBoard.tap_creature(card)
                                            card.card.tapped = True
                                        list_of_attackers.append(card.card)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            resolved = True

                    self.draw_screen(gameBoard)
                    if self.stacked_card != None:
                        gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)
                    pygame.display.update()
            return list_of_attackers

        else:
            list_of_attackers = player.attacker_list(next_player, gameBoard)
            for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                if creature_sprite.card in list_of_attackers:
                    gameBoard.tap_creature(creature_sprite)
                    creature_sprite.card.tapped = True
                    pygame.display.update()

            return list_of_attackers


    def select_defenders(self, next_player, list_of_attackers, gameBoard):
        if next_player.name == "AI_Dusty":
            available_blockers = []
            for creature in self.player_2.battlefield:
                if creature.tapped == False:
                    available_blockers.append(creature)

            list_of_defenders = (self.player_2.select_defenders(available_blockers, list_of_attackers, self.player_1))
            return list_of_defenders
        else:
            list_of_defenders = [0]*len(list_of_attackers)
            chosen_defender = None
            chosen_attacker = None
            if len(self.player_1.battlefield) > 0:
                resolved = False
                while not resolved:
                    for event in pygame.event.get():


                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                return list_of_defenders


                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()

                            if event.button == 1:


                                if gameBoard.concede_button_sec.x < pos[0] < gameBoard.concede_button_sec.x + gameBoard.concede_button_sec.w and gameBoard.concede_button_sec.y < pos[1] < gameBoard.concede_button_sec.y + gameBoard.concede_button_sec.h:
                                    self.quit = True
                                    resolved = True

                                if gameBoard.pass_button_sec.x < pos[0] < gameBoard.pass_button_sec.x + gameBoard.pass_button_sec.w and gameBoard.pass_button_sec.y < pos[1] < gameBoard.pass_button_sec.y + gameBoard.pass_button_sec.h:
                                    return list_of_defenders


                                for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if creature_sprite.rect.collidepoint(pos) and "Defending" not in creature_sprite.card.combat_state:
                                        if chosen_defender == None:
                                            chosen_defender = creature_sprite
                                            creature_sprite.card.combat_state = "Defending"
                                            gameBoard.tap_creature(creature_sprite)
                                for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if creature_sprite.rect.collidepoint(pos) and creature_sprite.card in list_of_attackers:
                                        if chosen_attacker == None:
                                            chosen_attacker = creature_sprite


                    self.draw_screen(gameBoard)
                    if chosen_attacker != None and chosen_defender != None:
                        indx = list_of_attackers.index(chosen_attacker.card)
                        if type(list_of_defenders[indx]) == int:
                            list_of_defenders[indx] = chosen_defender.card
                            gameBoard.add_battle_line(chosen_attacker, chosen_defender)
                        chosen_defender = None
                        chosen_attacker = None

                    for defender in list_of_defenders:
                        lst_1 = []
                        lst_2 = []
                        for creature in board.BATTELING_CREATURE_ATT:
                            x1, y1 = creature.rect.center
                            lst_1.append((x1,y1))

                        for creature in board.BATTELING_CREATURE_DEF:
                            x2, y2 = creature.rect.center
                            lst_2.append((x2,y2))

                        i = 0
                        while i < len(lst_1):
                            pygame.draw.line(screen_res.gameDisplay, board.BLACK, lst_1[i], lst_2[i], int(screen_res.display_width/60))
                            i += 1

                    if self.stacked_card != None:
                        gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)
                    pygame.display.update()
            else:
                list_of_defenders.append(0)
                return list_of_defenders

    def draw_cursor(self, x, y):
        screen_res.gameDisplay.blit(cursor, (x, y))

    def draw_screen(self, gameBoard):
        gameBoard.draw_board(self.phase)
        board.PLAYER_1_HAND_SPRITE_CARD_GROUP.draw(screen_res.gameDisplay)
        board.PLAYER_1_LAND_SPRITE_CARD_GROUP.draw(screen_res.gameDisplay)
        board.PLAYER_2_LAND_SPRITE_CARD_GROUP.draw(screen_res.gameDisplay)
        board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP.draw(screen_res.gameDisplay)
        board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP.draw(screen_res.gameDisplay)
        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            gameBoard.draw_summon_icon(card)
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            gameBoard.draw_summon_icon(card)

    def get_icon(self, w, h, keyword):
        scale_side = h
        if w < h:
            scale_side = w

        if keyword == "Tap":
            image = pygame.image.load('./images/spell_effects/tap_icon.png')

        elif keyword == "Damage":
            image = pygame.image.load('./images/spell_effects/damage_icon.png')

        elif keyword == "Bounce":
            image = pygame.image.load('./images/spell_effects/bounce_icon.png')

        elif keyword == "Haste":
            image = pygame.image.load('./images/spell_effects/haste_icon.png')

        elif keyword == "Combat_Creature":
            image = pygame.image.load('./images/spell_effects/combat_creature_icon.png')

        elif keyword == "Gain_life":
            image = pygame.image.load('./images/spell_effects/cross_icon.png')

        elif keyword == "Protection":
            image = pygame.image.load('./images/spell_effects/protection_symbol.png')

        elif keyword == "Exile":
            image = pygame.image.load('./images/spell_effects/exile_icon.png')

        elif keyword == "Destroy":
            image = pygame.image.load('./images/spell_effects/skull_icon.png')

        elif keyword == "Reanimate":
            image = pygame.image.load('./images/spell_effects/gravestone_icon.png')

        else:
            image = pygame.image.load('./images/crosshair.png')

        image_w = int(scale_side*0.7)
        image_h = image_w
        image = copy.copy(pygame.transform.smoothscale(image, (image_w, image_h)))
        return image


    def play_a_sorcery_or_instant(self, card, player, opponent, gameBoard, combinations = None):
        if card.effect == "Draw":
            self.effect_draw(player, gameBoard, card.value, combinations)

        elif card.effect == "Tap":
            self.effect_tap(player, opponent, gameBoard, combinations, card.value)

        elif card.effect == "Damage":
            self.effect_dmg(player, opponent, gameBoard, card.targets, card.value, combinations)

        elif card.effect == "Bounce":
            self.effect_bounce(player, opponent, gameBoard, combinations)

        elif card.effect == "Combat_Creature":
            self.effect_combat_creature(player, opponent, gameBoard, combinations)

        elif card.effect == "Search_land":
            self.effect_search_land(player, gameBoard, card, combinations)

        elif card.effect == "Gain_life":
            self.effect_gain_life(player, opponent, gameBoard, card.targets, card.value, combinations)

        elif card.effect == "Protection":
            self.effect_protection(player, opponent, gameBoard, card.targets, card.value, combinations)

        elif card.effect == "Exile":
            self.effect_exile(player, opponent, gameBoard, card.targets, combinations)

        elif card.effect == "Destroy":
            self.effect_destroy(player, opponent, gameBoard, card.targets, combinations)

        elif card.effect == "Discard":
            self.effect_discard(player, opponent, gameBoard, card.targets, card.value, combinations)

        elif card.effect == "Reanimate":
            self.effect_reanimate(player, opponent, gameBoard, card, combinations)

        gameBoard.draw_hand()
        gameBoard.draw_new_battlefield(player)
        gameBoard.draw_new_battlefield(opponent)

        return

    def get_target_icon(self, w, h):
        scale_side = h
        if w < h:
            scale_side = w

        image = pygame.image.load('./images/crosshair.png')

        image_w = int(scale_side*0.7)
        image_h = image_w
        image = copy.copy(pygame.transform.smoothscale(image, (image_w, image_h)))
        return image


    def effect_discard(self, player, opponent, gameBoard, list_of_targets, value, combinations):
        tmp_1 = False
        tmp_2 = False

        if "player" in list_of_targets and "Protection" not in player.state:
            tmp_1 = True

        if "opponent" in list_of_targets and "Protection" not in opponent.state:
            tmp_2 = True

        if tmp_1 or tmp_2:
            resolved = False
        else:
            resolved = True

        amt = 0
        clicked_target = ""

        if type(player) != ai.Ai:
            player_2_cards = []
            if len(self.player_1.hand) > 0 or len(self.player_2.hand) > 0:
                while not resolved:
                    if clicked_target == "opponent":
                        player_2_cards = gameBoard.draw_discard_hand(self.player_2)
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
                        mx, my = pos[0], pos[1]
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:

                                if "player" in list_of_targets and len(self.player_1.hand) > 0:
                                    if clicked_target == "" or clicked_target == "player":
                                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                            if card.rect.collidepoint(pos):
                                                clicked_target = "player"
                                                player.hand.remove(card.card)
                                                player.graveyard.append(card.card)
                                                amt += 1

                                if "opponent" in list_of_targets and len(self.player_2.hand) > 0:
                                    if (gameBoard.player_2_player_sec.x < pos[0] < gameBoard.player_2_player_sec.x + gameBoard.player_2_player_sec.w) and (gameBoard.player_2_player_sec.y < pos[1] < gameBoard.player_2_player_sec.y + gameBoard.player_2_player_sec.h):
                                        if clicked_target == "":
                                            clicked_target = "opponent"

                                if clicked_target == "opponent":
                                    for card in player_2_cards:
                                        if card.rect.collidepoint(pos):
                                            self.player_2.hand.remove(card.card)
                                            self.player_2.graveyard.append(card.card)
                                            amt += 1



                                if amt == int(value):
                                    resolved = True

                        self.draw_screen(gameBoard)
                        gameBoard.stacked_card(self.stacked_card)
                        gameBoard.draw_indicator(self.player_1)
                        if clicked_target == "opponent":
                            player_2_cards = gameBoard.draw_discard_hand(self.player_2)
                            pygame.display.update()
        else:
            if len(self.player_1.hand) > 0:
                indx = random.randint(0, len(self.player_1.hand) -1)
                self.player_1.graveyard.append(self.player_1.hand.pop(indx))


            elif len(self.player_2.hand) > 0:
                indx = random.randint(0, len(self.player_2.hand)-1)
                self.player_2.graveyard.append(self.player_2.hand.pop(indx))




    def effect_destroy(self, player, opponent, gameBoard, list_of_targets, combinations):
        tmp_1 = False
        tmp_2 = False

        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_1 = True

        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_2 = True

        if tmp_1 or tmp_2:
            resolved = False
        else:
            resolved = True

        if type(player) != ai.Ai:
            while not resolved:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            if "creature" in list_of_targets:
                                for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                                            player.battlefield.remove(card.card)
                                            player.graveyard.append(card.card)

                                            resolved = True

                                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                                            opponent.battlefield.remove(card.card)
                                            opponent.graveyard.append(card.card)

                                            resolved = True

                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    pygame.display.update()
        else:
            valid_targets_player = []
            valid_targets_ai = []
            for creature in self.player_1.battlefield:
                if "Protection" not in creature.keyword and "Protection" not in creature.tmp_keyword:
                    valid_targets_player.append([creature, self.player_1])

            for creature in self.player_2.battlefield:
                if "Protection" not in creature.keyword and "Protection" not in creature.tmp_keyword:
                    valid_targets_ai.append([creature, self.player_2])

            ai_combined_toughness = self.player_2.calculate_combined_toughness()
            ai_combined_power = self.player_2.calculate_combined_power()

            player_combined_toughness = self.player_2.calculate_combined_toughness(self.player_1)
            player_combined_power = self.player_2.calculate_combined_power(self.player_1)

            if len(valid_targets_player) > 0:
                if player_combined_toughness >= ai_combined_power:
                    best_target = None
                    for creature in valid_targets_player:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) < (creature.toughness + creature.toughness_modifier)
                            best_target = creature

                elif player_combined_power >= ai_combined_toughness:
                    best_target = None
                    for creature in valid_targets_player:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.power + best_target.power_modifier) < (creature.power + creature.power_modifier)
                            best_target = creature
                else:
                    best_target = None
                    for creature in valid_targets_player:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) + (best_target.power + best_target.power_modifier) < (creature.toughness + creature.toughness_modifier) + (creature.power + creature.power_modifier)
                            best_target = creature
                self.player_1.battlefield.remove(best_target)
                self.player_1.graveyard.append(best_target)
                self.draw_screen(gameBoard)
                gameBoard.draw_new_battlefield(self.player_1)




            elif len(valid_targets_ai) > 0:
                if player_combined_toughness >= ai_combined_power:
                    best_target = None
                    for creature in valid_targets_ai:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.power + best_target.power_modifier) > (creature.power + creature.power_modifier)
                            best_target = creature


                elif player_combined_power >= ai_combined_toughness:
                    best_target = None
                    for creature in valid_targets_ai:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) > (creature.toughness + creature.toughness_modifier)
                            best_target = creature

                else:
                    best_target = None
                    for creature in valid_targets_ai:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) + (best_target.power + best_target.power_modifier) > (creature.toughness + creature.toughness_modifier) + (creature.power + creature.power_modifier)
                            best_target = creature

                self.player_2.battlefield.remove(best_target)
                self.player_2.graveyard.append(best_target)
                self.draw_screen(gameBoard)
                gameBoard.draw_new_battlefield(self.player_2)





    def effect_exile(self, player, opponent, gameBoard, list_of_targets, combinations):
        tmp_1 = False
        tmp_2 = False

        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_1 = True

        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_2 = True

        if tmp_1 or tmp_2:
            resolved = False
        else:
            resolved = True

        if type(player) != ai.Ai:
            while not resolved:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            if "creature" in list_of_targets:
                                for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                                            player.battlefield.remove(card.card)

                                            resolved = True

                                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                                            opponent.battlefield.remove(card.card)

                                            resolved = True

                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    pygame.display.update()
        else:
            valid_targets_player = []
            valid_targets_ai = []
            for creature in self.player_1.battlefield:
                if "Protection" not in creature.keyword and "Protection" not in creature.tmp_keyword:
                    valid_targets_player.append(creature)

            for creature in self.player_2.battlefield:
                if "Protection" not in creature.keyword and "Protection" not in creature.tmp_keyword:
                    valid_targets_ai.append(creature)

            ai_combined_toughness = self.player_2.calculate_combined_toughness()
            ai_combined_power = self.player_2.calculate_combined_power()

            player_combined_toughness = self.player_2.calculate_combined_toughness(self.player_1)
            player_combined_power = self.player_2.calculate_combined_power(self.player_1)

            if len(valid_targets_player) > 0:
                if player_combined_toughness >= ai_combined_power:
                    best_target = None
                    for creature in valid_targets_player:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) < (creature.toughness + creature.toughness_modifier)
                            best_target = creature

                elif player_combined_power >= ai_combined_toughness:
                    best_target = None
                    for creature in valid_targets_player:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.power + best_target.power_modifier) < (creature.power + creature.power_modifier)
                            best_target = creature
                else:
                    best_target = None
                    for creature in valid_targets_player:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) + (best_target.power + best_target.power_modifier) < (creature.toughness + creature.toughness_modifier) + (creature.power + creature.power_modifier)
                            best_target = creature
                self.player_1.battlefield.remove(best_target)
                self.draw_screen(gameBoard)
                gameBoard.draw_new_battlefield(self.player_1)




            elif len(valid_targets_ai) > 0:
                if player_combined_toughness >= ai_combined_power:
                    best_target = None
                    for creature in valid_targets_ai:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.power + best_target.power_modifier) > (creature.power + creature.power_modifier)
                            best_target = creature


                elif player_combined_power >= ai_combined_toughness:
                    best_target = None
                    for creature in valid_targets_ai:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) > (creature.toughness + creature.toughness_modifier)
                            best_target = creature

                else:
                    best_target = None
                    for creature in valid_targets_ai:
                        if best_target == None:
                            best_target = creature
                        else:
                            (best_target.toughness + best_target.toughness_modifier) + (best_target.power + best_target.power_modifier) > (creature.toughness + creature.toughness_modifier) + (creature.power + creature.power_modifier)
                            best_target = creature

                self.player_2.battlefield.remove(best_target)
                self.draw_screen(gameBoard)
                gameBoard.draw_new_battlefield(self.player_2)




    def effect_protection(self, player, opponent, gameBoard, list_of_targets, value, combinations):
        tmp_1 = False
        tmp_2 = False
        tmp_3 = False
        tmp_4 = False

        if "player" in list_of_targets and "Protection" not in player.state:
            tmp_1 = True

        if "opponent" in list_of_targets and "Protection" not in opponent.state:
            tmp_2 = True

        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_3 = True

        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_4 = True

        if tmp_1 or tmp_2 or tmp_3 or tmp_4:
            resolved = False
        else:
            resolved = True
        if type(player) != ai.Ai:
            while not resolved:
                 for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if "player" in list_of_targets and tmp_1:
                                if gameBoard.player_1_player_sec.y + gameBoard.player_1_player_sec.h > pos[1] > gameBoard.player_1_player_sec.y and gameBoard.player_1_player_sec.x + gameBoard.player_1_player_sec.w > pos[0] > gameBoard.player_1_player_sec.x:
                                    player.state = "Protection"
                                    resolved = True

                            if "opponent" in list_of_targets and tmp_2:
                                if gameBoard.player_2_player_sec.y + gameBoard.player_2_player_sec.h > pos[1] > gameBoard.player_2_player_sec.y and gameBoard.player_2_player_sec.x + gameBoard.player_2_player_sec.w > pos[0] > gameBoard.player_2_player_sec.x:
                                    opponent.state = "Protection"
                                    resolved = True

                            if "creature" in list_of_targets:
                                for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if card.card.tmp_keyword == "":
                                            card.card.tmp_keyword = "Protection"
                                        else:
                                            tmp = card.card.tmp_keyword + "Protection"
                                            card.card.tmp_keyword = tmp
                                    resolved = True

                                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if card.card.tmp_keyword == "":
                                            card.card.tmp_keyword = "Protection"
                                        else:
                                            tmp = card.card.tmp_keyword + "Protection"
                                            card.card.tmp_keyword = tmp
                                    resolved = True

                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    if "player" in list_of_targets and tmp_1:
                        image = self.get_target_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h)
                        image_rect = image.get_rect()
                        image_rect.center = ((gameBoard.player_1_player_sec.x + (gameBoard.player_1_player_sec.w/2)), (gameBoard.player_1_player_sec.y + (gameBoard.player_1_player_sec.h/2)))
                        screen_res.gameDisplay.blit(image, image_rect)


                    if "opponent" in list_of_targets and tmp_2:
                        image = self.get_target_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h)
                        image_rect = image.get_rect()
                        image_rect.center = ((gameBoard.player_2_player_sec.x + (gameBoard.player_2_player_sec.w/2)), (gameBoard.player_2_player_sec.y + (gameBoard.player_2_player_sec.h/2)))
                        screen_res.gameDisplay.blit(image, image_rect)

                    pygame.display.update()




    def effect_gain_life(self, player, opponent, gameBoard,list_of_targets, value, combinations):
        resolved = True

        if "player" in list_of_targets and "Protection" not in player.state:
            resolved = False

        if "opponent" in list_of_targets and "Protection" not in opponent.state:
            resolved = False

        if type(player) != ai.Ai:
            while not resolved:
                 for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if "opponent" in list_of_targets and "Protection" not in opponent.state:
                                if  gameBoard.player_2_player_sec.y + gameBoard.player_2_player_sec.h > pos[1] > gameBoard.player_2_player_sec.y and gameBoard.player_2_player_sec.x + gameBoard.player_2_player_sec.w > pos[0] > gameBoard.player_2_player_sec.x:
                                    opponent.life += int(value)
                                    resolved = True
                            if "player" in list_of_targets and "Protection" not in player.state:
                                if gameBoard.player_1_player_sec.y + gameBoard.player_1_player_sec.h > pos[1] > gameBoard.player_1_player_sec.y and gameBoard.player_1_player_sec.x + gameBoard.player_1_player_sec.w > pos[0] > gameBoard.player_1_player_sec.x:
                                    player.life += int(value)
                                    resolved = True
                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    if "player" in list_of_targets and "Protection" not in player.state:
                        image = self.get_target_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h)
                        image_rect = image.get_rect()
                        image_rect.center = ((gameBoard.player_1_player_sec.x + (gameBoard.player_1_player_sec.w/2)), (gameBoard.player_1_player_sec.y + (gameBoard.player_1_player_sec.h/2)))
                        screen_res.gameDisplay.blit(image, image_rect)


                    if "opponent" in list_of_targets and "Protection" not in opponent.state:
                        image = self.get_target_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h)
                        image_rect = image.get_rect()
                        image_rect.center = ((gameBoard.player_2_player_sec.x + (gameBoard.player_2_player_sec.w/2)), (gameBoard.player_2_player_sec.y + (gameBoard.player_2_player_sec.h/2)))
                        screen_res.gameDisplay.blit(image, image_rect)


                    pygame.display.update()
        else:
            if "player" in list_of_targets and "Protection" not in player.state:
                player.life += int(value)

            elif "opponent" in list_of_targets and "Protection" not in opponent.state:
                opponent.life += int(value)


    def effect_search_land(self, player, gameBoard, spell, combinations):
        land_cards = []
        for land_card in player.deck.cards:
            if land_card.card_type == "Land":
                land_cards.append(land_card)

        counter = 0
        if type(player) != ai.Ai:
            resolved = False
            while not resolved:
                card_list = gameBoard.draw_search_land(player)

                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            for card in card_list:
                                if card.rect.collidepoint(pos):
                                    player.land_zone.append(card.card)
                                    player.deck.cards.remove(card.card)
                                    counter += 1
                                    self.shuffle_deck(self.player_1)
                                    gameBoard.draw_land(player)
                                    if (counter == int(spell.value) or (len(land_cards) - counter == 0)):
                                        resolved = True
        else:
            for card in player.deck.cards:
                if card.card_type == "Land":
                    player.land_zone.append(card)
                    player.deck.cards.remove(card)
                    self.shuffle_deck(self.player_2)
                    gameBoard.draw_land(player)
                    return

    def effect_combat_creature(self, player, opponent, gameBoard, combinations):
        tmp_1 = False
        tmp_2 = False
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_1 = True
        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                tmp_2 = True

        if tmp_1 == True and tmp_2 == True:
            resolved = False
        else:
            resolved = True

        attacker = []
        defender = []
        if type(player) != ai.Ai:
            while not resolved:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                    if len(attacker) < 1:
                                        attacker.append(card.card)
                            for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                    if len(defender) < 1:
                                        defender.append(card.card)
                            if len(attacker) + len(defender) == 2:
                                attacker[0].toughness_modifier -= defender[0].power
                                defender[0].toughness_modifier -= attacker[0].power
                                if (defender[0].toughness + defender[0].toughness_modifier) <= 0:
                                    for card in opponent.battlefield:
                                        if card == defender[0]:
                                            opponent.graveyard.append(card)
                                            opponent.battlefield.remove(card)
                                if (attacker[0].toughness + attacker[0].toughness_modifier) <= 0:
                                    for card in player.battlefield:
                                        if card == attacker[0]:
                                            player.graveyard.append(card)
                                            player.battlefield.remove(card)
                                resolved = True

                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    if len(attacker) == 0:
                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                image = self.get_target_icon(card.rect.w, card.rect.h)
                                image_rect = image.get_rect()
                                image_rect.center = card.rect.center
                                screen_res.gameDisplay.blit(image, image_rect)

                    if len(defender) == 0:
                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                image = self.get_target_icon(card.rect.w, card.rect.h)
                                image_rect = image.get_rect()
                                image_rect.center = card.rect.center
                                screen_res.gameDisplay.blit(image, image_rect)


                    pygame.display.update()
        else:
            ranked_creatures = []
            opponent_battlefield_copy = opponent.battlefield[:]
            while len(ranked_creatures) != len(opponent.battlefield):
                best_creature = None

                for creature in opponent_battlefield_copy:
                    if best_creature == None:
                        best_creature = creature
                    else:
                        if best_creature.power < creature.power:
                            best_creature = creature

                ranked_creatures.append(best_creature)
                opponent_battlefield_copy.remove(best_creature)

            ai_target = None
            enemy_target = None
            found_targets = False
            i = 0
            while i < len(ranked_creatures) and found_targets == False:
                tmp_target = ranked_creatures[i]
                for creature in self.player_2.battlefield:
                    if (creature.power >= tmp_target.toughness) and (creature.toughness > tmp_target.power):
                        ai_target = creature
                        enemy_target = tmp_target
                        found_targets = True

                i += 1
            if ai_target != None and enemy_target != None:
                ai_target.toughness_modifier -= (enemy_target.power + enemy_target.power_modifier)
                enemy_target.toughness_modifier -= (ai_target.power + ai_target.power_modifier)

                if ai_target.toughness + ai_target.toughness_modifier <= 0:
                    self.player_2.battlefield.remove(ai_target)
                    self.player_2.graveyard.append(ai_target)
                    self.draw_screen(gameBoard)
                    gameBoard.draw_new_battlefield(self.player_2)
                    pygame.display.update()

                if enemy_target.toughness + enemy_target.toughness_modifier <= 0:
                    self.player_1.battlefield.remove(enemy_target)
                    self.player_1.graveyard.append(enemy_target)
                    self.draw_screen(gameBoard)
                    gameBoard.draw_new_battlefield(self.player_1)
                    pygame.display.update()




    def effect_draw(self, player, gameBoard, value, combinations):
        for i in range (int(value)):
            self.draw(player, gameBoard)

    def effect_tap(self, player, opponent, gameBoard, combinations, value):
        available_targets = []
        resolved = True
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                available_targets.append(card.card)
                resolved = False
        amt = 0
        if type(player) != ai.Ai:
            while not resolved:
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
                        mx, my = pos[0], pos[1]
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if (card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword)) and card.card.tapped != True:
                                        card.card.tapped = True
                                        gameBoard.tap_creature(card)
                                        card.card.tapped = True
                                        amt += 1
                                        if amt == int(value) or len(available_targets) - amt == 0:
                                            resolved = True


                        self.draw_screen(gameBoard)
                        gameBoard.stacked_card(self.stacked_card)
                        gameBoard.draw_indicator(self.player_1)

                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                                image = self.get_target_icon(card.rect.w, card.rect.h)
                                image_rect = image.get_rect()
                                image_rect.center = card.rect.center
                                screen_res.gameDisplay.blit(image, image_rect)

                        pygame.display.update()
        else:
            resolved = False
            available_targets = []
            while not resolved:
                print("hi")
                best_attacker = None
                best_blocker = None
                for creature in self.player_2.battlefield:
                    if best_blocker == None:
                        best_blocker = creature
                    else:
                        if creature.toughness > best_blocker.toughness:
                            best_blocker = creature

                for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if creature_sprite.card.tapped != True:
                        available_targets.append(creature_sprite)

                for creature_sprite in available_targets:
                    if best_attacker == None:
                        best_attacker = creature_sprite
                    else:
                        if creature_sprite.card.power > best_attacker.card.power:
                            best_attacker = creature_sprite

                if best_attacker != None and best_blocker != None:
                    if best_blocker.toughness <= best_attacker.card.power:
                        best_attacker.card.tapped = True
                        gameBoard.tap_creature(best_attacker)
                        best_attacker.card.tapped = True
                        amt += 1

                if amt == int(value) or len(available_targets) - amt <= 0:
                    resolved = True


    def effect_dmg(self, player, opponent, gameBoard, list_of_targets, value, combinations):
        resolved = True
        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                resolved = False
        if "opponent" in list_of_targets and "Protection" not in opponent.state:
            resolved = False
        while not resolved:
            if player.name != "AI_Dusty":
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            if "opponent" in list_of_targets:

                                if "Protection" not in opponent.state:

                                    if gameBoard.player_2_player_sec.y + gameBoard.player_2_player_sec.h > pos[1] > gameBoard.player_2_player_sec.y and gameBoard.player_2_player_sec.x + gameBoard.player_2_player_sec.w > pos[0] > gameBoard.player_2_player_sec.x:
                                        opponent.life -= int(value)
                                        resolved = True

                            if "creature" in list_of_targets:

                                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:

                                    if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                        if (self.damage_creature(card.card, value)):
                                            opponent.graveyard.append(card.card)
                                            opponent.battlefield.remove(card.card)
                                            gameBoard.draw_new_battlefield(opponent)
                                            resolved = True
                        if event.type == pygame.QUIT:
                            self.my_quit()

                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    if "opponent" in list_of_targets and "Protection" not in opponent.state:
                        image = self.get_target_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h)
                        image_rect = image.get_rect()
                        image_rect.center = ((gameBoard.player_2_player_sec.x + (gameBoard.player_2_player_sec.w/2)), (gameBoard.player_2_player_sec.y + (gameBoard.player_2_player_sec.h/2)))
                        screen_res.gameDisplay.blit(image, image_rect)



                    pygame.display.update()
            else:
                chosen_target  = None
                ai_combined_toughness = player.calculate_combined_toughness()
                player_combined_toughness = player.calculate_combined_toughness(opponent)
                ai_combined_power = player.calculate_combined_power()
                player_combined_power = player.calculate_combined_power(opponent)
                opponent_weight = 0

                if "opponent" in list_of_targets and "Protection" not in opponent.state:
                    if (int(opponent.life) <= int(value)):
                        opponent_weight = 1
                    elif (int(opponent.life)) + (player_combined_toughness)  <=  ai_combined_power:
                        opponent_weight = 0.055
                    elif (int(opponent.life)) + (player_combined_toughness)  >  ai_combined_power:
                        opponent_weight = 0.05
                    elif (int(opponent.life)) < 5:
                        opponent_weight = 0.05

                if "creature" in list_of_targets:
                    potential_creatures = []
                    for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in creature_sprite.card.keyword and "Protection" not in creature_sprite.card.tmp_keyword:
                            if creature_sprite.card.toughness_modifier < 0:
                                potential_creatures.append([0.045, creature_sprite.card])
                            if int(value) >= (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier):
                                potential_creatures.append([0.20, creature_sprite.card])
                            else:
                                tmp_hp = (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier) - int(value)
                                if combinations != None:
                                    for next_card in combinations:
                                        if (next_card.card_type == "Instant" or next_card.card_type == "Sorcery") and next_card is not card and int(next_card.value) >= tmp_hp:
                                            potential_creatures.append([0.025,creature_sprite.card])

                spell_target = player.calculate_target(opponent,opponent_weight,potential_creatures)
                if spell_target != self.player_1:
                        if self.damage_creature(creature_sprite.card, value):
                            opponent.graveyard.append(creature_sprite.card)
                            opponent.battlefield.remove(creature_sprite.card)
                            gameBoard.draw_new_battlefield(opponent)
                            resolved = True
                else:
                    opponent.life -= int(value)
                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(player)
                    resolved = True



    def effect_bounce(self, player, opponent, gameBoard, combinations):
        print("hi")
        resolved = True
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                resolved = False

        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword:
                resolved = False
                print(resolved)

        if type(player) != ai.Ai:
            while not resolved:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                    player.hand.append(card.card)
                                    player.battlefield.remove(card.card)
                                    card.card.summon_sick = True
                                    resolved = True

                            for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                    opponent.hand.append(card.card)
                                    opponent.battlefield.remove(card.card)
                                    card.card.summon_sick = True
                                    resolved = True

                    if event.type == pygame.QUIT:
                        self.my_quit()

                    self.draw_screen(gameBoard)
                    gameBoard.stacked_card(self.stacked_card)
                    gameBoard.draw_indicator(self.player_1)

                    for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)


                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                            image = self.get_target_icon(card.rect.w, card.rect.h)
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    pygame.display.update()
        else:
            best_attacker = None
            best_blocker = None
            for creature in self.player_2.battlefield:
                if best_blocker == None:
                    best_blocker = creature
                else:
                    if creature.toughness > best_blocker.toughness:
                        best_blocker = creature.toughness

            for creature in self.player_1.battlefield:
                if best_attacker == None:
                    best_attacker = creature
                else:
                    if creature.power > best_attacker.power:
                        best_attacker = creature
            if best_attacker != None and best_blocker != None:
                if best_blocker.toughness <= best_attacker.power:
                    self.player_1.battlefield.remove(best_attacker)
                    self.player_1.hand.append(best_attacker)
                    best_attacker.summon_sick = True
                    self.draw_screen(gameBoard)
                    gameBoard.draw_hand()
                    gameBoard.draw_new_battlefield(self.player_1)




    def effect_reanimate(self, player, opponent, gameBoard, spell, combinations):
        creature_cards_player_1 = []
        for creature_card in self.player_1.graveyard:
            if creature_card.card_type == "Creature":
                creature_cards_player_1.append(creature_card)

        creature_cards_player_2 = []
        for creature_card in self.player_2.graveyard:
            if creature_card.card_type == "Creature":
                creature_cards_player_2.append(creature_card)


        if (len(creature_cards_player_1) > 0) or (len(creature_cards_player_2) > 0):
            counter = 0
            if type(player) != ai.Ai:
                card_list = []
                chosen_player = None
                resolved = False

                while not resolved:
                    if chosen_player != None:
                        if chosen_player == "player":
                            card_list = gameBoard.draw_search_grave(self.player_1)
                        elif chosen_player == "opponent":
                            card_list = gameBoard.draw_search_grave(self.player_2)

                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
                        mx, my = pos[0], pos[1]
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:

                                if chosen_player == None:
                                    if gameBoard.player_1_player_sec.y + gameBoard.player_1_player_sec.h > pos[1] > gameBoard.player_1_player_sec.y and gameBoard.player_1_player_sec.x + gameBoard.player_1_player_sec.w > pos[0] > gameBoard.player_1_player_sec.x:
                                        if len(creature_cards_player_1) > 0:
                                            chosen_player = "player"

                                    if gameBoard.player_2_player_sec.y + gameBoard.player_2_player_sec.h > pos[1] > gameBoard.player_2_player_sec.y and gameBoard.player_2_player_sec.x + gameBoard.player_2_player_sec.w > pos[0] > gameBoard.player_2_player_sec.x:
                                        if len(creature_cards_player_2) > 0:
                                            chosen_player = "opponent"

                                for card in card_list:
                                    if card.rect.collidepoint(pos):
                                        card.card.summon_sick = True
                                        card.card.tapped = False
                                        card.card.toughness_modifier = 0
                                        card.card.power_modifier = 0
                                        if chosen_player == "player":
                                            self.player_1.battlefield.append(card.card)
                                            self.player_1.graveyard.remove(card.card)
                                            gameBoard.draw_new_battlefield(self.player_1)
                                        elif chosen_player == "opponent":
                                            self.player_1.battlefield.append(card.card)
                                            self.player_2.graveyard.remove(card.card)
                                            gameBoard.draw_new_battlefield(self.player_2)
                                        counter += 1
                                        if chosen_player == "player":
                                            if (counter == int(spell.value) or (len(creature_cards_player_1) - counter == 0)):
                                                resolved = True
                                        if chosen_player == "opponent":
                                            if (counter == int(spell.value) or (len(creature_cards_player_2) - counter == 0)):
                                                resolved = True

            else:
                ai_combined_toughness = player.calculate_combined_toughness()
                player_combined_toughness = player.calculate_combined_toughness(opponent)
                ai_combined_power = player.calculate_combined_power()
                player_combined_power = player.calculate_combined_power(opponent)

                if len(player.graveyard) > 0 or len(opponent.graveyard) > 0:
                    possible_targets = []
                    #SPLIT INTO TWO LISTS TO MAKE SURE AI DOESN'T RESURECT FROM BOTH GRAVEYARDS
                    for dead_card in player.graveyard:
                        if dead_card.card_type == "Creature":
                            possible_targets.append(dead_card)

                    for dead_card in opponent.graveyard:
                        if dead_card.card_type == "Creature":
                            possible_targets.append(dead_card)

                    if len(possible_targets) > 0:
                        targets = []
                        range_val = 0
                        if len(possible_targets) < int(spell.value):
                            range_val = len(possible_targets)
                        else:
                            range_val = int(spell.value)
                        for i in range(range_val):
                            best_target = None
                            for target in possible_targets:

                                if best_target == None:
                                    best_target = target
                                else:
                                    if ai_combined_toughness <= player_combined_power:
                                        if best_target.toughness < target.toughness:
                                            best_target = target
                                    else:
                                        if best_target.power < target.power:
                                            best_target = target

                            targets.append(best_target)

                        targets_toughness = 0
                        targets_power = 0
                        for creature in targets:
                            if creature != None:
                                creature.summon_sick = True
                                creature.tapped = False
                                creature.toughness_modifier = 0
                                creature.power_modifier = 0
                                player.battlefield.append(creature)
                                self.draw_screen(gameBoard)
                                gameBoard.draw_new_battlefield(player)
                                pygame.display.update()



    def damage_creature(self, card, damage):
        card.toughness_modifier -= int(damage)
        return (card.toughness_modifier <= card.toughness)



    def play_a_land(self, card, current_player, gameBoard):

        if current_player.land_flag == False:
            indx = current_player.hand.index(card)
            current_player.land_zone.append(current_player.hand.pop(indx))
            gameBoard.draw_hand()
            gameBoard.draw_land(current_player)
            current_player.land_flag = True
        else:
            gameBoard.draw_hand()

    def play_a_creature(self,card, current_player,next_player, gameBoard):
        gameBoard.draw_hand()
        gameBoard.draw_new_battlefield(current_player)
        gameBoard.draw_new_battlefield(next_player)

    def check_mana(self, player, card):
        cards_cost = card.mana_cost[:]
        mana_copy = list(player.mana[:])
        i = len(cards_cost) - 1
        while i >= 0 :
            if cards_cost[i].isdigit():
                if len(mana_copy) >= int(cards_cost[i]):
                    if int(cards_cost[i]) > 0:
                        for n in range(int(cards_cost[i])):
                            mana_copy.pop(0)
                else:
                    return False

            elif cards_cost[i] in mana_copy:
                mana_copy.remove(cards_cost[i])

            else:
                return False

            i -= 1
        player.mana = "".join(mana_copy)
        return True

    def clear_mana(self, player):
        player.mana = ""

    def my_quit(self):
        pygame.quit()
        quit()
