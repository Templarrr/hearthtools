import json

import constants
from dataobjects.constants import legendaries, class_cards
from dataobjects.collection import Collection
from collections import OrderedDict


class Deck(object):
    """
    Class for storing information about Hearthstone deck
    """
    _class_deck_combo = None

    def __init__(self, my_col=None):
        self.player_class = ''
        self.name = 'Noname deck'
        self.type = constants.CONSTRUCTED_DECK
        self.cards = {}
        if my_col:
            self.my_col = my_col
        else:
            self.my_col = {}

    @property
    def class_deck_combo(self):
        if not self._class_deck_combo:
            input_file = 'data/' + self.player_class + '.json'
            with open(input_file, 'r') as f:
                self._class_deck_combo = json.load(f)
        return self._class_deck_combo

    def is_valid(self):
        """
        is this Deck valid to use in Hearthstone?
        :return: bool
        """
        return len(self.get_errors()) == 0

    def get_errors(self):
        """
        Get list of errors in deck
        :return: list of str
        """
        errors = []
        allowed_cards = class_cards['Neutral'][:]
        allowed_cards.extend(class_cards[self.player_class])
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
                if card_name not in allowed_cards:
                    errors.append('Card "%s" is not allowed - you can use only neutral or class cards' % card_name)
        errors.extend(self.get_nerfed_deck_errors())
        errors.extend(self.get_jokers_errors())
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

    def get_jokers_errors(self):
        """
        Filter out "joke" decks
        :return:
        """
        errors = []
        weapon_synergy_cards = [
            'Bloodsail Corsair',
            'Southsea Deckhand',
            'Orgrimmar Aspirant',
            'Goblin Auto-Barber',
            'Spiteful Smith',
            'Buccaneer',
            'Captain Greenskin',
            'Dread Corsair'
        ]
        for weapon_synergy_card in weapon_synergy_cards:
            if self.player_class in ['Mage', 'Warlock', 'Priest', 'Druid'] and weapon_synergy_card in self.cards:
                errors.append('Haha, %s in class without weapons, very funny' % weapon_synergy_card)
        return errors

    def get_arena_advice(self):
        real_col = self.my_col
        my_col_object = Collection()
        my_col_object.cards = real_col
        temp_col = {}
        for i in range(1, 4):
            card_option = my_col_object.get_closest_name(raw_input('Card to choose #%d: ' % i))
            temp_col[card_option] = 30
        self.my_col = temp_col
        card_to_add, card_syn_value, _ = self.get_constructed_advice()
        self.my_col = real_col
        return card_to_add, card_syn_value, []

    def get_constructed_advice(self):
        synergy_array = self.get_deck_synergy_array()
        synergy_array = OrderedDict(sorted(synergy_array.items(), key=lambda t: t[1], reverse=True))
        # find maximal synergy card outside deck
        card_to_add = ''
        card_syn_value = 0
        better_cards = []
        for card in synergy_array:
            if card != 'used_in_decks':
                if card in self.my_col and self.my_col[card] > 0 and (
                                card not in self.cards or self.cards[card] < self.my_col[card]):
                    card_to_add = card
                    card_syn_value = synergy_array[card_to_add]
                    break
                elif (card in legendaries and self.my_col[card] == 0) or (
                        card not in legendaries and self.my_col[card] == 1):
                    better_cards.append(card)
        return card_to_add, card_syn_value, better_cards

    def get_worst_card(self):
        card_to_remove = ''
        ctr_syn = 30
        for card in self.cards:
            self.remove_card(card)
            synergy_array = self.get_deck_synergy_array()
            if synergy_array[card] < ctr_syn:
                card_to_remove = card
                ctr_syn = synergy_array[card]
            self.add_card(card)
        return card_to_remove, ctr_syn

    def get_advice(self):
        if self.type == constants.CONSTRUCTED_DECK:
            return self.get_constructed_advice()
        else:
            return self.get_arena_advice()

    def get_total_synergy_score(self):
        synergy_array = self.get_deck_synergy_array()
        total_synergy_cost = 0
        for card in self.cards:
            if card in synergy_array:
                total_synergy_cost += self.cards[card] * synergy_array[card]
        return total_synergy_cost

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

    def get_deck_synergy_array(self):
        synergy_array = {card_name: 0 for card_name in self.class_deck_combo.keys()}
        for card in self.cards:
            for card2 in self.class_deck_combo:
                if card2 != 'used_in_decks' and card in self.class_deck_combo[card2]:
                    synergy_array[card2] += self.class_deck_combo[card2][card] * self.cards[card]
        return synergy_array

    def refine_deck(self, max_iteration=30):
        """
        iteratively improve deck by removing card from lowest synergy cost and adding card with highest
        as long as it's bigger, not the same card and max iteration limit not reached
        """
        print "===Initiating refining==="
        iteration_counter = 0
        while iteration_counter <= max_iteration:
            # find card to remove
            card_to_remove, ctr_syn = self.get_worst_card()
            # calculating synergy cost
            self.remove_card(card_to_remove)
            card_to_add, cta_syn = self.get_constructed_advice()
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
