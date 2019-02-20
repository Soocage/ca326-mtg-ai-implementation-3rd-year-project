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


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

cursor = pygame.image.load('./images/crosshair.png')
cursor_w = 100
cursor_h = 100
cursor = pygame.transform.scale(cursor, (cursor_w, cursor_h))


class Game():

    def __init__(self, gameDisplay, display_size, player_1, player_2):
        self.gameDisplay = gameDisplay
        self.display_size = display_size
        self.player_1 = player_1
        self.player_2 = player_2
        self.phase = None
        self.turn = 0
        self.current_player = None

    def run_game(self):
        player_1_deck_list = self.deck_selection(self.player_1)
        player_2_deck_list = self.deck_selection(self.player_2)

        self.player_1.deck = deck.Deck("gablins", player_1_deck_list)
        self.player_2.deck = deck.Deck("gibluns", player_2_deck_list)

        self.shuffle_deck(self.player_1)
        self.shuffle_deck(self.player_2)

        gameBoard = board.Board(self.gameDisplay, self.display_size, self.player_1, self.player_2)

        self.deal_cards(self.player_1, 7)
        self.deal_cards(self.player_2, 7)
        print(self.player_1.hand)


        gameBoard.draw_board()
        gameBoard.draw_hand(self.player_1)
        gameBoard.draw_hand(self.player_2)
        pygame.display.update()
        
        

        self.current_player = random.choice([self.player_1, self.player_2])

        print(self.current_player.name)

        self.game_loop(self.gameDisplay, gameBoard)

    def game_loop(self, display, gameBoard):
        while self.check_game_status(): 

            ########### TURNS LOGIC ################
            self.untap(self.player_1, gameBoard)
            self.draw(self.player_1, gameBoard)
            self.main_phase(self.player_1, self.player_2, gameBoard, display)

############################# UPDATING SCREEN ######################################





    def check_game_status(self):
        lives = self.player_1.life > 0 and self.player_2.life > 0
        decks = len(self.player_1.deck.cards) > 0 and len(self.player_2.deck.cards) > 0
        ##has_quit =  self.player_1.has_quit()
        return lives and decks### and has_quit 

    def deck_selection(self, player):
        f = open("./personal_decks/deck_2", "rb")
        player_deck = pickle.load(f)
        f.close()

        return player_deck

    def shuffle_deck(self, player):
        shuffle(player.deck.cards)

    def deal_cards(self, player, n):    
        for i in range(n):
            player.hand.append(player.deck.cards.pop(0))

    def draw(self, player, gameBoard):
        player.hand.append(player.deck.cards.pop(0))
        gameBoard.draw_hand(player)
        print("######################### Break ###########################")

    def untap(self, player, gameBoard):

        for creature in player.battlefield:
            creature.state = "untapped"


        for land in player.land_zone:
            land.state = "untapped"

        gameBoard.draw_land(player)
        player.land_flag = False
        self.clear_mana(player)

    def add_mana(self, player, land):
        land.state = "tapped"
        player.mana += land.colour
        player.mana = "".join(sorted(player.mana))

    def main_phase(self, current_player, next_player, gameBoard, display):
        pass_phase = False
        
        while not pass_phase:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.my_quit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        pass_phase = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if event.button == 1:
                        for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                card.clicked = True

                        if gameBoard.player_1_land_box.x + gameBoard.player_1_land_box.w > pos[0] > gameBoard.player_1_land_box.x and gameBoard.player_1_land_box.y + gameBoard.player_1_land_box.h > pos[1] > gameBoard.player_1_land_box.y:
                            for land in board.PLAYER_1_LAND_SPRITE_CARD_GROUP:
                                print (land.card.name)
                                if land.rect.collidepoint(pos) and land.card.state != "tapped":
                                    self.add_mana(current_player, land.card)
                                    gameBoard.tap_mana(land)
                                    print(current_player.mana)

                if event.type == pygame.MOUSEBUTTONUP:

                    for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                        if card.clicked == True:
                            card.clicked = False

                            if ((gameBoard.player_1_hand_box.x > card.rect.x) or (card.rect.x > gameBoard.player_1_hand_box.x + gameBoard.player_1_hand_box.w)) or gameBoard.player_1_hand_box.y > card.rect.y:
                                
                                if card.card.card_type == "Land":
                                    self.play_a_land(card.card, current_player, gameBoard)

                                if card.card.card_type == "Creature":
                                    self.play_a_creature(card.card, current_player,next_player, gameBoard)

                                if card.card.card_type == "Sorcery":
                                    self.play_a_sorcery(card.card, current_player, next_player, gameBoard, display)
                            else:
                                gameBoard.draw_hand(current_player)


                         

