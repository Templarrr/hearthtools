import json


class AbstractExtractor(object):
    source_site = 'www.some_deck_source.com'
    output_file = 'decks.json'

    def get_decks_list(self):
        raise NotImplementedError

    def get_deck(self, decks_source):
        raise NotImplementedError

    def save_decks_results(self, results):
        with open(self.output_file, 'w') as f:
            json.dump(results, f)

    def run(self):
        result = {}
        decks_sources = self.get_decks_list()
        for decks_source in decks_sources:
            deck = self.get_deck(decks_source)
            if not deck.is_valid():
                print 'Errors: %s' % str(deck.get_errors())
                continue
            if deck.player_class not in result:
                result[deck.player_class] = []
            result[deck.player_class].append(deck.cards)
        self.save_decks_results(result)