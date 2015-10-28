from deck_extractors.general_extractor import AbstractExtractor
from dataobjects.deck import Deck
from dataobjects.collection import Collection
from data.my_collection import cards
import requests
import json

my_collection = Collection()
my_collection.cards = cards

class TempostormExtractor(AbstractExtractor):
    source_site = 'https://tempostorm.com/'
    output_file = 'tempostorm_decks.json'

    def _process_url(self, url):
        payload = {"klass": False, "page": 1, "perpage": 4, "search": False}
        res = requests.post(url,
                            data=json.dumps(payload),
                            headers={
                                'Accept': 'application/json, text/plain, */*',
                                'Content-Type': 'application/json;charset=utf-8',
                            })
        total_featured_decks = res.json()['total']
        print ('Found %d featured decks' % total_featured_decks)
        payload['perpage'] = total_featured_decks
        res = requests.post(url,
                            data=json.dumps(payload),
                            headers={
                                'Accept': 'application/json, text/plain, */*',
                                'Content-Type': 'application/json;charset=utf-8',
                            })
        sources = []
        decks = res.json()['decks']
        for deck in decks:
            sources.append({
                'slug': deck['slug'],
                'name': deck['name']
            })
        return sources

    def get_decks_list(self):
        sources = []
        featured_decks = self._process_url('https://tempostorm.com/decks/featured')
        sources.extend(featured_decks)
        community_decks = self._process_url('https://tempostorm.com/decks/community')
        sources.extend(community_decks)
        return sources

    def get_deck(self, decks_source):
        print('Processing "%s" deck' % decks_source['name'])
        payload = {"slug": decks_source['slug']}
        res = requests.post('https://tempostorm.com/deck',
                            data=json.dumps(payload),
                            headers={
                                'Accept': 'application/json, text/plain, */*',
                                'Content-Type': 'application/json;charset=utf-8',
                            })
        deck_object = Deck()
        deck = res.json()['deck']
        player_class = deck['playerClass']
        cards = {}
        for card in deck['cards']:
            cards[my_collection.get_closest_name(card['card']['name'])] = card['qty']
        deck_object.cards = cards
        deck_object.player_class = player_class
        deck_object.is_valid()
        return deck_object
