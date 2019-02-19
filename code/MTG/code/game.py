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


pygame.init()
pygame.mixer.init()

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
            self.untap(self.player_1)
            self.draw(self.player_1)
            gameBoard.draw_hand(self.player_1)
            self.main_phase(self.player_1, self.player_2, gameBoard, display)

############################# UPDATING SCREEN ######################################
            gameBoard.draw_board()
            board.HAND_SPRITE_CARD_GROUP.draw(display)
            pygame.display.update()
            self.my_quit()





    def check_game_status(self):
        lives = self.player_1.life > 0 and self.player_2.life > 0
        decks = self.player_1.deck.size > 0 and self.player_2.deck.size > 0
        ##has_quit =  self.player_1.has_quit()
        return lives and decks### and has_quit 

    def deck_selection(self, player):
        f = open("./personal_decks/deck_1", "rb")
        player_deck = pickle.load(f)
        f.close()

        return player_deck

    def shuffle_deck(self, player):
        shuffle(player.deck.cards)

    def deal_cards(self, player, n):    
        for i in range(n):
            player.hand.append(player.deck.cards.pop(0))

    def draw(self, player):
        player.hand.append(player.deck.cards.pop(0))
        print("######################### Break ###########################")

    def untap(self, player):

        for creature in player.battlefield:
            creature.status = "norm"

        for land in player.land_zone:
            land.status = "norm"

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
                    x = pos[0]
                    y = pos[1]

                    if event.button == 1:
                        for card in board.HAND_SPRITE_CARD_GROUP:
                            if card.rect.collidepoint(pos):
                                card.clicked = True

                if event.type == pygame.MOUSEBUTTONUP:

                    for card in board.HAND_SPRITE_CARD_GROUP:
                        if card.clicked == True:
                            card.clicked = False

                            if gameBoard.player_1_hand_box.x > card.rect.x > gameBoard.player_1_hand_box.x + gameBoard.player_1_hand_box.w or gameBoard.player_1_hand_box.y > card.rect.y:
                                if card.card.card_type == "Land":
                                    if current_player.land_flag < 1:
                                        indx = current_player.hand.index(card.card)
                                        current_player.land_zone.append(current_player.hand.pop(indx))
                                        print(current_player.land_zone)


############################# GAME LOGIC HERE#######################################

            for card in board.HAND_SPRITE_CARD_GROUP:
                if card.clicked == True:
                    pos = pygame.mouse.get_pos()
                    card.rect.x = pos[0] - (card.rect.width/2)
                    card.rect.y = pos[1] - (card.rect.height/2)


            gameBoard.draw_board()
            board.HAND_SPRITE_CARD_GROUP.draw(display)
            pygame.display.update()



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
