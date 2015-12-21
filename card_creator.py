import json
from collections import OrderedDict
from data.my_collection import cards as my_col
# from data.nastya_collection import cards as my_col
from dataobjects.constants import legendaries
from dataobjects.collection import Collection
from dataobjects.deck import Deck

my_col_object = Collection()
my_col_object.cards = my_col

player_class = raw_input('Input your class: ')
input_file = 'data/' + player_class + '.json'
popular_file = 'data/cards_popularity_per_class.json'

with open(input_file, 'r') as f:
    class_deck_combo = json.load(f)
with open(popular_file, 'r') as f:
    popular_cards = json.load(f)

start_card = my_col_object.get_closest_name(raw_input('First card in deck? '))

deck = {start_card: 1}
probability = class_deck_combo[start_card].copy()

# constrcted
show_top = 20
auto = True
while sum(deck.values()) < 30:
    probability = OrderedDict(sorted(probability.items(), key=lambda t: t[1], reverse=True))
    index = 0
    more_suitable_not_in_collection = []
    for card in probability:
        if card != 'used_in_decks':
            if card in my_col and my_col[card] > 0 and (card not in deck or deck[card] < my_col[card]):
                print("%s : %f, skipped: %s" % (card, probability[card], str(more_suitable_not_in_collection)))
                index += 1
                if auto:
                    next_card = card
                    break
            elif my_col[card] == 0 or (card not in legendaries and my_col[card] == 1):
                more_suitable_not_in_collection.append(card)

    if not auto:
        next_card = raw_input('Next card in deck? (%d left)' % (30 - sum(deck.values())))

    if next_card in deck:
        deck[next_card] += 1
    else:
        deck[next_card] = 1

    for some_card in probability:
        probability[some_card] += class_deck_combo[next_card][some_card]

# arena
# while sum(deck.values()) < 30:
#     probability = OrderedDict(sorted(probability.items(), key=lambda t: t[1], reverse=True))
#     index= 0
#     # for card in probability:
#     #     if index>=show_top:
#     #         break
#     #     if card!='used_in_decks' and (card not in deck or deck[card]<10):
#     #         print("%s : %f" % (card, probability[card]))
#     #         index += 1
#     card1 = raw_input('Card1: ')
#     print ('Value: %f' % probability[card1])
#     card2 = raw_input('Card2: ')
#     print ('Value: %f' % probability[card2])
#     card3 = raw_input('Card3: ')
#     print ('Value: %f' % probability[card3])
#     next_card = raw_input('Next card in deck? (%d left)' % (30 - sum(deck.values())))
#
#     if next_card in deck:
#         deck[next_card] += 1
#     else:
#         deck[next_card] = 1
#
#     for some_card in probability:
#         probability[some_card] += class_deck_combo[next_card][some_card]

deck_object = Deck()
deck_object.cards = deck
if raw_input("Refine? (y/n)") == 'y':
    deck_object.refine_deck(class_deck_combo, my_col)

print('Final deck:')
for card in deck_object.cards:
    print "%s : %d" % (card, deck[card])
