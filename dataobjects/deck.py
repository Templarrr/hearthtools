import constants
from dataobjects.constants import legendaries
from collections import OrderedDict


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
            for card_name, card_count in self.cards.iteritems():
                if card_count > 2 or card_count < 1:
                    errors.append('Invalid count of card "%s" : %d' % (card_name, card_count))
                if card_count > 1 and card_name in legendaries:
                    errors.append('You cannot have more then 1 legendary card "%s" in deck' % card_name)
        errors.extend(self.get_nerfed_deck_errors())
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

    def add_card(self, card_name):
        if card_name in self.cards:
            self.cards[card_name] += 1
        else:
            self.cards[card_name] = 1

    def remove_card(self, card_name):
        if card_name not in self.cards:
            raise Exception("No %s card in this deck to remove" % card_name)
        else:
            self.cards[card_name] -= 1
            if self.cards[card_name] == 0:
                del self.cards[card_name]

    def get_deck_synergy_array(self, class_deck_combo):
        synergy_array = {card_name: 0 for card_name in class_deck_combo.keys()}
        for card in self.cards:
            for card2 in class_deck_combo:
                if card2 != 'used_in_decks':
                    synergy_array[card2] += class_deck_combo[card][card2] * self.cards[card]
        return synergy_array

    def refine_deck(self, class_deck_combo, my_col, max_iteration=30):
        """
        iteratively improve deck by removing card from lowest synergy cost and adding card with highest
        as long as it's bigger, not the same card and max iteration limit not reached
        """
        print "===Initiating refining==="
        iteration_counter = 0
        while iteration_counter <= max_iteration:
            # find card to remove
            card_to_remove = ''
            ctr_syn = 30
            for card in self.cards:
                self.remove_card(card)
                synergy_array = self.get_deck_synergy_array(class_deck_combo)
                if synergy_array[card] < ctr_syn:
                    card_to_remove = card
                    ctr_syn = synergy_array[card]
                self.add_card(card)
            # calculating synergy cost
            self.remove_card(card_to_remove)
            synergy_array = self.get_deck_synergy_array(class_deck_combo)
            synergy_array = OrderedDict(sorted(synergy_array.items(), key=lambda t: t[1], reverse=True))
            # find maximal synergy card outside deck
            card_to_add = ''
            cta_syn = 0
            for card in synergy_array:
                if card != 'used_in_decks':
                    if card in my_col and my_col[card] > 0 and (
                                    card not in self.cards or self.cards[card] < my_col[card]):
                        card_to_add = card
                        cta_syn = synergy_array[card]
                        break
            # checking constrains
            print "Card to add: %s : %f" % (card_to_add, cta_syn)
            print "Card to remove: %s : %f" % (card_to_remove, ctr_syn)
            if cta_syn < ctr_syn + 0.01:
                print "Not enough improvements, stop"
                self.add_card(card_to_remove)
                break
            else:
                self.add_card(card_to_add)
                print "===Switch!==="
            iteration_counter += 1
