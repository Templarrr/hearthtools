from data.my_collection import cards
from api_tools.tools import get_card_set_stats
from dataobjects.constants import card_sets_available_in_store, card_rarities, probabilities_in_booster, dust_cost_to_craft

stats = get_card_set_stats(cards)
for card_set in card_sets_available_in_store:
    print '**** %s ****' % card_set
    amortized_booster_dust_cost = 0
    for rarity in card_rarities:
        if rarity == 'Free':
            continue
        print "%s : %d out of %d collected, %d - 1 copy, %d - 2 copies. In booster %f chance to get new, %f to get second copy" % (
            rarity,
            stats[card_set][rarity][1] + stats[card_set][rarity][2],
            stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2],
            stats[card_set][rarity][1],
            stats[card_set][rarity][2],
            1 - (1 - probabilities_in_booster[rarity] * stats[card_set][rarity][0] / (
            stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])) ** 5,
            1 - (1 - probabilities_in_booster[rarity] * stats[card_set][rarity][1] / (
            stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])) ** 5
        )
        if rarity != 'Legendary':
            amortized_booster_dust_cost += 5 * dust_cost_to_craft[rarity] * probabilities_in_booster[rarity] * (stats[card_set][rarity][0] + stats[card_set][rarity][1]) / (
                stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])
        else:
            # we don't need 2nd copy of legendaries, as we only can use 1
            amortized_booster_dust_cost += 5 * dust_cost_to_craft[rarity] * probabilities_in_booster[rarity] * (stats[card_set][rarity][0]) / (
                stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])
    print 'Amortized dust cost of new cards and second copies in booster %f' % amortized_booster_dust_cost