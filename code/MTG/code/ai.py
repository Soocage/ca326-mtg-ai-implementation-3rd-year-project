import pygame
import sys
import board
import itertools
import random


class Ai():
    def __init__(self, name, ai_mode):
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
        self.ai_mode = ai_mode

    def play_land(self):
        for card in self.hand:
            if card.card_type == "Land" and self.land_flag == False:
                self.land_zone.append(card)
                self.hand.remove(card)
                self.land_flag = True
                return

    def check_card_playable(self,card):
        available_lands = self.check_available_lands()
        card_cost = self.check_card_cost(card)
        return available_lands >= card_cost

    def calculate_combinations(self, gameBoard, opponent):
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
                print(card, card.name)
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
        combinations = self.calculate_combinations(gameBoard, opponent)
        list_of_moves = []
        for combination in combinations:
            if self.ai_mode == "red":
                list_of_moves.append((self.combination_cost_red(combination, opponent), combination))
            #elif self.ai_mode == "green":
                #list_of_moves.append((self.combination_cost_green(combination, opponent), combination))
            #elif self.ai_mode == "black"
                #list_of_moves.append((self.combination_cost_black(combination, opponent), combination))
            #elif self.ai_mode ==  "white":
                #list_of_moves.append((self.combination_cost_white(combination, opponent), combination))
            #elif self.ai_mode == "blue":
                #list_of_moves.append((self.combination_cost_blue(combination, opponent), combination))
        list_of_moves = self.sort_combinations(list_of_moves)
        #chosen_move = list_of_moves[0][1]
        #order = card_cost(chosen_move)
        order = list_of_moves[0][1]
        return order


    def sort_combinations(self, list_of_moves):
        for i in range (1, len(list_of_moves)):
            key = list_of_moves[i]
            j = i-1
            while j >= 0 and key[0] < list_of_moves[j][0]:
                list_of_moves[j+1] = list_of_moves[j]
                j -= 1
            list_of_moves[j+1] = key
        return list_of_moves


    def combination_cost_red(self, combination, opponent): 
        combination_cost = 1.0
        number_of_enemy_creatures = 0
        number_of_ai_creatures = 0

        ai_combined_toughness = self.calculate_combined_toughness()
        player_combined_toughness = self.calculate_combined_toughness(opponent)
        ai_combined_power = self.calculate_combined_power()
        player_combined_power = self.calculate_combined_power(opponent)

        for creature in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            number_of_enemy_creatures += 1

        for creature in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            number_of_ai_creatures += 1

        for card in combination:
            if number_of_ai_creatures < number_of_enemy_creatures:
                if card.card_type == "Creature":
                    if ai_combined_power + card.power <= player_combined_toughness: 
                        combination_cost -= 0.11
                    elif ai_combined_power + card.power > player_combined_toughness:
                        combination_cost -= 0.12
                    if ai_combined_toughness + card.toughness >= player_combined_power:
                        combination_cost -= 0.03
                    if card.keyword == "Haste":
                        combination_cost -= 0.005
                elif card.card_type == "Sorcery" or card.card_type == "Instant":
                    if card.effect == "Damage":
                        if "creature" in card.targets:
                            for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if int(card.value) >= (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier):
                                    combination_cost -= 0.005

                        if "opponent" in card.targets:
                            if int(card.value) > int(opponent.life)*(0.2):
                                combination_cost -= 0.005
                            elif int(card.value) == int(opponent.life):
                                combination_cost -= combination_cost
                                return combination_cost
                            elif int(card.value) < int(opponent.life)*(0.2):
                                combination_cost += 0.01


            elif number_of_ai_creatures == number_of_enemy_creatures:
                if card.card_type == "Creature":
                    if ai_combined_power + card.power <= player_combined_toughness: 
                        combination_cost -= 0.055
                    elif ai_combined_power + card.power > player_combined_toughness:
                        combination_cost -= 0.015
                    if ai_combined_toughness + card.toughness >= player_combined_power:
                        combination_cost -= 0.015
                    if card.keyword == "Haste":
                        combination_cost -= 0.01

                if card.card_type == "Sorcery" or card.card_type == "Instant":
                    if card.effect == "Damage":
                        if "creature" in card.targets:
                            for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if int(card.value) >= (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier):
                                    combination_cost -= 0.02

                        if "opponent" in card.targets:
                            if int(card.value) >= int(opponent.life)*(0.1):
                                combination_cost -= 0.1
                            elif card.calue == int(opponent.life):
                                combination_cost -= combination
                                return combination_cost
                            elif int(card.value) < int(opponent.life)*(0.1):
                                combination_cost -= 0.005

            elif number_of_ai_creatures > number_of_enemy_creatures:
                if card.card_type == "Creature":
                    if ai_combined_power + card.power <= player_combined_toughness: 
                        combination_cost -= 0.005
                    elif ai_combined_power + card.power > player_combined_toughness:
                        combination_cost -= 0.002
                    if ai_combined_toughness + card.toughness >= player_combined_power:
                        combination_cost -= 0.005
                    if card.keyword == "Haste":
                        combination_cost -= 0.02

                if card.card_type == "Sorcery" or card.card_type == "Instant":
                    print("friends")
                    if card.effect == "Damage":
                        if "creature" in card.targets:
                            for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                                if int(card.value) >= (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier):
                                    combination_cost -= 0.002

                        if "opponent" in card.targets:
                            if int(card.value) >= int(opponent.life)*(0.1):
                                combination_cost -= 0.4
                            elif card.calue == int(opponent.life):
                                combination_cost -= combination
                                return combination_cost
                            elif int(card.value) < int(opponent.life)*(0.1):
                                combination_cost -= 0.2
        return combination_cost

    def calculate_combined_toughness(self, player = None):
        combined_toughness = 0
        if player == None:
            for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                combined_toughness += (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier)

        else:
            for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                combined_toughness += (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier)
        return combined_toughness

    def calculate_combined_power(self, player = None):
        combined_power = 0
        if player == None:
            for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                combined_power += (creature_sprite.card.power + creature_sprite.card.power_modifier)
        else:
            for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                combined_power += (creature_sprite.card.power + creature_sprite.card.power_modifier)
        return combined_power


    def calculate_target(self,opponent, opponent_weight,potential_creatures):
        ai_combined_toughness = self.calculate_combined_toughness()
        player_combined_toughness = self.calculate_combined_toughness(opponent)
        ai_combined_power = self.calculate_combined_power()
        player_combined_power = self.calculate_combined_power(opponent)

        for creature_weight in potential_creatures:
            centage = (int(creature_weight[1].power)/player_combined_power)
            if creature_weight[1].tapped == True:
                creature_weight[0] += (creature_weight[0]*centage)/2
            else:
                creature_weight[0] += creature_weight[0]*centage
            if creature_weight[1].keyword != "":
                centage = creature_weight[0]*(0.3)
                creature_weight[0] += centage

        sorted_creatures = self.sort_combinations(potential_creatures)
        if len(sorted_creatures) > 0:
            target_creature = sorted_creatures[-1]
        else:
            return opponent

        rand_creature_weight = float(random.randrange(90, 110))/100
        rand_player_weight = float(random.randrange(90, 110))/100

        opponent_weight = opponent_weight * rand_player_weight
        target_creature[0] = target_creature[0] * rand_creature_weight
        print(target_creature[0], " and ", opponent_weight)

        if opponent_weight >= target_creature[0]:
            return opponent
        else:
            return target_creature[1]



