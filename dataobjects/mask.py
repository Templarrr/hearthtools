from api_tools.tools import get_all_cards_names


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
        for card_name in get_all_cards_names():
            self.allow_card(card_name)

    def forbid_all(self):
        for card_name in get_all_cards_names():
            self.forbid_card(card_name)

    def allow_card(self, card_name):
        self.cards[card_name] = 1

    def forbid_card(self, card_name):
        self.cards[card_name] = 0
