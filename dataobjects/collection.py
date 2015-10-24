from api_tools.tools import get_all_cards_data


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
