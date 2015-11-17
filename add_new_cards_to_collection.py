from data.my_collection import cards as my_collection_cards
from api_tools.tools import get_all_cards_names
from collections import OrderedDict
import json

all_cards = get_all_cards_names()
for card in all_cards:
    if card not in my_collection_cards:
        my_collection_cards[card] = 0

my_collection_cards = OrderedDict(sorted(my_collection_cards.items(), key=lambda t: t[0], reverse=False))
print "{"
for card in my_collection_cards:
    print '    "%s": %d,' % (card, my_collection_cards[card])
print "}"
# print(json.dumps(my_collection_cards))