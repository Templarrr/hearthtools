from data.my_collection import cards
# from data.nastya_collection import cards
from api_tools.tools import get_card_set_stats
from dataobjects.constants import card_sets_available_in_store, card_rarities, probabilities_in_booster, dust_cost_to_craft, dust_cost_to_sell

stats = get_card_set_stats(cards)
for card_set in card_sets_available_in_store:
    print '**** %s ****' % card_set
    amortized_booster_dust_cost = 0.0
    amortized_booster_dust_for_sell = 0.0
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
            amortized_booster_dust_for_sell += 5 * dust_cost_to_sell[rarity] * probabilities_in_booster[rarity] * (stats[card_set][rarity][2]) / (
                stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])
        else:
            # we don't need 2nd copy of legendaries, as we only can use 1
            amortized_booster_dust_cost += 5 * dust_cost_to_craft[rarity] * probabilities_in_booster[rarity] * (stats[card_set][rarity][0]) / (
                stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])
            amortized_booster_dust_for_sell += 5 * dust_cost_to_sell[rarity] * probabilities_in_booster[rarity] * (stats[card_set][rarity][2] + stats[card_set][rarity][1]) / (
                stats[card_set][rarity][0] + stats[card_set][rarity][1] + stats[card_set][rarity][2])
        print "0 copies of cards: %s" % str(stats[card_set][rarity][3])
        print "1 copy of cards: %s" % str(stats[card_set][rarity][4])
    print 'Amortized dust cost of new cards and second copies in booster %f' % amortized_booster_dust_cost
    print 'Amortized dust retrieved from selling copies in booster %f' % amortized_booster_dust_for_sell
    print 'Total booster value %f' % (amortized_booster_dust_cost + amortized_booster_dust_for_sell)