############################# GAME LOGIC HERE#######################################

            for card in board.PLAYER_1_HAND_SPRITE_CARD_GROUP:
                if card.clicked == True:
                    pos = pygame.mouse.get_pos()
                    card.rect.x = pos[0] - (card.rect.width/2)
                    card.rect.y = pos[1] - (card.rect.height/2)


            self.draw_screen(gameBoard, display)
            pygame.display.update()
            clock.tick(60)            
        self.clear_mana(current_player)

    def draw_cursor(self, x, y, display):
        display.blit(cursor, (x, y))



    def draw_screen(self, gameBoard, display):
        gameBoard.draw_board()
        board.PLAYER_1_LAND_SPRITE_CARD_GROUP.draw(display)
        board.PLAYER_2_LAND_SPRITE_CARD_GROUP.draw(display)
        board.PLAYER_1_HAND_SPRITE_CARD_GROUP.draw(display)
        board.PLAYER_2_HAND_SPRITE_CARD_GROUP.draw(display)
        board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP.draw(display)
        board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP.draw(display)


    def play_a_sorcery(self, card, player, opponent, gameBoard, display):
        playable = self.check_mana(player, card)
        if playable == True:
            pygame.mouse.set_visible(False)
            i = 0
            while i < len(player.hand):
                if player.hand[i] == card:
                    if card.effect == "Draw":
                        self.effect_draw(player, gameBoard, card.value, display)

                    elif card.effect == "Tap":
                        self.effect_tap(player, opponent, gameBoard, display)

                    elif card.effect == "Damage":
                        self.effect_dmg(opponent, gameBoard, card.targets, card.value, display)

                    elif card.effect == "Bounce":
                        self.effect_bounce(player, opponent, gameBoard, display)

                    elif card.effect == "Haste":
                        self.effect_haste(player, gameBoard, value, display)

                    elif card.effect == "Combat_Creature":
                        self.effect_combat_creature(player, opponent, gameBoard, display)

                    elif card.effect == "Search_land":
                        self.effect_search_land(player, gameBoard, display)

                    elif card.effect == "Gain_life":
                        self.effect_gain_life()

                    elif card.effect == "Protection":
                        self.effect_protection()

                    elif card.effect == "Exile":
                        self.effect_exile()

                    elif card.effect == "Destroy":
                        self.effect_destroy()

                    elif card.effect == "Discard":
                        self.effect_discard()

                    elif "Reanimate" in card.effect:
                        self.effect_reanimate()
                    pygame.mouse.set_visible(True)
                    player.graveyard.append(player.hand.pop(i))
                    #gameBoard.draw_graveyard(player)
                    gameBoard.draw_hand(player)
                    gameBoard.draw_hand(opponent)
                    gameBoard.draw_new_battlefield(player)
                    gameBoard.draw_new_battlefield(opponent)

                    return
                i += 1
        else:
            gameBoard.draw_hand(player)

    def effect_search_land(self, player, gameBoard, display):
        gameBoard.draw_search_land(player)

    def effect_combat_creature(self, player, opponent, gameBoard, display):
        resolved = False
        attacker = []
        defender = []
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                if len(attacker) < 1:
                                    attacker.append(card.card)
                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                if len(defender) < 1:
                                    defender.append(card.card)
                        if len(attacker) + len(defender) == 2:
                            attacker[0].toughness_modifier -= defender[0].power
                            defender[0].toughness_modifier -= attacker[0].power
                            if (defender[0].toughness - abs(defender[0].toughness_modifier)) <= 0:
                                print("friends")
                                for card in opponent.battlefield:
                                    if card == defender[0]:
                                        opponent.graveyard.append(card)
                                        opponent.battlefield.remove(card)
                            if (attacker[0].toughness - abs(attacker[0].toughness_modifier)) <= 0:
                                for card in player.battlefield:
                                    if card == attacker[0]:
                                        player.graveyard.append(card)
                                        player.battlefield.remove(card)
                            resolved = True

                self.draw_screen(gameBoard, display)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2), display)
                pygame.display.update()

    def effect_haste(self, player, gameBoard, value, display):
        resolved = False
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                card.card.keyword = "Haste"
                                resolved = True

                self.draw_screen(gameBoard, display)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2), display)
                pygame.display.update()

    def effect_draw(self, player, gameBoard, value, display):
        for i in range (value):
            self.draw(player, gameBoard, display)

    def effect_tap(self, player, opponent, gameBoard, display):
        resolved = False
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                card.card.state = "tapped"
                                board.tap_creature(card.card)
                                resolved = True

                self.draw_screen(gameBoard, display)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2), display)
                pygame.display.update()

    def effect_dmg(self, opponent, gameBoard, list_of_targets, value, display):
            resolved = False
            print(list_of_targets)
            while not resolved:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    mx, my = pos[0], pos[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            if "opponent" in list_of_targets:
                                print("2")

                                if  gameBoard.player_2_life_sec.y + gameBoard.player_2_life_sec.h > pos[1] > gameBoard.player_2_life_sec.y and gameBoard.player_2_life_sec.x + gameBoard.player_2_life_sec.w > pos[0] > gameBoard.player_2_life_sec.x:
                                    opponent.life -= int(value)
                                    resolved = True
                            if "Creature" in list_of_targets:        
                                for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                                    if card.rect.collidepoint(pos):
                                        if (self.damage_creature(card.card, value)):
                                            opponent.graveyard.append(card,card)
                                            opponent.battlefield.remove(card.card)
                                            gameBoard.draw_new_battlefield(opponent)
                                            gameBoard.draw_graveyard(opponent)
                                            resolved = True
                    if event.type == pygame.QUIT:
                        self.my_quit()

                    self.draw_screen(gameBoard, display)
                    self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2), display)
                    pygame.display.update()

    def effect_bounce(self, player, opponent, gameBoard, display):
        resolved = False
        while not resolved:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                mx, my = pos[0], pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                player.hand.append(card.card)
                                player.battlefield.remove(card.card)
                                resolved = True

                        for card in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                opponent.hand.append(card.card)
                                opponent.battlefield.remove(card.card)
                                resolved = True

                if event.type == pygame.QUIT:
                    self.my_quit()

                self.draw_screen(gameBoard, display)
                self.draw_cursor(mx - (cursor_w/2), my - (cursor_h/2), display)
                pygame.display.update()

                                

    def damage_creature(self, card, damage):
        card.toughness_modifier -= damage
        return (card.toughness_modifier >= card.toughness)



    def play_a_land(self, card, current_player, gameBoard):
        if current_player.land_flag == False:
            indx = current_player.hand.index(card)
            current_player.land_zone.append(current_player.hand.pop(indx))
            gameBoard.draw_hand(current_player)
            gameBoard.draw_land(current_player) 
            current_player.land_flag = True
        else:
            gameBoard.draw_hand(current_player)

    def play_a_creature(self,card, current_player,next_player, gameBoard):
        playable = self.check_mana(current_player, card)
        if playable == True:
            indx = current_player.hand.index(card)
            copy.copy(current_player.hand[indx])
            next_player.battlefield.append(copy.copy(current_player.hand[indx]))
            current_player.battlefield.append(current_player.hand.pop(indx))
            gameBoard.draw_hand(current_player)
            gameBoard.draw_new_battlefield(current_player)
            gameBoard.draw_new_battlefield(next_player)
            print("we did it")    
        else:
            gameBoard.draw_hand(current_player)

    def check_mana(self, player, card):
        cards_cost = card.mana_cost[:]
        mana_copy = list(player.mana[:])
        print(mana_copy)
        i = 0
        j = 0
        while i < len(cards_cost):
            if type(cards_cost[i]) == "int":
                if card_cost[i] > 0 and len(mana_copy) >= cards_cost[i]:
                    for n in range(card_cost[i]):
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


