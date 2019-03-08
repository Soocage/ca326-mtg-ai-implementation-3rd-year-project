import unittest
from mtg import *

class testDamage(unittest.TestCase):


	def testDamageStep(self):
		damage = 2
		self.assertTrue(game.damage_creature())