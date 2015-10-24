class Card(object):
    def __init__(self):
        self.cardId = ''
        self.name = ''
        self.cardSet = ''
        self.type = ''
        self.faction = ''
        self.rarity = ''
        self.cost = 0
        self.attack = 0
        self.health = 0
        self.durability = 0
        self.text = ''
        self.inPlayText = ''
        self.race = ''
        self.flavor = ''
        self.artist = ''
        self.collectible = False
        self.elite = False
        self.playerClass = 'Neutral'
        self.howToGet = ''
        self.howToGetGold = ''
        self.img = ''
        self.imgGold = ''
        self.locale = 'enUS'
        self.mechanics = []

    def fill_from_dict(self, data):
        for key in data:
            if key in self.__dict__:
                self.__dict__[key] = data[dict]

    def get_dict(self):
        return self.__dict__