def run_game(gameDisplay, display_size):
    (display_w, display_h) = display_size
    player_deck_list = deck_selection()
    opponent_deck_list = deck_selection()

    
    #game_board = board.Board(gameDisplay, display_size, player_1, player_2)

    n = 7
    shuffle_deck(player_1)
    shuffle_deck(player_2)

    #board.draw_decks(player_1, player_2, gameDisplay, display_size)
    print("###################PLAYER 1 DRAW#######################")
    deal_cards(player_1, gameDisplay, display_size, n)#, game_board)
    for card in player_1.hand:
        print(card.name, card.card_type)
    print("###################PLAYER 1 MULIGAN#######################")
    mulligan(player_1, gameDisplay, display_size, n)#, game_board)

    print("###################PLAEYR 2 DRAW#######################")
    deal_cards(player_2, gameDisplay, display_size, n)#, game_board)
    for card in player_2.hand:
        print(card.name, card.card_type)
    print("###################PLAYER 2 MULIGAN#######################")
    mulligan(player_2, gameDisplay, display_size, n)#, game_board)

    while player_1.life > 0 and player_2.life > 0:   
        print("###################PLAYER 1 TURN#######################")
        for card in player_1.hand:
            print(card.name)
        untap(player_1, gameDisplay, display_size)#, game_board)
        draw(player_1, gameDisplay, display_size)#, game_board)
        main(player_1, player_2, gameDisplay, display_size)#, game_board)
        combat(player_1, player_2, gameDisplay, display_size)
        main(player_1, player_2, gameDisplay, display_size)
        end_step(player_1, player_2, gameDisplay, display_size)

        print("###################PLAYER 1 TURN#######################")
        for card in player_2.hand:
            print(card.name)
        untap(player_2, gameDisplay, display_size)#, game_board)
        draw(player_2, gameDisplay, display_size)#, game_board)
        main(player_2, player_1, gameDisplay, display_size)#, game_board)
        combat(player_2, player_1, gameDisplay, display_size)
        main(player_2, player_1, gameDisplay, display_size)
        end_step(player_2, player_1, gameDisplay, display_size)

    

    pygame.display.update()






