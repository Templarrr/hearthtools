from api_tools.tools import get_all_cards_names, get_cards_by_rarity


class Mask(object):
    """
    Class for applying masks to collection in case deck construction have some restraints.
    Will be useful for Standard game mode and some deck-constructing challenges.
    """

    def __init__(self):
        """
        Init mask with all 1s - which mean that by default you can use any card.
        :return:
        """
        self.cards = {}
        self.allow_all()

    def allow_all(self):
        self.allow_card_list(get_all_cards_names())

    def forbid_all(self):
        self.forbid_card_list(get_all_cards_names())

    def allow_card_list(self, card_list):
        for card_name in card_list:
            self.allow_card(card_name)

    def forbid_card_list(self, card_list):
        for card_name in card_list:
            self.forbid_card(card_name)

    def allow_rarity(self, rarity):
        """
        :param rarity: one from ['Legendary', 'Epic', 'Rare', 'Common', 'Free']
        """
        self.allow_card_list(get_cards_by_rarity(rarity))

    def forbid_rarity(self, rarity):
        """
        :param rarity: one from ['Legendary', 'Epic', 'Rare', 'Common', 'Free']
        """
        self.forbid_card_list(get_cards_by_rarity(rarity))

    def allow_card(self, card_name):
        self.cards[card_name] = 1

    def forbid_card(self, card_name):
        self.cards[card_name] = 0

    @property
    def allowed_cards(self):
        return [card for card in self.cards if self.cards[card] == 1]

    @property
    def forbidden_cards(self):
        return [card for card in self.cards if self.cards[card] == 0]

    def inverse(self):
        for card in self.cards:
            self.cards[card] = 1 - self.cards[card]
