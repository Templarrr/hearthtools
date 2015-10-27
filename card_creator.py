import json
from collections import OrderedDict
from data.my_collection import cards as my_col

player_class = raw_input('Input your class: ')
input_file = 'data/' + player_class + '.json'
popular_file = 'data/cards_popularity_per_class.json'

with open(input_file, 'r') as f:
    class_deck_combo = json.load(f)
with open(popular_file, 'r') as f:
    popular_cards = json.load(f)

start_card = raw_input('First card in deck? ')

deck = {start_card:1}
probability = class_deck_combo[start_card].copy()

# constrcted
show_top = 20
auto = True
while sum(deck.values()) < 30:
    probability = OrderedDict(sorted(probability.items(), key=lambda t: t[1], reverse=True))
    index= 0
    for card in probability:
        if index>=show_top:
            break
        if card!='used_in_decks' and card in my_col and my_col[card]>0 and (card not in deck or deck[card]<my_col[card]):
            print("%s : %f" % (card, probability[card]))
            index += 1
            if auto:
                next_card = card
                break
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

print('Final deck:')
print(json.dumps(deck))