def end_step(player_1, player_2, gameDisplay, display_size):
    for card in player_1.battlefield:
        card.toughness_modifier = 0
    for card in player_2.battlefield:
        card.toughness_modifier = 0
        
        




def combat(curr_player, next_player ,gameDisplay, display_size):#, game_board):
    print("###################COMBAT PHASE#######################")
    if len(curr_player.battlefield) > 0:
        list_of_attackers = []
        list_of_defenders = []
        print("select attackers")
        for card in curr_player.battlefield:
            print(card.name, card.state)
        attackers = input().split(",")

        for card in curr_player.battlefield:
            if card.name in attackers and card.state != "tapped":
                card.state == "attacking"
                list_of_attackers.append(card)
        
        if len(list_of_attackers) > 0:
            list_of_defenders = defenders(next_player, curr_player, gameDisplay, display_size, list_of_attackers)#, game_board)

        creature_damage(curr_player, next_player ,gameDisplay, display_size, list_of_attackers, list_of_defenders)#game_board,
        return

def defenders(next_player, curr_player, gameDisplay, display_size, attackers):#, game_board):
    print("###################", next_player.name.upper() ," DEFENDING PHASE#######################")
    pass_phase = False
    list_of_defenders = [0]*len(attackers)
    while not pass_phase:
        print("Would you like to pass? yes / no")
        ans = input().lower()
        if ans == "no":
            print("select defender")
            for card in next_player.battlefield:
                print(card.name, " power = ", card.power, " toughness = ", card.toughness)
            defender = input().upper()
            for card in next_player.battlefield:
                if card.name == defender and card.state != "tapped":
                    print("select which creature to block")
                    for card in attackers:
                        print(card.name, " power = ", card.power, " toughness = ", card.toughness)
                    blocked = input().upper()

                    i = 0
                    while i < len(attackers):
                        if attackers[i].name.upper() == blocked and attackers[i].state != "blocked":
                            attackers[i].state = "blocked"
                            list_of_defenders[i] = card
        elif ans == "yes":
            pass_phase = True
            print(list_of_defenders)
            return list_of_defenders

