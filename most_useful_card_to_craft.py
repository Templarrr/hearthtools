from dataobjects.constants import player_classes
from dataobjects.collection import Collection
from data.my_collection import cards as my_col
from collections import OrderedDict
import json

empty_col = Collection()
empty_col.fill_collection_empty()


for player_class in player_classes:
    classfile = 'data/' + player_class + '.json'
    with open(classfile, 'r') as f:
        class_deck_combo = json.load(f)
    probability = empty_col.cards.copy()
    for card1 in my_col:
        if my_col[card1] == 0:
            continue
        # !!! why use incorrect name??? :(
        if card1 == "Ship's Cannon":
            card1_ = "Ship Cannon"
        elif card1 == 'Hemet Nesingwary':
            card1_ = 'Hemit Nesingwary'
        elif card1 == 'Bouncing Blade':
            card1_ = 'Bouncing Blades'
        elif card1 == 'Steamwheedle Sniper':
            card1_ = 'Staemwheedle Sniper'
        elif card1 == "Ancestor's Call":
            card1_ = 'Ancestors Call'
        else:
            card1_ = card1

        if card1_ in class_deck_combo:
            for card2 in class_deck_combo[card1_]:
                if card2 == 'used_in_decks':
                    continue
                if card2 == "Ship Cannon":
                    card2_ = "Ship's Cannon"
                elif card2 == 'Hemit Nesingwary':
                    card2_ = 'Hemet Nesingwary'
                elif card2 == 'Bouncing Blades':
                    card2_ = 'Bouncing Blade'
                elif card2 == 'Staemwheedle Sniper':
                    card2_ = 'Steamwheedle Sniper'
                elif card2 == "Ancestors Call":
                    card2_ = "Ancestor's Call"
                else:
                    card2_ = card2
                probability[card2_] += class_deck_combo[card1_][card2] * my_col[card1]
    probability = OrderedDict(sorted(probability.items(), key=lambda t: t[1], reverse=True))
    to_break = False
    for card in probability:
        if my_col[card]<2 and card != 'Dr. Boom' and card != 'Grommash Hellscream' and card != 'Loatheb':
            print "Best card for class %s to craft is : %s (%f)" % (player_class, card, probability[card])
            if to_break:
                break
            to_break = True
