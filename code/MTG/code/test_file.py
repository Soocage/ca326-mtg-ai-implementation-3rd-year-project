import pygame
import sys
import player
import board
import deck
import pickle
import card
from random import shuffle


pygame.init()
pygame.mixer.init()



def run_game(gameDisplay, display_size):
    (display_w, display_h) = display_size
    player_deck_list = deck_selection()
    opponent_deck_list = deck_selection()

    player_deck = deck.Deck("gablins", player_deck_list)
    opponent_deck = deck.Deck("gibluns", opponent_deck_list)

    player_1 = player.Player("Sean", player_deck)
    player_2 = player.Player("AI_Dusty", opponent_deck)

    
    #game_board = board.Board(gameDisplay, display_size, player_1, player_2)

    n = 7
    shuffle_deck(player_1)
    shuffle_deck(player_2)

    #board.draw_decks(player_1, player_2, gameDisplay, display_size)

    deal_cards(player_1, gameDisplay, display_size, n)#, game_board)
    mulligan(player_1, gameDisplay, display_size, n)#, game_board)

    deal_cards(player_2, gameDisplay, display_size, n)#, game_board)
    mulligan(player_2, gameDisplay, display_size, n)#, game_board)

    while player_1.life > 0 and player_2.life > 0:   
        print("FIRST PLAYERS TURN")
        for card in player_1.hand:
            print(card.name)
        untap(player_1, gameDisplay, display_size)#, game_board)
        draw(player_1, gameDisplay, display_size)#, game_board)
        main_1(player_1, player_2, gameDisplay, display_size)#, game_board)
        player_1.life -= 10

    

    pygame.display.update()




def main_1(player, player_2, gameDisplay, display_size):#, game_board):

    pass_phase = False
    while not pass_phase:
        print(player_2.name, "'s health is at ", player_2.life)
        print("chose action")
        print("tap mana\nplay a creature\nplay a sorcery\nplay an instant\nplay a land\npass phase")
        ans = input().lower()

        if ans == "tap mana":
            list_of_names = []
            print("which land would you like to tap")
            for land_card in player.land_zone:
                print(land_card.name, land_card.state)
                list_of_names.append(land_card.name)

            chosen_card = input()
            if chosen_card in list_of_names:
                found_flag = False
                i = 0
                while i < len(list_of_names) and found_flag == False:
                    if list_of_names[i] == chosen_card and player.land_zone[i].state != "tapped":
                        tap_mana(player, gameDisplay, display_size, player.land_zone[i])# game_board,
                        found_flag = True
                    i += 1
                
                if found_flag == False:
                    print("mana unavailable")

            else:
                print("chosen card ain't there")

            print(player.name ," your current mana is ", player.mana)

        elif ans == "play a land":
            list_of_names = []
            print("what land?")
            for card in player.hand:
                print(card.name, card.card_type)
                list_of_names.append(card.name.upper())

            land_card = input().upper()
            indx = list_of_names.index(land_card)
            play_a_land(player, gameDisplay, display_size, player.hand[indx])# game_board,
            

        elif ans == "play a creature":
            list_of_names = []
            print("What creature")
            for card in player.hand:
                print(card.name, card.card_type)
                list_of_names.append(card.name.upper())

            creature_card = input().upper()
            indx = list_of_names.index(creature_card)
            play_a_creature(player, gameDisplay, display_size, player.hand[indx])# game_board
            print("your hand is")
            for card in player.hand:
                print(card.name)
            print("your battlefield is")
            for card in player.hand:
                print(card.name)

        elif ans == "play a sorcery":
            list_of_names = []
            print("What sorcery")
            for card in player.hand:
                print(card.name, card.card_type)
                list_of_names.append(card.name.upper())

            sorcery_card = input().upper()
            indx = list_of_names.index(sorcery_card)
            play_a_sorcery(player, player_2, gameDisplay, display_size, player.hand[indx])# game_board,
            print("your hand is")
            for card in player.hand:
                print(card.name)
            print("your battlefield is")
            for card in player.hand:
                print(card.name)

        elif ans == "play an instant":
            play_an_instant(player, gameDisplay, display_size, card)# game_board,

        elif ans == "pass phase":
            pass_phase = True



def play_a_creature(player, gameDisplay, display_size, card):# game_board,
    playable = check_mana(player, card)
    if playable:
        #game_board.add_creature(player, gameDisplay, display_size)
        i = 0
        while i < len(player.hand):
            if player.hand[i].name == card.name:
                player.battlefield.append(player.hand.pop(i))
                return
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
                return

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
    card.state = "tapped"
    player.mana.append(card.colour)






def mulligan(player, gameDisplay, display_size, n, ):#game_board):
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



def deal_cards(player, gameDisplay, display_size, n,):# game_board):
    
    for i in range(n):
        player.hand.append(player.deck.cards.pop(0))
    #game_board.draw_hand(player, gameDisplay, display_size)

def deck_selection():
    f = open("../personal_decks/deck_1", "rb")
    player_deck = pickle.load(f)
    print(player_deck[0].state)
    f.close()

    return player_deck





def my_quit():
    pygame.quit()
    quit()


def shuffle_deck(player):
    shuffle(player.deck.cards)

def draw(player, gameDisplay, display_size): #, game_board):
    player.hand.append(player.deck.cards.pop(0))
    #game_board.draw_new_hand(player, gameDisplay, display_size)

def untap(player, gameDisplay, display_size):#, game_board):

    for creature in player.battlefield:
        creature.status = "norm"

    for land in player.land_zone:
        land.status = "norm"

    #game_board.draw_new_battlefield(player, gameDisplay, display_size)

if __name__ == "__main__":
    display_info = pygame.display.Info()
    display_size = (display_width, display_height)= (display_info.current_w, display_info.current_h)
    display_size = (20, 20)
    gameDisplay = pygame.display.set_mode(display_size)
    run_game(gameDisplay, display_size)