def player_damage(curr_player, next_player ,gameDisplay, display_size, attackers):#game_board, 
    for creature in attackers:
        next_player.life -= creature.power
    return

def creature_damage(curr_player, next_player ,gameDisplay, display_size, attackers, list_of_defenders):#, game_board:
    new_attackers = []
    i = 0
    while i < len(attackers):
        if list_of_defenders[i] != 0:
            list_of_defenders[i].toughness_modifier -= attackers[i].power
            attackers[i].toughness_modifier -= list_of_defenders[i].power
            if attackers[i].toughness - attackers[i].toughness_modifier == 0:
                attackers[i].state = "Dead"
            elif list_of_defenders[i].toughness - list_of_defenders[i].toughness_modifier == 0:
                list_of_defenders[i] = "Dead"
        i += 1

    for card in attackers:
        if card.state != "Dead":
                new_attackers.append(card)
        player_damage(curr_player, next_player ,gameDisplay, display_size,  new_attackers)#game_board,



def play_a_creature(player, gameDisplay, display_size, card):# game_board,
    playable = check_mana(player, card)
    if playable:
        #game_board.add_creature(player, gameDisplay, display_size)
        i = 0
        while i < len(player.hand):
            if player.hand[i].name == card.name:
                player.battlefield.append(player.hand.pop(i))
                return
            i += 1
    return

def play_a_sorcery(player, player_2, gameDisplay, display_size, card):# game_board,
    playable = check_mana(player, card)
    if playable:
        #game_board.add_sorcery(player, gameDisplay, display_size)
        i = 0
        while i < len(player.hand):
            if player.hand[i].name == card.name:
                player.hand.pop(i)
                if card.effect == "Draw":
                    effect_draw(player, gameDisplay, display_size,card)

                elif card.effect == "Tap":
                    effect_tap()

                elif card.effect == "Damage":
                    effect_dmg(player, player_2, gameDisplay, display_size,card)

                elif card.effect == "Bounce":
                    effect_bounce()

                elif card.effect == "Haste":
                    effect_haste()

                elif card.effect == "Dmg_Tough":
                    effect_dmg_tough()

                elif card.effect == "Combat_Creature":
                    effect_combat_creature()

                elif card.effect == "Search_land":
                    effect_serach_land()

                elif card.effect == "Gain_life":
                    effect_gain_life()

                elif card.effect == "Protection":
                    effect_protection()

                elif card.effect == "Exile":
                    effect_exile()

                elif card.effect == "Destroy":
                    effect_destroy()

                elif card.effect == "Discard":
                    effect_discard()

                elif card.effect == "Reanimate":
                    effect_reanimate()
                return
            i += 1

