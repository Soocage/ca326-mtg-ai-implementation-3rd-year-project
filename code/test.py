import unittest
import sys

sys.path.append('./code')

import game
import card
import player
import deck
import copy
from card import Land
from card import Instant
import ai

class test_Status(unittest.TestCase):

	def testStatus(self):
		player_1_life = 20
		player_2_life = 20
		player_1_deck_len = 60
		player_2_deck_len = 60

		self.assertTrue(player_1_life > 0 and player_2_life > 0 and player_1_deck_len > 0 and player_2_deck_len > 0)

		player_1_life = 10
		player_2_life = 5
		player_1_deck_len = 42
		player_2_deck_len = 20

		self.assertTrue(player_1_life > 0 and player_2_life > 0 and player_1_deck_len > 0 and player_2_deck_len > 0)

		player_1_life = 0
		player_2_life = 20
		player_1_deck_len = 60
		player_2_deck_len = 60

		self.assertFalse(player_1_life > 0 and player_2_life > 0 and player_1_deck_len > 0 and player_2_deck_len > 0)

		player_1_life = 0
		player_2_life = -5
		player_1_deck_len = 60
		player_2_deck_len = 60

		self.assertFalse(player_1_life > 0 and player_2_life > 0 and player_1_deck_len > 0 and player_2_deck_len > 0)

		player_1_life = 30
		player_2_life = 20
		player_1_deck_len = -10
		player_2_deck_len = 60

		self.assertFalse(player_1_life > 0 and player_2_life > 0 and player_1_deck_len > 0 and player_2_deck_len > 0)
		pass

class test_Damage(unittest.TestCase):

	def testDamageStep(self):
		test_creature = card.Creature("test", "Creature", "B", "B", "", 4, 2)
		damage = 2
		self.assertTrue(game.Game.damage_creature(game.Game,test_creature, damage))

		test_creature = card.Creature("test", "Creature", "B", "B", "", 4, 1)
		damage = 2
		self.assertTrue(game.Game.damage_creature(game.Game,test_creature, damage))

		test_creature = card.Creature("test", "Creature", "B", "B", "", 4, 4)
		damage = 2
		self.assertFalse(game.Game.damage_creature(game.Game,test_creature, damage))

		test_creature = card.Creature("test", "Creature", "B", "B", "", 0, 2)
		damage = 4
		self.assertTrue(game.Game.damage_creature(game.Game,test_creature, damage))
		pass

class test_DealCards(unittest.TestCase):

	def testDealCards(self):
		test_player = player.Player("test")
		test_card = card.Creature("test", "Creature", "B", "B", "", 4, 2)
		test_deck = deck.Deck("test_deck", [test_card]*60)

		test_deck_copy = copy.copy(test_deck)
		test_player.hand = []
		test_player.deck = test_deck_copy

		game.Game.deal_cards(game.Game, test_player, 7)
		self.assertTrue(len(test_player.hand) == 7)
		self.assertFalse(len(test_player.hand) == 6)

		test_deck_copy = copy.copy(test_deck)
		test_player.hand = []
		test_player.deck = test_deck_copy

		game.Game.deal_cards(game.Game, test_player, 0)
		self.assertTrue(len(test_player.hand) == 0)
		self.assertFalse(len(test_player.hand) == 1)

		test_deck_copy = copy.copy(test_deck)
		test_player.hand = []
		test_player.deck = test_deck_copy

		game.Game.deal_cards(game.Game, test_player, 5)
		self.assertTrue(len(test_player.hand) == 5)
		self.assertFalse(len(test_player.hand) == 1)

