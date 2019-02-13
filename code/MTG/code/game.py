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

    shuffle_decks(player_1, player_2)
    board.draw_decks(player_1, player_2, gameDisplay, display_size)
    deal_cards()
    mulligan()

    pygame.display.update()

    
    while player_1.life > 0 or player_2.life > 0:           
            untap()
            draw()
            main_1()
            combat()
            main_2()
            end_step()

    get_winner(player_1, player_2)

def deck_selection():
    f = open("./personal_decks/deck_1", "rb")
    player_deck = pickle.load(f)
    f.close()

    return player_deck


def my_quit():
    pygame.quit()
    quit()


def shuffle_decks(player_1, player_2):
    shuffle(player_1.deck)
    shuffle(player_2.deck)