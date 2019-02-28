import pygame
import sys
import board
import itertools


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

    def calculate_combinations(self, gameBoard, opponent):
        print("########Lands##########")
        print(self.land_zone)
        number_of_available_lands = self.check_available_lands()
        list_of_available_cards = []
        for card in self.hand:
            if (card.card_type == "Creature" or card.card_type == "Instant" or card.card_type == "Sorcery") and (self.check_card_cost(card) <= number_of_available_lands):
                list_of_available_cards.append(card)
        list_of_combinations = []
        for n in range(len(list_of_available_cards)+1):
            for combi in itertools.combinations(list_of_available_cards, n):
                list_of_combinations.append(combi)

        copy_list_of_combinations = list_of_combinations[:]
        for combination in copy_list_of_combinations:
            mana_sum = 0
            for card in combination:
                mana_sum += self.check_card_cost(card)
            if mana_sum > number_of_available_lands:
                list_of_combinations.remove(combination)

        return list_of_combinations

    def check_available_lands(self):
        counter = 0
        for card in self.land_zone:
            if card.tapped != True:
                counter += 1
        return counter

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

    def play_a_card(self,gameBoard,opponent):
        combinations = calculate_combinations(gameBoard, opponent)
        list_of_moves = []
        for combination in combinations:
            list_of_moves.append((self.combination_cost(combination, opponent), combination))
        list_of_moves = sorted(list_of_moves)
        chosen_move = list_of_moves[0][1]
        order = card_cost(chosen_move)
        return order


    def combination_cost(self, combination, opponent):
