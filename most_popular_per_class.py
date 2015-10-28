import json
from collections import OrderedDict

input_decks_file = 'tempostorm_decks.json'
with open(input_decks_file, 'r') as f:
    decks = json.load(f)

output_file = 'cards_popularity_per_class.json'
result = {'Total':{}}
for player_class in decks:
    result[player_class] = {}
    for deck in decks[player_class]:
        for card in deck:
            if card not in result[player_class]:
                result[player_class][card] = deck[card]
            else:
                result[player_class][card] += deck[card]
            if card not in result['Total']:
                result['Total'][card] = deck[card]
            else:
                result['Total'][card] += deck[card]
for player_class in result:
    result[player_class] = OrderedDict(sorted(result[player_class].items(), key=lambda t: t[1], reverse=True))
with open(output_file, 'w') as f:
    json.dump(result, f)

usability_matrix = {}
for player_class in result:
    if player_class=='Total':
        continue
    usability_matrix[player_class] = {}
    all_cards_used_by_class = result[player_class].keys()
    for card1 in all_cards_used_by_class:
        usability_matrix[player_class][card1] = {'used_in_decks': 0}
        for card2 in all_cards_used_by_class:
            usability_matrix[player_class][card1][card2] = 0

for player_class in decks:
    for deck in decks[player_class]:
        for card1 in deck:
            usability_matrix[player_class][card1]['used_in_decks'] += 1
            for card2 in deck:
                if card1 == card2 and deck[card1] < 2:
                    continue
                else:
                    usability_matrix[player_class][card1][card2] += 1

for player_class in usability_matrix:
    for card1 in usability_matrix[player_class]:
        for card2 in usability_matrix[player_class][card1]:
            if card2 != 'used_in_decks':
                usability_matrix[player_class][card1][card2] /= float(usability_matrix[player_class][card1]['used_in_decks'])

for player_class in usability_matrix:
    with open(player_class+'.json', 'w') as f:
        json.dump(usability_matrix[player_class], f)