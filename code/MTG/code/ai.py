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

        if self.ai_mode == "red":
            self.ai_life_weight = 0.15
            self.ai_battlefield_weight = 0.20
            self.opponent_battlefield_weight = 0.10
            self.open_mana_weight = 0.25
            self.opponent_life_weight = 0.30

            self.spell_weight = 4/5
            self.creature_weight = 1 - self.spell_weight

        elif self.ai_mode == "blue":
            self.ai_life_weight = 0.15
            self.ai_battlefield_weight = 0.20 
            self.opponent_battlefield_weight = 0.10
            self.open_mana_weight = 0.25
            self.opponent_life_weight = 0.30

            self.spell_weight = 3/5
            self.creature_weight = 1 - self.spell_weight


        elif self.ai_mode == "white":
            self.ai_life_weight = 0.15
            self.ai_battlefield_weight = 0.20 
            self.opponent_battlefield_weight = 0.10
            self.open_mana_weight = 0.25
            self.opponent_life_weight = 0.30

            self.spell_weight = 2/5
            self.creature_weight = 1 - self.spell_weight

        elif self.ai_mode == "black":
            self.ai_life_weight = 0.15
            self.ai_battlefield_weight = 0.20 
            self.opponent_battlefield_weight = 0.10
            self.open_mana_weight = 0.25
            self.opponent_life_weight = 0.30

            self.spell_weight = 3/5
            self.creature_weight = 1 - self.spell_weight

        elif self.ai_mode == "green":
            self.ai_life_weight = 0.15
            self.ai_battlefield_weight = 0.20 
            self.opponent_battlefield_weight = 0.10
            self.open_mana_weight = 0.25
            self.opponent_life_weight = 0.30

            self.spell_weight = 1/5
            self.creature_weight = 1 - self.spell_weight





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
                list_of_moves.append((self.combination_cost(combination, opponent), combination))
        print(list_of_moves)
        list_of_moves = self.sort_combinations(list_of_moves)
        chosen_move = list_of_moves[0][1]
        return chosen_move


    def sort_combinations(self, list_of_moves):
        for i in range (1, len(list_of_moves)):
            key = list_of_moves[i]
            j = i-1
            while j >= 0 and key[0] < list_of_moves[j][0]:
                list_of_moves[j+1] = list_of_moves[j]
                j -= 1
            list_of_moves[j+1] = key
        return list_of_moves


    
    def combination_cost(self, combination, opponent):

