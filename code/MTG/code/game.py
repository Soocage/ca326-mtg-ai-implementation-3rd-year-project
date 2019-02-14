import pygame
import sys
import player
import board
import deck
import pickle
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

    
    game_board = board.Board(gameDisplay, display_size, player_1, player_2)

    n = 7
    shuffle_deck(player_1)
    shuffle_deck(player_2)

    board.draw_decks(player_1, player_2, gameDisplay, display_size)

    deal_cards(player_1, gameDisplay, display_size, n, game_board)
    deal_cards(player_2, gameDisplay, display_size, n game_board)

    mulligan(player_1, gameDisplay, display_size, n, game_board)
    mulligan(player_2, gameDisplay, display_size, n, game_board)

    pygame.display.update()

    while player_1.life > 0 or player_2.life > 0:   
        print("FIRST PLAYERS TURN")
        untap(player_1, gameDisplay, display_size, game_board)
        draw(player_1, gameDisplay, display_size, game_board)
        main_1(player_1, gameDisplay, display_size, game_board)
        combat(player_1,player_2 gameDisplay, display_size, game_board)
        main_2(player_1, gameDisplay, display_size, game_board)
        end_step()

        print("SECOND PLAYERS TURN")
        untap(player_2, gameDisplay, display_size, game_board)
        draw(player_2, gameDisplay, display_size, game_board)
        main_1(player_2, gameDisplay, display_size, game_board)
        combat(player_2, player_1, gameDisplay, display_size, game_board)
        main_2(player_2, gameDisplay, display_size, game_board)
        end_step()

    get_winner(player_1, player_2)






def defenders(next_player, gameDisplay, display_size, game_board):
    print("select defenders")
    defenders = input().split(",")
    for creature in next_player.battlefield:
        creature.status = "defending"

def combat(curr_player, next_player ,gameDisplay, display_size, game_board):
    print("select attackers")
    attackers = input().split(",")
    for card in curr_player.battlefield:
        if card.name in attackers:
            card.status == "tapped"

    list_of_defenders = defenders(next_player, gameDisplay, display_size, game_board)

    if len(list_of_defenders) > 0:
        creature_damage(curr_player, next_player ,gameDisplay, display_size, game_board, attackers, list_of_defenders)
    else:
        player_damage(curr_player, next_player ,gameDisplay, display_size, game_board, attackers)
    return

def creature_damage(curr_player, next_player ,gameDisplay, display_size, game_board, attackers, list_of_defenders):
    i = 0
    while list_of_defenders or i < len(attackers):
        #chose who to damage:
    if i < len(attackers):
        new_attackers = attackers[i:]
        player_damage(curr_player, next_player ,gameDisplay, display_size, game_board, new_attackers)
    return

def player_damage(curr_player, next_player ,gameDisplay, display_size, game_board, attackers):
    for creature in attackers:
        player.life -= creature.power
    return


def check_mana()
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


def play_a_creature(player, gameDisplay, display_size, game_board, card):
    playable = check_mana(player, card)
    if playable:
        player.current_mana = (player.current_mana - card.mana_cost)
        game_board.add_creature(player, gameDisplay, display_size)
        i = 0
        while i < len(player.current_hand):
            if player.current_hand[i].name == card.name:
                player.current_hand.pop(i)
                return
    return

def play_a_sorcery(player, gameDisplay, display_size, game_board, card):
    playable = check_mana(player, card)
    if playable:
        player.current_mana = (player.current_mana - card.mana_cost)
        game_board.add_sorcery(player, gameDisplay, display_size)
        i = 0
        while i < len(player.current_hand):
            if player.current_hand[i].name == card.name:
                player.current_hand.pop(i)
                return

def play_an_instant(player, gameDisplay, display_size, game_board, card):
    playable = check_mana(player, card)
        player.current_mana = (player.current_mana - card.mana_cost)
        game_board.add_instant(player, gameDisplay, display_size)
        i = 0
        while i < len(player.current_hand):
            if player.current_hand[i].name == card.name:
                player.current_hand.pop(i)
                return

def play_a_land(player, gameDisplay, display_size, game_board, card):
    if player.land_flag < 1:
        i = 0
        while i < len(player.current_hand):
            if player.current_hand[i].name == card.name:
                player.current_hand.pop(i)
                player.land_flag = 1
                game_board.add_land(player, gameDisplay, display_size, card)
                return

def tap_mana(player, gameDisplay, display_size, game_board, card):
    card.state = "tapped"
    player.mana.append(card.colour)


def main_1(player, gameDisplay, display_size, game_board):
    print("chose action")
    ans = input().lower
    pass_phase = False
    while not pass_phase:
        if ans = "tap mana":
            tap_mana(player, gameDisplay, display_size, game_board, card)

        if ans == "play a creature":
            play_a_creature(player, gameDisplay, display_size, game_board, card)

        elif ans == "play a sorcery":
            play_a_sorcery(player, gameDisplay, display_size, game_board, card)

        elif ans = "play an instant":
            play_an_instant(player, gameDisplay, display_size, game_board, card)

        elif ans = "play a land":
            play_a_land(player, gameDisplay, display_size, game_board, card)

def main_2(player, gameDisplay, display_size, game_board):
    print("chose action")
    ans = input().lower
    pass_phase = False
    while not pass_phase:
        if ans == "play a creature":
            play_a_creature(player, gameDisplay, display_size, game_board)

        elif ans == "play a sorcery":
            play_a_sorcery(player, gameDisplay, display_size, game_board)

        elif ans = "play an instant":
            play_an_instant(player, gameDisplay, display_size, game_board)
            
        elif ans = "play a land":
            play_a_land(player, gameDisplay, display_size, game_board)

def untap(player, gameDisplay, display_size, game_board):

    for creature in player.battlefield:
        creature.status = "norm"

    for land in player.land_zone:
        land.status = "norm"

    game_board.draw_new_battlefield(player, gameDisplay, display_size)

def draw(player, gameDisplay, display_size, game_board):
    player.current_hand.append(player.deck[0])
    player.deck.pop(0)

    game_board.draw_new_hand(player, gameDisplay, display_size)

def mulligan(player, gameDisplay, display_size, n, game_board):
    print("would you liek to muligan? yes/no")
    ans = input().lower()
    while ans:
        if ans == "yes":
            for card in player.current_hand:
                player.deck.append(card)
            player.current_hand = []
            shuffle_deck(player)
            n -= 1
            deal_cards(player, gameDisplay, display_size, n)
            if n != 0:
                mulligan(player, gameDisplay, display_size, n)
            return

        elif ans == "no":
            return

        else:
            print("invalid anwser please write yes or no")
            print("would you liek to muligan? yes/no")
            ans = input().lower()



def deal_cards(player gameDisplay, display_size, n, game_board):
    
    for i in range(n):
        player.current_hand.append(player.deck.pop(0))
    game_board.draw_hand(player, gameDisplay, display_size)




def deck_selection():
    f = open("./personal_decks/deck_1", "rb")
    player_deck = pickle.load(f)
    f.close()

    return player_deck


def my_quit():
    pygame.quit()
    quit()


def shuffle_deck(player):
    shuffle(player.deck)
