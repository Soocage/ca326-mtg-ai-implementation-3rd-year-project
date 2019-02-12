import pygame
import sys
import player
import board
import deck


pygame.init()
pygame.mixer.init()



def game_initialise(gameDisplay, display_size):

    (display_w, display_h) = display_size

    player_deck = deck_selection()
    opponent_deck = deck_selection()

    player_1 = player.Player("Sean", player_deck)
    player_2 = player.Player("AI_Dusty", opponent_deck)
    
    board.draw_board(gameDisplay, display_w, display_h, player_1, player_2)
    pygame.display.update()

    exitGame = False
    while not exitGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                my_quit()






def deck_selection():
    player_deck = deck.Deck("my_deck", [])
    return player_deck


def my_quit():
    pygame.quit()
    quit()