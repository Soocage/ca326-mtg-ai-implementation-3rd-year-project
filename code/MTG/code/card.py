class Card():
	def __init__ (self, name, card_type, colour, mana_cost, texture):
		self.name = name
		self.card_type = card_type
		self.colour = colour
		self.mana_cost = mana_cost
		self.texture = texture


class Creature(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, power, toughness, keyword = None):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.power = power
		self.toughness = toughness
		self.keyword = keyword

class Sorcery(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, targets, value, effect):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.targets = targets
		self.value = value
		self.effect = effect

class Instant(Card):
	def __init__ (self, name, card_type, colour, mana_cost, texture, targets, value, effect):
		Card.__init__(self, name, card_type, colour, mana_cost, texture)
		self.targets
		self.value
		self.effect


