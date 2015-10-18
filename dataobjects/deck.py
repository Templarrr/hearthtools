import constants


class Deck(object):
    """
    Class for storing information about Hearthstone deck
    """

    def __init__(self):
        self.player_class = ''
        self.name = 'Noname deck'
        self.type = constants.CONSTRUCTED_DECK
        self.cards = {}

    def is_valid(self):
        """
        is this Deck valid to use in Heartstone?
        :return: bool
        """
        return len(self.get_errors()) == 0

    def get_errors(self):
        """
        Get list of errors in deck
        :return: list of str
        """
        errors = []
        if self.player_class not in constants.player_classes:
            errors.append('Invalid class %s' % self.player_class)
        if sum(self.cards.values()) != 30:
            errors.append('Deck should contain 30 cards, this deck contain %d' % sum(self.cards.values()))
        if self.type != constants.ARENA_DECK:
            for card_name, card_count in self.cards:
                if card_count > 2 or card_count < 1:
                    errors.append('Invalid count of card "%s" : %d' % (card_name, card_count))
        errors.extend(self.get_nerfed_deck_errors())
        # TODO add checking for legendary cards - only 1 per deck
        # TODO add checking for class cards - deck should have only class and common cards
        return errors

    def get_nerfed_deck_errors(self):
        """
        Check if this deck was invalidated by card nerfs and return those
        :return: list of str
        """
        errors = []
        if 'Warsong Commander' in self.cards and ('Grim Patron' in self.cards or 'Frothing Berserker' in self.cards):
            errors.append('Patron-Warsong and Berserker-Warsong combos no longer valid by Warsong commander nerf')
        return errors

    def get_arena_advice(self):
        # todo
        pass

    def get_constructed_advice(self):
        # todo
        pass

    def get_advice(self):
        if self.type == constants.CONSTRUCTED_DECK:
            self.get_constructed_advice()
        else:
            self.get_arena_advice()

    def get_total_synergy_score(self):
        # todo
        pass
