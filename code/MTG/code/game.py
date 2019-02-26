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

    def run_game(self):
        player_1_deck_list = self.deck_selection(self.player_1)
        player_2_deck_list = self.deck_selection(self.player_2)

        self.player_1.deck = deck.Deck("gablins", player_1_deck_list)
        self.player_2.deck = deck.Deck("gibluns", player_2_deck_list)

        self.shuffle_deck(self.player_1)
        self.shuffle_deck(self.player_2)

        gameBoard = board.Board(self.player_1, self.player_2)

        self.deal_cards(self.player_1, 7)
        self.deal_cards(self.player_2, 7)
        print(self.player_1.hand)

        gameBoard.calc_board()
        self.draw_screen(gameBoard)
        gameBoard.draw_hand()

        pygame.display.update()

        self.current_player = random.choice([self.player_1, self.player_2])

        print(self.current_player.name)

        self.game_loop(gameBoard)

    def game_loop(self, gameBoard):
        while self.check_game_status():

            ########### TURNS LOGIC ################
            self.untap(self.player_1, gameBoard)
            print("1")
            self.draw(self.player_1, gameBoard)
            print("2")
            self.main_phase(self.player_1, self.player_2, gameBoard)
            print("3")
            self.combat_phase(self.player_1, self.player_2, gameBoard)
            print("4")
            self.main_phase(self.player_1, self.player_2, gameBoard)
            print("5")
            self.end_step(gameBoard)