def effect_draw(player, gameDisplay, display_size,card):
    draw(player, gameDisplay, display_size)
    #Draw the new screen
    return

def effect_dmg(player, player_2, gameDisplay, display_size,card):
    player_2.life -= int(card.value)
    return

def play_an_instant(player, gameDisplay, display_size, card):# game_board, 
    playable = check_mana(player, card)
    if playable:
        #game_board.add_instant(player, gameDisplay, display_size)
        i = 0
        while i < len(player.hand):
            if player.hand[i].name == card.name:
                player.hand.pop(i)
                if card.effect == "Draw":
                    effect_draw(player, gameDisplay, display_size,card)

                elif card.effect == "Tap":
                    effect_tap()

                elif card.effect == "Damage":
                    effect_dmg(player, player_2, gameDisplay, display_size,card)

                elif card.effect == "Bounce":
                    effect_bounce()

                elif card.effect == "Haste":
                    effect_haste()

                elif card.effect == "Dmg_Tough":
                    effect_dmg_tough()

                elif card.effect == "Combat_Creature":
                    effect_combat_creature()

                elif card.effect == "Search_land":
                    effect_serach_land()

                elif card.effect == "Gain_life":
                    effect_gain_life()

                elif card.effect == "Protection":
                    effect_protection()

                elif card.effect == "Exile":
                    effect_exile()

                elif card.effect == "Destroy":
                    effect_destroy()

                elif card.effect == "Discard":
                    effect_discard()

                elif card.effect == "Reanimate":
                    effect_reanimate()
                return
            i += 1


def play_a_land(player, gameDisplay, display_size, card):# game_board,
    if player.land_flag < 1:
        i = 0
        while i < len(player.hand):
            if player.hand[i].name == card.name:
                print(len(player.hand))
                player.hand.pop(i)
                player.land_flag = 1
                player.land_zone.append(card)
                #game_board.add_land(player, gameDisplay, display_size, card)
                return

            i += 1
    else:
        print(len(player.hand))
        print("You already played a land this tunr")
        return

def check_mana(player, card):
    cards_cost = card.mana_cost[:]
    mana_copy = player.mana[:]
    i = 0
    j = 0
    while i < len(cards_cost):
        if type(cards_cost[i]) == "int":
            if card_cost[i] > 0 and len(mana_copy) >= cards_cost[i]:
                for n in range(card_cost[i]):
                    mana_copy.pop(0)

        elif cards_cost[i] in mana_copy:
            mana_copy.remove(cards_cost[i])

        else:
            return False

        i += 1
    player.mana = mana_copy
    return True


def tap_mana(player, gameDisplay, display_size, card):# game_board,
    print("###################TAP MANA#######################")
    card.state = "tapped"
    player.mana.append(card.colour)


def mulligan(player, gameDisplay, display_size, n):#game_board):
    print(player.name)
    print("would you like to muligan? yes/no")
    ans = input().lower()
    while ans:
        if ans == "yes":
            for card in player.hand:
                player.deck.cards.append(card)
            player.hand = []
            shuffle_deck(player)
            n -= 1
            deal_cards(player, gameDisplay, display_size, n)
            for card in player.hand:
                print(card.name)
            if n != 0:
                mulligan(player, gameDisplay, display_size, n)
            return

        elif ans == "no":
            return

        else:
            print("invalid anwser please write yes or no")
            print("would you liek to muligan? yes/no")
            ans = input().lower()

    #game_board.draw_new_battlefield(player, gameDisplay, display_size)

if __name__ == "__main__":
    display_info = pygame.display.Info()
    display_size = (display_width, display_height)= (display_info.current_w, display_info.current_h)
    display_size = (20, 20)
    gameDisplay = pygame.display.set_mode(display_size)
    run_game(gameDisplay, display_size)
