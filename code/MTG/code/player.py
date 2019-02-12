class Player():

    def __init__(self, name, deck):
        self.deck = deck
        self.name = name
        self.life = 20
        self.hand = []
        self.graveyard = []
        self.land_zone = []
        self.battlefield = []