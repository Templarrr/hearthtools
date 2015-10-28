from api_tools.tools import get_all_cards_data
from difflib import SequenceMatcher as SM


class Collection(object):
    def __init__(self):
        self.cards = {}

    def get_stats_by_types(self):
        # todo
        pass

    def get_most_missing_card(self, filters):
        # todo
        pass

    def fill_collection_auto(self):
        """
        This will be implemented as soon as Blizzard will provide any way to programmatically extract collection data
        """
        # todo
        pass

    def fill_collection_manual(self):
        all_cards = get_all_cards_data()
        for card in all_cards:
            amount = int(input("(%s):" % card.name))
            if amount > 0 and amount < 3:
                self.cards[card.name] = amount

    def fill_collection_empty(self):
        all_cards = get_all_cards_data()
        for card in all_cards:
            self.cards[card.name] = 0

    def get_closest_name(self, name_with_possible_error):
        if name_with_possible_error in self.cards:
            return name_with_possible_error
        else:
            similarity_score = 0
            candidate = 0
            for card in self.cards:
                new_similarity_score = SM(None, card, name_with_possible_error).ratio()
                if new_similarity_score > similarity_score:
                    candidate = card
                    similarity_score = new_similarity_score
            return candidate