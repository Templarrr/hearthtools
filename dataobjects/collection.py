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

    def get_all_cards_in_game(self):
        # todo
        pass

    def fill_collection_manual(self):
        all_cards = self.get_all_cards_in_game()
        for card in all_cards:
            amount = int(input("(%s):" % card.name))
            if amount > 0 and amount < 3:
                self.cards[card.name] = amount
