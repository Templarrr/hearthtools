import json


class AbstractExtractor(object):
    source_site = 'www.some_deck_source.com'
    output_file = 'decks.json'

    def get_decks_list(self):
        raise NotImplementedError

    def get_deck_cards_and_class(self, decks_source):
        raise NotImplementedError

    def save_decks_results(self, results):
        with open(self.output_file, 'w') as f:
            json.dump(results, f)

    def run(self):
        result = {}
        decks_sources = self.get_decks_list()
        for decks_source in decks_sources:
            cards, player_class = self.get_deck_cards_and_class(decks_source)
            if player_class not in result:
                result[player_class] = []
            result[player_class].append(cards)
        self.save_decks_results(result)