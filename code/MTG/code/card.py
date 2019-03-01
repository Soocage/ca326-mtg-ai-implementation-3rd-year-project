class Card():
	def __init__ (self, name, card_type, colour, mana_cost, texture):
		self.name = name
		self.card_type = card_type
		self.colour = colour
		self.mana_cost = mana_cost
		self.texture = texture


class Creature(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, power, toughness, keyword = ""):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.power = power
		self.toughness = toughness
		self.keyword = keyword
		self.power_modifier = 0
		self.toughness_modifier = 0
		self.counter = ("", 0, 0)
		self.tmp_keyword = ""
		self.combat_state = ""
		self.tapped = False
		self.summon_sick = True

class Sorcery(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, targets, value, effect):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.targets = targets
		self.value = value
		self.effect = effect

class Instant(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, targets, value, effect):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.targets = targets
		self.value = value
		self.effect = effect

class Land(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, effect, tapped = False):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.effect = effect
		self.tapped = tapped
