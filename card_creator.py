from data.my_collection import cards as my_col
# from data.nastya_collection import cards as my_col
from dataobjects.collection import Collection
from dataobjects.mask import Mask
from dataobjects.deck import Deck
from dataobjects import constants

my_col_object = Collection()
my_col_object.cards = my_col

# m = Mask()
# m.forbid_all()
# m.allow_rarity('Free')
# m.allow_rarity('Common')
# my_col_object.apply_mask(m)

player_class = raw_input('Input your class: ')
start_card = my_col_object.get_closest_name(raw_input('First card in deck? '))
is_arena_deck = raw_input('Type y if it is arena deck') == 'y'

deck = Deck(my_col=my_col_object.cards)
deck.add_card(start_card)
deck.player_class = player_class
if is_arena_deck:
    deck.type = constants.ARENA_DECK

while sum(deck.cards.values()) < 30:
    next_card, card_syn_value, better_cards = deck.get_advice()
    print 'Adding %s : %f (skipped missing cards: %s)' % (next_card, card_syn_value, str(better_cards))
    deck.add_card(next_card)

if raw_input("Refine? (y/n)") == 'y':
    deck.refine_deck()

print('Final deck:')
for card in deck.cards:
    print "%s : %d" % (card, deck.cards[card])
print('Synergy score: %f' % deck.get_total_synergy_score())