class test_AddMana(unittest.TestCase):

	def testAddMana(self):
		forest = card.Land("forest", "Land", "G", 0, "", "mana")
		swamp = card.Land("swamp", "Land", "B", 0, "", "mana")
		plains = card.Land("plains", "Land", "W", 0, "", "mana")
		mountain = card.Land("mountain", "Land", "R", 0, "", "mana")
		island = card.Land("island", "Land", "U", 0, "", "mana")

		test_player = player.Player("test")
		test_player.mana = []

		game.Game.add_mana(game.Game, test_player, forest)
		self.assertTrue(test_player.mana == "G")

		test_player.mana = []

		game.Game.add_mana(game.Game, test_player, swamp)
		self.assertTrue(test_player.mana == "B")

		test_player.mana = []

		game.Game.add_mana(game.Game, test_player, plains)
		self.assertTrue(test_player.mana == "W")

		test_player.mana = []

		game.Game.add_mana(game.Game, test_player, mountain)
		self.assertTrue(test_player.mana == "R")

		test_player.mana = []

		game.Game.add_mana(game.Game, test_player, island)
		self.assertTrue(test_player.mana == "U")

		test_player.mana = []

		game.Game.add_mana(game.Game, test_player, swamp)
		game.Game.add_mana(game.Game, test_player, plains)
		self.assertTrue(test_player.mana == "BW")


class test_CardCost(unittest.TestCase):

	def testCardCost(self):
		test_card_1 = card.Creature("test", "Creature", "B", "B", "", 4, 2)
		test_card_2 = card.Creature("test", "Creature", "W", "W", "", 4, 2)
		test_card_3 = card.Creature("test", "Creature", "R", "2R", "", 4, 2)
		test_card_4 = card.Instant("test", "Creature", "G", "5G", "", 4, 2, "")

		self.assertTrue(game.Game.check_card_cost(game.Game, test_card_1) == 1)
		self.assertTrue(game.Game.check_card_cost(game.Game, test_card_2) == 1)
		self.assertTrue(game.Game.check_card_cost(game.Game, test_card_3) == 3)
		self.assertTrue(game.Game.check_card_cost(game.Game, test_card_4) == 6)


class test_ClearMana(unittest.TestCase):

	def test_ClearMana(self):
		test_player = player.Player("test")
		game.Game.clear_mana(game.Game, test_player)
		self.assertTrue(test_player.mana == "")

		test_player.mana = ["BWWWW"]
		game.Game.clear_mana(game.Game, test_player)
		self.assertTrue(test_player.mana == "")

		test_player.mana = ["GRWBU"]
		game.Game.clear_mana(game.Game, test_player)
		self.assertFalse(test_player.mana == "GRWBU")

class test_PlayALand(unittest.TestCase):

	def testt_PlayALand(self):
		test_Ai = ai.Ai("test_ai", "red")

		forest = card.Land("forest", "Land", "G", 0, "", "mana")
		test_card_1 = card.Creature("test", "Creature", "B", "B", "", 4, 2)

		test_Ai.land_flag = False
		test_Ai.hand = [forest]*3
		test_Ai.play_land()

		self.assertTrue(test_Ai.hand == [forest, forest] and test_Ai.land_zone == [forest])

		test_Ai.land_flag = False
		test_Ai.hand = [forest]*3 + [test_card_1]
		test_Ai.land_zone = []

		test_Ai.play_land()
		self.assertTrue(test_Ai.hand == [forest, forest, test_card_1] and test_Ai.land_zone == [forest])

		test_Ai.land_flag = False
		test_Ai.hand = [test_card_1]
		test_Ai.land_zone = []

		test_Ai.play_land()
		self.assertTrue(test_Ai.hand == [test_card_1] and test_Ai.land_zone == [])




if __name__ == "__main__":
	test_classes_to_run = [test_Damage, test_Status, test_DealCards, test_AddMana, test_CardCost, test_ClearMana, test_PlayALand]
	loader = unittest.TestLoader()
	suites_list = []

	for test_class in test_classes_to_run:
		suite = loader.loadTestsFromTestCase(test_class)
		suites_list.append(suite)


	big_suite = unittest.TestSuite(suites_list)
	runner = unittest.TextTestRunner()
	results = runner.run(big_suite)