#        ideal_state = [ai_hp = 20, opponent ==> 0, new_nr_of_creatures > old_number_of_creatures, old_number_of_creatures_oppnent < new_number_of_ceatures_opponent]
        combination_cost = 1.0
        ai_combined_toughness = self.calculate_combined_toughness()
        player_combined_toughness = self.calculate_combined_toughness(opponent)
        ai_combined_power = self.calculate_combined_power()
        player_combined_power = self.calculate_combined_power(opponent)

        for card in combination:
            if card.card_type == "Creature":
                if "Haste" in card.keyword:
                    possible_blockers = []
                    for creature in opponent.battlefield:
                        if creature.tapped == False:
                            possible_blockers.append(creature)
                    if len(possible_blockers) == 0:
                        combination_cost = combination_cost*((card.power+opponent.life) / opponent.life)
                    else:
                        best_blocker = None
                        for blocker in possible_blockers:
                            if best_blocker == None:
                                best_blocker = blocker
                            else:
                                if blocker.toughness > best_blocker.toughness:
                                    best_blocker = blocker
                        combination_cost = combination_cost*(card.power/best_blocker.toughness + card.power)

                if "Flying" in card.keyword:
                    possible_blockers = []
                    for creature in opponent.battlefield:
                        if "Flying" in creature.keyword or "Flying" in creature.temp_keyword:
                            if creature.tapped == False:
                                possible_blockers.append(creature)
                    if len(possible_blockers) == 0:
                        combination_cost = combination_cost*((card.power+opponent.life) / opponent.life)
                    else:
                        best_blocker = None
                        for blocker in possible_blockers:
                            if best_blocker == None:
                                best_blocker = blocker
                            else:
                                if blocker.toughness > best_blocker.toughness:
                                    best_blocker = blocker
                        combination_cost = combination_cost*(card.power/best_blocker.toughness + card.power)

                if "Vigiliance" in card.keyword:
                    possible_blockers = []
                    for creature in opponent.battlefield:
                        if creature.tapped == False:
                            possible_blockers.append(creature)
                    if len(possible_blockers) == 0:
                        combination_cost = combination_cost*((card.power+opponent.life) / opponent.life)
                    else:
                        best_blocker = None
                        for blocker in possible_blockers:
                            if best_blocker == None:
                                best_blocker = blocker
                            else:
                                if blocker.toughness > best_blocker.toughness:
                                    best_blocker = blocker
                        combination_cost = combination_cost*(card.power/best_blocker.toughness + card.power)

                        best_attacker = None
                        for attacker in possible_blockers:
                            if best_attacker == None:
                                best_attacker = attacker
                            else:
                                if attacker.power > best_attacker.power:
                                    best_attacker = attacker
                        combination_cost = combination_cost*(1-(best_attacker.power/card.toughness + best_attacker.power))

                if "LifeLink" in card.keyword:
                    combination_cost = combination_cost*((card.power + self.life)/self.life)

                if "Trample" in card.keyword:
                    possible_blockers = []
                    for creature in opponent.battlefield:
                        if creature.tapped == False:
                            possible_blockers.append(creature)
                    if len(possible_blockers) > 0:
                        combination_cost = combination_cost*(card.power/(card.power + best_blocker.toughness))
                        if card.power > best_blocker.toughness:
                            combination_cost = combination_cost*((card.power - best_blocker.toughness) + opponent.life/opponent.life)

                if "Deathtouch" in card.keyword:
                    best_attacker = None
                    for creature in opponent.battlefield:
                        if best_attacker == None:
                            best_attacker = creature
                        else:
                            if creature.power > best_attacker.power:
                                best_attacker = creature

                    combination_cost = combination_cost*(1-(best_attacker.power/card.toughness + best_attacker.power))
                    combination_cost = combination_cost*(card.power / (card.power + best_attacker.toughness))

                if len(opponent.battlefield) > 0:
                    combination_cost = combination_cost*((ai_combined_power + card.power) / player_combined_toughness)
                    if player_combined_power > 0:
                        combination_cost = combination_cost*((ai_combined_toughness + card.toughness) / player_combined_power)

                combination_cost = combination_cost * self.creature_weight

            elif card.card_type == "Sorcery" or card.card_type == "Instant":
                if card.effect == "Draw":
                    combination_cost = combination_cost*((len(self.hand))/(len(self.hand)+7))

                if card.effect == "Tap":
                    best_attacker = None
                    best_blocker = None
                    for creature in self.battlefield:
                        if best_blocker == None:
                            best_blocker = creature
                        else:
                            if creature.toughness > best_blocker.toughness:
                                best_blocker = creature.toughness

                    for creature in opponent.battlefield:
                        if best_attacker == None:
                            best_attacker = creature
                        else:
                            if creature.power > best_attacker.power:
                                best_attacker = creature

                    if best_blocker.toughness <= best_attacker.attacker:
                        combination_cost = combination_cost*((player_combined_toughness + player_combined_power) - (best_attacker.power + best_attacker.toughness)) / (player_combined_power + player_combined_toughness)

                if card.effect == "Damage":
                    player_factor = 1 - ((opponent.life - int(card.value))/opponent.life)
                    potential_targets = []
                    best_target = None
                    for creature in opponent.battlefield:
                        if creature.toughness <= int(card.value):
                            potential_targets.append(creature)

                    for creature in potential_targets:
                        if best_target == None:
                            best_target = creature
                        else:
                            if creature.power > best_target.power:
                                best_target = creature
                    
                    if best_target != None:
                        if player_combined_power > 0:
                         creature_factor = 1 -((player_combined_power - best_target.power)/player_combined_power)
                        else:
                            creature_factor = 1 -((player_combined_toughness - best_target.toughness) / player_combined_toughness)
                        combination_cost = combination_cost*((player_factor + creature_factor)/2)

                if card.effect == "Bounce":
                    best_attacker = None
                    best_blocker = None
                    for creature in self.battlefield:
                        if best_blocker == None:
                            best_blocker = creature
                        else:
                            if creature.toughness > best_blocker.toughness:
                                best_blocker = creature.toughness

                    for creature in opponent.battlefield:
                        if best_attacker == None:
                            best_attacker = creature
                        else:
                            if creature.power > best_attacker.power:
                                best_attacker = creature

                    if best_blocker.toughness <= best_attacker.attacker:
                        combination_cost = combination_cost*((player_combined_toughness + player_combined_power) - (best_attacker.power + best_attacker.toughness)) / (player_combined_power + player_combined_toughness)


                if card.effect == "Combat_Creature":
                    ranked_creatures = []
                    opponent_battlefield_copy = opponent.battlefield[:]
                    while len(ranked_creatures) != len(opponent.battlefield):
                        best_creature = None

                        for creature in opponent_battlefield_copy:
                            if best_creature == None:
                                best_creature = creature
                            else:
                                if best_creature.power < creature.power:
                                    best_creature = creature

                        ranked_creatures.append(best_creature)
                        opponent_battlefield_copy.remove(best_creature)

                    player_target = None
                    enemy_target = None
                    found_targets = False
                    i = 0
                    while i < len(ranked_creatures) and found_targets == False:
                        tmp_target = ranked_creatures[i]
                        for creature in self.battlefield:
                            if (creature.power >= tmp_target.toughness) and (creature.toughness > tmp_target.power):
                                player_target = creature
                                enemy_target = tmp_target
                                found_targets = True
                        i += 1

                    if found_targets:
                        combination_cost = combination_cost*((player_combined_power - enemy_target.power)/ player_combined_power)

                if card.effect == "search_land":

                    total_mana_cost = 0
                    for card in self.hand:
                        total_mana_cost += self.check_card_cost(card)

                    combination_cost = combination_cost*(int(card.value)/(total_mana_cost/len(self.hand)))

                if card.effect == "Gain_life":

                    combination_cost = combination_cost*1-((self.life + int(card.value)) / 20)

                if card.effect == "Exile" and card.effect == "Destroy":
                    best_attacker = None
                    for creature in opponent.battlefield:
                        if best_attacker == None:
                            best_attacker = creature
                        else:
                            if best_attacker.power < creature.power:
                                best_attacker = creature

                    combination_cost = combination_cost*((player_combined_power - best_attacker.power)/ player_combined_power)

                if card.effect == "Discard":
                    combination_cost = combination_cost*(len(opponent.hand) / 7)

                if card.effect == "Reanimate":
                    possible_targets = []

                    for dead_card in self.graveyard:
                        if dead_card.card_type == "Creature":
                            possible_targets.append(card)

                    for dead_card in opponent.graveyard:
                        if dead_card.card_type == "Creature":
                            possible_targets.append(card)

                    targets = []
                    for i in range(card.value):
                        best_target = None
                        for target in possible_targets:

                            if best_target == None:
                                best_target = target
                            else:
                                if ai_combined_toughness <= player_combined_power:
                                    if best_target.toughness < target.toughness:
                                        best_target = target
                                else:
                                    if best_target.power < target.power:
                                        best_target = target

                        targets.append(best_target)
                    targets_toughness = 0
                    targets_power = 0
                    for creature in target:
                        targets_toughness += creature.toughness
                        targets_power += creature.power

                    if ai_combined_toughness <= player_combined_power:
                        combination_cost = combination_cost*(ai_combined_toughness/(ai_combined_toughness+targets_toughness))

                combination_cost = combination_cost*(self.spell_weight)

        return combination_cost




    def calculate_combined_toughness(self, player = None, battlefield = None):
        if battlefield == None:
            combined_toughness = 0
            if player == None:
                for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                    combined_toughness += (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier)

            else:
                for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                    combined_toughness += (creature_sprite.card.toughness + creature_sprite.card.toughness_modifier)
            return combined_toughness

        else:
            combined_toughness = 0
            if player == None:
                for creature in battlefield:
                    combined_toughness += (creature.toughness + creature.toughness_modifier)

            else:
                for creature in battlefield:
                    combined_toughness += (creature.toughness + creature.toughness_modifier)
            return combined_toughness



    def calculate_combined_power(self, player = None, battlefield = None):
        if battlefield == None:
            combined_power = 0
            if player == None:
                for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
                    combined_power += (creature_sprite.card.power + creature_sprite.card.power_modifier)
            else:
                for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
                    combined_power += (creature_sprite.card.power + creature_sprite.card.power_modifier)
            return combined_power
        else:
            combined_power = 0
            if player == None:
                for creature in battlefield:
                    combined_power += (creature.power + creature.power_modifier)
            else:
                for creature in battlefield:
                    combined_power += (creature.power + creature.power_modifier)
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

        if opponent_weight >= target_creature[0]:
            return opponent
        else:
            return target_creature[1]

    def attacker_list(self, opponent, gameBoard):

        potential_attackers = []
        for creature_sprite in board.PLAYER_2_BATTLEFIELD_SPRITE_CARD_GROUP:
            if (creature_sprite.card.summon_sick == False or creature_sprite.card.keyword == "Haste") and creature_sprite.card.tapped == False:
                potential_attackers.append(creature_sprite.card)

        list_of_combinations_attackers = []
        for n in range(len(potential_attackers)+1):
            for combi in itertools.combinations(potential_attackers, n):
                list_of_combinations_attackers.append(combi)

        potential_defenders = []
        for creature_sprite in board.PLAYER_1_BATTLEFIELD_SPRITE_CARD_GROUP:
            if creature_sprite.card.tapped == False:
                potential_defenders.append(creature_sprite.card)

        list_of_combinations_defenders = []
        for n in range(len(potential_defenders)+1):
            for combi in itertools.combinations(potential_defenders, n):
                list_of_combinations_defenders.append(combi)

        cost_of_attacking = self.check_cost_of_attacking(list_of_combinations_attackers, list_of_combinations_defenders,opponent)
        # [value, [combi, [AI life, Opponent Life, AI battlefield, Opponent Battlefield]]]
        ideal_board_state = [self.life, 0, self.battlefield, []]
        chosen_move = None
        i = 0
        for move in cost_of_attacking:
            if chosen_move == None:
                chosen_move = move
            else:
                chosen_move_value = 0
                chosen_move_ai_life = chosen_move[1][1][0]
                chosen_move_opponent_life = chosen_move[1][1][1]
                chosen_move_ai_battlefield = chosen_move[1][1][2]
                chosen_move_opponent_battlefield = chosen_move[1][1][3]

                move_value = 0
                move_ai_life = move[1][1][0]
                move_opponent_life = move[1][1][1]
                move_ai_battlefield = move[1][1][2]
                move_opponent_battlefield = move[1][1][3]

                opponent_ideal_life_change  = opponent.life

                chosen_move_opponent_life_change = opponent.life - chosen_move_opponent_life
                move_opponent_life_change = opponent.life - move_opponent_life

                if len(opponent.battlefield) <= 0:
                    opp_bat = 1
                else:
                    if len(chosen_move[1][1][3]) <= 0:
                        opp_bat = 1
                    else:
                        opp_bat = (len(opponent.battlefield)/len(chosen_move[1][1][3]))

                chosen_move_average_score = ((chosen_move_ai_life/ideal_board_state[0]) + (chosen_move_opponent_life_change/opponent_ideal_life_change) + (len(self.battlefield)/len(chosen_move[1][1][2])) + opp_bat) / 4

                move_average_score = ((move_ai_life/ideal_board_state[0]) + (move_opponent_life_change/opponent_ideal_life_change) + (len(self.battlefield)/len(move[1][1][2])) + opp_bat) / 4

                if move_average_score > chosen_move_average_score:
                    chosen_move = move

        return chosen_move[1][0]




    def check_cost_of_attacking(self, potential_attackers, potential_defenders, opponent):
        ai_combined_toughness = self.calculate_combined_toughness()
        player_combined_toughness = self.calculate_combined_toughness(opponent)
        ai_combined_power = self.calculate_combined_power()
        player_combined_power = self.calculate_combined_power(opponent)

        cost_of_attacking = []
        list_of_end_of_battle_board_states = []

        #[AI life, Opponent Life, AI battlefield, Opponent Battlefield]
        for combi_attackers in potential_attackers:
            for combi_defenders in potential_defenders:

                if len(combi_defenders) == 0:
                    temp_list = len(combi_attackers)*[0]
                    list_of_end_of_battle_board_states.append([combi_attackers, self.simulate_battle(combi_attackers, temp_list, opponent)])

                elif len(combi_defenders) < len(combi_attackers):
                    temp_list = len(combi_attackers)*[0]
                    for i in range(len(combi_defenders)):
                        temp_list[i] = combi_defenders[i]
                        for perm in itertools.permutations(temp_list, len(temp_list)):
                            list_of_end_of_battle_board_states.append([combi_attackers, self.simulate_battle(combi_attackers, perm, opponent)])

                elif len(combi_defenders) == len(combi_attackers):
                    for i in range(len(combi_defenders)):
                        for perm in itertools.permutations(combi_defenders, len(combi_defenders)):
                            list_of_end_of_battle_board_states.append([combi_attackers, self.simulate_battle(combi_attackers, combi_defenders, opponent)])

        for combi_and_board_state in list_of_end_of_battle_board_states:
            after_ai_combined_toughness = self.calculate_combined_toughness(None,combi_and_board_state[1][2])
            after_player_combined_toughness = self.calculate_combined_toughness(opponent,combi_and_board_state[1][2])
            after_ai_combined_power = self.calculate_combined_power(None,combi_and_board_state[1][2])
            after_player_combined_power = self.calculate_combined_power(opponent,combi_and_board_state[1][2])

            ai_life_weight = self.ai_life_weight
            ai_battlefield_weight = self.ai_battlefield_weight
            opponent_battlefield_weight = self.opponent_battlefield_weight
            opponent_life_weight = self.opponent_life_weight

            ai_life_weight = ai_life_weight*((combi_and_board_state[1][0]/self.life))

            if len(self.battlefield) > 0:
                ai_battlefield_factor = (((after_ai_combined_power/ai_combined_power) + (after_ai_combined_toughness/ai_combined_toughness) + (len(combi_and_board_state[1][2])/len(self.battlefield))) / 3)
                ai_battlefield_weight = ai_battlefield_weight*ai_battlefield_factor
            else:
                ai_battlefield_weight = self.ai_battlefield_weight

            if len(opponent.battlefield) > 0:
                opponent_battlefield_factor = (((after_player_combined_power/player_combined_power) + (after_player_combined_toughness/player_combined_toughness) + (len(combi_and_board_state[1][3])/len(opponent.battlefield))) / 3)
                opponent_battlefield_weight = opponent_battlefield_weight*opponent_battlefield_factor
            else:
                opponent_battlefield_weight = self.opponent_battlefield_weight

            new_opponent_life = combi_and_board_state[1][1]
            damage_done = opponent.life - new_opponent_life
            opponent_life_factor = 1 - ((opponent.life - damage_done) / opponent.life)
            opponent_life_weight = opponent_life_weight*opponent_life_factor

            value = ai_life_weight + ai_battlefield_weight + opponent_battlefield_weight + opponent_life_weight

            cost_of_attacking.append([value, combi_and_board_state])

        sorted_cost_of_attacking = self.sort_combinations(cost_of_attacking)
        return sorted_cost_of_attacking[:5]







    def simulate_battle(self, combi_attackers, combi_defenders, opponent):
        for attacker in combi_attackers:
            if type(attacker) != int:
                attacker.toughness_modifier = 0
        for defender in combi_defenders:
            if type(defender) != int:
                defender.toughness_modifier = 0

        opponent_health = opponent.life
        ai_health = self.life
        current_ai_battlefield = self.battlefield[:]
        current_player_battlefield = opponent.battlefield[:]

        i = 0
        while i < len(combi_attackers):
            if type(combi_defenders[i]) != int:
                combi_attackers[i].toughness_modifier -= (combi_defenders[i].power + combi_defenders[i].power_modifier)
                combi_defenders[i].toughness_modifier -= (combi_attackers[i].power + combi_attackers[i].power_modifier)
                if combi_attackers[i].toughness + combi_attackers[i].toughness_modifier <= 0:
                    current_ai_battlefield.remove(combi_attackers[i])
                if combi_defenders[i].toughness + combi_defenders[i].toughness_modifier <= 0:
                    current_player_battlefield.remove(combi_defenders[i])
            else:
                opponent_health -= combi_attackers[i].power
            i += 1
        return [ai_health, opponent_health, current_ai_battlefield, current_player_battlefield]
