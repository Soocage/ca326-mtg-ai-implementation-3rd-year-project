import pygame
import sys
import board

class Ai():
    def __init__(self, name):
        self.deck = []
        self.name = name
        self.life = 20
        self.hand = []
        self.graveyard = []
        self.land_zone = []
        self.battlefield = []
        self.land_flag = False
        self.mana = ""
        self.state = ""




    def play_land(self):
        for card in self.hand:
            if card.card_type == "Land" and self.land_flag == False:
                self.land_zone.append(card)
                self.hand.remove(card)
                self.land_flag = True
                return 

    def play_creature(self, gameBoard):

        available_lands = 0
        for land in board.PLAYER_2_LAND_SPRITE_CARD_GROUP:
            if land.card.tapped != True:
                available_lands += 1

        for card in self.hand:
            if card.card_type == "Creature":
                a = "b"