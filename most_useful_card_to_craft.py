from dataobjects.constants import player_classes, legendaries
from dataobjects.collection import Collection
from data.my_collection import cards as my_col
# from data.nastya_collection import cards as my_col
from collections import OrderedDict, Counter
import json

empty_col = Collection()
empty_col.fill_collection_empty()

total_rate = Counter()

for player_class in player_classes:
    classfile = 'data/' + player_class + '.json'
    with open(classfile, 'r') as f:
        class_deck_combo = json.load(f)
    probability = empty_col.cards.copy()
    for card1 in my_col:
        if my_col[card1] == 0:
            continue

        if card1 in class_deck_combo:
            for card2 in class_deck_combo[card1]:
                if card2 == 'used_in_decks':
                    continue
                probability[card2] += class_deck_combo[card1][card2] * my_col[card1]
    probability = OrderedDict(sorted(probability.items(), key=lambda t: t[1], reverse=True))

    show_limit = 10
    cards_to_show = []
    for card in probability:
        if (my_col[card] < 2 and card not in legendaries) or (my_col[card] < 1 and card in legendaries):
            cards_to_show.append('%s: %s' % (card, str(probability[card])))
            total_rate[card] += probability[card]
            if len(cards_to_show) >= show_limit:
                break
    print "Best cards for class %s to craft is : %s" % (player_class, str(cards_to_show))

print "Total craft rating: %s" % total_rate.most_common()