############################# UPDATING SCREEN ######################################



    def end_step(self, gameBoard):
        self.phase = "end"
        gameBoard.draw_phase_section(self.phase)
        pygame.display.update()
        self.player_1.state = ""
        self.player_2.state = ""
        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            card.card.toughness_modifier = 0
            card.card.power_modifier = 0
            card.card.tmp_keyword = ""
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            card.card.toughness_modifier = 0
            card.card.power_modifier = 0
            card.card.tmp_keyword = ""


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
        f = open("./personal_decks/deck_4", "rb")
        player_deck = pickle.load(f)
        f.close()

        return player_deck

    def shuffle_deck(self, player):
        shuffle(player.deck.cards)

    def deal_cards(self, player, n):
        for i in range(n):
            player.hand.append(player.deck.cards.pop(0))

    def draw(self, player, gameBoard):
        self.phase = "draw"
        gameBoard.draw_phase_section(self.phase)
        pygame.display.update()


        if self.check_not_mill(player):
            player.hand.append(player.deck.cards.pop(0))
            gameBoard.draw_hand()
            gameBoard.draw_player_hand_section()

    def untap(self, player, gameBoard):
        self.phase = "untap"
        gameBoard.draw_phase_section(self.phase)
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
        print(player.mana)

    def main_phase(self, current_player, next_player, gameBoard):
        if self.phase == "combat":
            self.phase = "main_2"
        else:
            self.phase = "main_1"
        self.draw_screen(gameBoard)
        pygame.display.update()
        print(self.check_life())
        if self.check_life() and not self.quit:
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
                            print(gameBoard.concede_button_sec.x, pos[0])
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


                            for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos):
                                    card.clicked = True

                            if gameBoard.player_1_land_sec.x + gameBoard.player_1_land_sec.w > pos[0] > gameBoard.player_1_land_sec.x and gameBoard.player_1_land_sec.y + gameBoard.player_1_land_sec.h > pos[1] > gameBoard.player_1_land_sec.y:
                                for land in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:

                                    if land.rect.collidepoint(pos) and land.card.tapped == False:
                                        self.add_mana(current_player, land.card)
                                        gameBoard.tap_mana(land)
                                        print(current_player.mana)

                    if event.type == pygame.MOUSEBUTTONUP:

                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                            if card.clicked == True:
                                self.draw_screen(gameBoard)
                                card.clicked = False

                                if ((gameBoard.player_hand_sec.x > card.rect.x) or (card.rect.x > gameBoard.player_hand_sec.x + gameBoard.player_hand_sec.w)) or gameBoard.player_hand_sec.y > card.rect.y:

                                    if card.card.card_type == "Land":
                                        self.play_a_land(card.card, current_player, gameBoard)


                                    if card.card.card_type == "Creature":
                                        self.play_a_creature(card.card, current_player,next_player, gameBoard)

                                    if card.card.card_type == "Sorcery" or card.card.card_type == "Instant":
                                        self.play_a_sorcery_or_instant(card.card, current_player, next_player, gameBoard)

                                    if self.check_life() == False:
                                        return

                                    self.draw_screen(gameBoard)
                                    pygame.display.update()

                                else:
                                    gameBoard.draw_hand()


                    for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                        if card.clicked == True:
                            pos = pygame.mouse.get_pos()
                            card.rect.x = pos[0] - (card.rect.width/2)
                            card.rect.y = pos[1] - (card.rect.height/2)
                            pos, card.rect.x, card.rect.y

                    self.draw_screen(gameBoard)
                    for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                        if card.rect.collidepoint(pos):
                            gameBoard.view_card(card)
                            board.VIEWED_CARD.draw(screen_res.gameDisplay)
                            pygame.display.update()

                    for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if card.rect.collidepoint(pos):
                            gameBoard.view_card(card)
                            board.VIEWED_CARD.draw(screen_res.gameDisplay)
                            pygame.display.update()


                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if card.rect.collidepoint(pos):
                            gameBoard.view_card(card)
                            board.VIEWED_CARD.draw(screen_res.gameDisplay)
                            pygame.display.update()

                    for card in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:
                        if card.rect.collidepoint(pos):
                            gameBoard.view_card(card)
                            board.VIEWED_CARD.draw(screen_res.gameDisplay)
                            pygame.display.update()

                    for card in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
                        if card.rect.collidepoint(pos):
                            gameBoard.view_card(card)
                            board.VIEWED_CARD.draw(screen_res.gameDisplay)
                            pygame.display.update()

                clock.tick(60)
            self.clear_mana(current_player)


    def combat_phase(self, current_player, next_player, gameBoard):
        self.phase = "combat"
        gameBoard.draw_phase_section(self.phase)
        pygame.display.update()

        if self.check_life() and not self.quit:
            attackers = self.select_attackers(current_player, gameBoard)
            defenders = self.select_defenders(next_player, attackers, gameBoard)
            self.damage_step(attackers, defenders,current_player, next_player, gameBoard)
            for attacker in attackers:
                attacker.combat_state = ""
            for defenders in defenders:
                combat_state = ""

    def damage_step(self, attackers, defenders, current_player, next_player, gameBoard):
        i = 0
        while i < len(attackers):
            if type(defenders[i]) != int:
                attackers[i].toughness_modifier -= defenders[i].power
                defenders[i].toughness_modifier -= attackers[i].power
                if attackers[i].toughness + attackers[i].toughness_modifier <= 0:
                    current_player.graveyard.append(attackers[i])
                    current_player.battlefield.remove(attackers[i])
                if defenders[i].toughness + defenders[i].toughness_modifier <= 0:
                    next_player.graveyard.append(defenders[i])
                    next_player.battlefield.remove(defenders[i])
            else:
                next_player.life -= attackers[i].power
            i += 1
        gameBoard.draw_new_battlefield(current_player)
        gameBoard.draw_new_battlefield(next_player)


    def select_attackers(self, player, gameBoard):
        list_of_attackers = []
        resolved = False
        while not resolved:
            for event in pygame.event.get():

                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                print(card.card.combat_state)
                                if card.card.combat_state != "attacking" and card.card.summon_sick != True:
                                    card.card.combat_state = "attacking"
                                    if "Vigiliance" not in card.card.keyword and "Vigiliance" not in card.card.tmp_keyword:
                                        card.card.tapped = True
                                        gameBoard.tap_creature(card)
                                    list_of_attackers.append(card.card)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        resolved = True

                self.draw_screen(gameBoard)
                pygame.display.update()
        return list_of_attackers

    def select_defenders(self, next_player, list_of_attackers, gameBoard):
        resolved = True
        list_of_defenders = []
        if len(list_of_attackers) > 0:
            list_of_defenders = len(list_of_attackers)*[0]
            resolved = False
        while not resolved:
            i = 0
            for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                list_of_defenders[i] = card.card
                i += 1
            resolved = True
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





    def play_a_sorcery_or_instant(self, card, player, opponent, gameBoard):
        playable = self.check_mana(player, card)
        if playable == True:
            pygame.mouse.set_visible(False)
            i = 0
            while i < len(player.hand):
                if player.hand[i] == card:
                    if card.effect == "Draw":
                        self.effect_draw(player, gameBoard, card.value)

                    elif card.effect == "Tap":
                        self.effect_tap(player, opponent, gameBoard)

                    elif card.effect == "Damage":
                        self.effect_dmg(opponent, gameBoard, card.targets, card.value)

                    elif card.effect == "Bounce":
                        self.effect_bounce(player, opponent, gameBoard)

                    elif card.effect == "Haste":
                        self.effect_haste(player, gameBoard, value)

                    elif card.effect == "Combat_Creature":
                        self.effect_combat_creature(player, opponent, gameBoard)

                    elif card.effect == "Search_land":
                        self.effect_search_land(player, gameBoard)

                    elif card.effect == "Gain_life":
                        self.effect_gain_life(player, opponent, gameBoard, card.targets, card.value)

                    elif card.effect == "Protection":
                        self.effect_protection(player, opponent, gameBoard, card.targets, card.value)

                    elif card.effect == "Exile":
                        self.effect_exile(player, opponent, gameBoard, card.targets)

                    elif card.effect == "Destroy":
                        self.effect_destroy(player, opponent, gameBoard, card.targets)

                    elif card.effect == "Discard":
                        self.effect_discard(player, opponent, gameBoard, card.targets, card.value)

                    elif card.effect == "Reanimate":
                        self.effect_reanimate(player, opponent, card.targets, gameBoard)

                    pygame.mouse.set_visible(True)
                    player.hand.remove(card)
                    player.graveyard.append(card)
                    #gameBoard.draw_graveyard(player)
                    gameBoard.draw_hand()
                    gameBoard.draw_new_battlefield(player)
                    gameBoard.draw_new_battlefield(opponent)

                    return
                i += 1
        else:
            gameBoard.draw_hand()

    def effect_discard(self, player, opponent, gameBoard, list_of_targets, value):
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
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        if "player" in list_of_targets:
                            if clicked_target == "" or clicked_target == "player":
                                for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        clicked_target = "player"
                                        player.hand.remove(card.card)
                                        player.graveyard.append(card.card)
                                        amt += 1


                        if "opponent" in list_of_targets:
                            if clicked_target == "" or clicked_target == "opponent":
                                for card in board.PLAYER_2_HAND_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        clicked_target = "opponent"
                                        opponent.hand.remove(card.card)
                                        opponent.graveyard.append(card.card)

                                        amt += 1

                        if amt == int(value):
                            resolved = True

                self.draw_screen(gameBoard)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()

    def effect_destroy(self, player, opponent, gameBoard, list_of_targets):
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

                for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Destroy")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Destroy")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()

    def effect_exile(self, player, opponent, gameBoard, list_of_targets):
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

                for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Exile")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Exile")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()


    def effect_protection(self, player, opponent, gameBoard, list_of_targets, value):
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

                for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Protection")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Protection")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                if "player" in list_of_targets and tmp_1:
                    image = self.get_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h, "Protection")
                    image_rect = image.get_rect()
                    image_rect.center = ((gameBoard.player_1_player_sec.x + (gameBoard.player_1_player_sec.w/2)), (gameBoard.player_1_player_sec.y + (gameBoard.player_1_player_sec.h/2)))
                    screen_res.gameDisplay.blit(image, image_rect)


                if "opponent" in list_of_targets and tmp_2:
                    image = self.get_icon(gameBoard.player_1_player_sec.w, gameBoard.player_1_player_sec.h, "Protection")
                    image_rect = image.get_rect()
                    image_rect.center = ((gameBoard.player_2_player_sec.x + (gameBoard.player_2_player_sec.w/2)), (gameBoard.player_2_player_sec.y + (gameBoard.player_2_player_sec.h/2)))
                    screen_res.gameDisplay.blit(image, image_rect)


                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()



    def effect_gain_life(self, player, opponent, gameBoard,list_of_targets, value):
        resolved = True

        if "player" in list_of_targets and "Protection" not in player.state:
            resolved = False

        if "opponent" in list_of_targets and "Protection" not in opponent.state:
            resolved = False
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

                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                    if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                        image = self.get_icon(card.rect.w, card.rect.h, "Gain_life")
                        image_rect = image.get_rect()
                        image_rect.center = card.rect.center
                        screen_res.gameDisplay.blit(image, image_rect)

                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()


    def effect_search_land(self, player, gameBoard):
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
                                gameBoard.draw_land(player)
                                resolved = True


    def effect_combat_creature(self, player, opponent, gameBoard):
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
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()

    def effect_haste(self, player, gameBoard, value):
        resolved = True
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                resolved = False
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                            if card.rect.collidepoint(pos):
                                card.card.keyword = "Haste"
                                resolved = True

                self.draw_screen(gameBoard)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()

    def effect_draw(self, player, gameBoard, value):
        for i in range (int(value)):
            self.draw(player, gameBoard)

    def effect_tap(self, player, opponent, gameBoard):
        resolved = True
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                resolved = False
        while not resolved:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword) or card.card.tapped != True:
                                    card.card.tapped = True
                                    gameBoard.tap_creature(card)
                                    resolved = True


                    self.draw_screen(gameBoard)

                    for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                        if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                            image = self.get_icon(card.rect.w, card.rect.h, "Tap")
                            image_rect = image.get_rect()
                            image_rect.center = card.rect.center
                            screen_res.gameDisplay.blit(image, image_rect)

                    self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                    pygame.display.update()

    def effect_dmg(self, opponent, gameBoard, list_of_targets, value):
        resolved = True
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                resolved = False
        if "opponent" in list_of_targets and "Protection" not in opponent.state:
            resolved = False

        while not resolved:
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
                                    print("4")
                                    if (self.damage_creature(card.card, value)):
                                        print("5")
                                        opponent.graveyard.append(card.card)
                                        opponent.battlefield.remove(card.card)
                                        gameBoard.draw_new_battlefield(opponent)
                                        #gameBoard.draw_graveyard(opponent)
                                        resolved = True
                    if event.type == pygame.QUIT:
                        self.my_quit()

                self.draw_screen(gameBoard)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()

    def effect_bounce(self, player, opponent, gameBoard):
        resolved = True
        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if "Protection" not in card.card.tmp_keyword and "Protection" not in card.card.keyword and card.card.tapped == False:
                resolved = False
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
                                resolved = True

                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos) and ("Protection" not in card.card.keyword and "Protection" not in card.card.tmp_keyword):
                                opponent.hand.append(card.card)
                                opponent.battlefield.remove(card.card)
                                resolved = True

                if event.type == pygame.QUIT:
                    self.my_quit()

                self.draw_screen(gameBoard)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
                pygame.display.update()

    def effect_reanimate(self, player, opponent, targets, gameBoard):
        resolved = False
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if "opponent" in targets:
                            if (gameBoard.player_2_graveyard.y + gameBoard.player_2_graveyard.h > my > gameBoard.player_2_graveyard.y) and (gameBoard.player_2_graveyard.x + gameBoard.player_2_graveyard.w > mx > gameBoard.player_2_graveyard.x):

                                resolved = True
                        if "player" in targets:
                            if (gameBoard.player_1_graveyard.y + gameBoard.player_1_graveyard.h > my > gameBoard.player_1_graveyard.y) and (gameBoard.player_2_graveyard.x + gameBoard.player_2_graveyard.w > mx > gameBoard.player_2_graveyard.x):

                                resolved = True
                if event.type == pygame.QUIT:
                    self.my_quit()

                self.draw_screen(gameBoard)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2))
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
        playable = self.check_mana(current_player, card)
        if playable == True:
            indx = current_player.hand.index(card)
            copy.copy(current_player.hand[indx])
            next_player.battlefield.append(copy.copy(current_player.hand[indx]))
            current_player.battlefield.append(current_player.hand.pop(indx))
            gameBoard.draw_hand()
            gameBoard.draw_new_battlefield(current_player)
            gameBoard.draw_new_battlefield(next_player)

        else:
            gameBoard.draw_hand()

    def check_mana(self, player, card):
        cards_cost = card.mana_cost[:]
        mana_copy = list(player.mana[:])
        i = 0
        j = 0
        while i < len(cards_cost):
            if cards_cost[i].isdigit():
                if int(cards_cost[i]) > 0 and len(mana_copy) >= int(cards_cost[i]):
                    for n in range(int(cards_cost[i])):
                        mana_copy.pop(0)

            elif cards_cost[i] in mana_copy:
                mana_copy.remove(cards_cost[i])

            else:
                return False

            i += 1
        player.mana = "".join(mana_copy)
        return True

    def clear_mana(self, player):
        player.mana = ""

    def my_quit(self):
        pygame.quit()
        quit()
