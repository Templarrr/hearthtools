from api_tools.tools import get_all_legendaries, get_cards_for_all_classes, get_all_cards_names

card_types = ['Hero', 'Enchantment', 'Hero Power', 'Weapon', 'Spell', 'Minion']
card_types_in_collection = ['Weapon', 'Spell', 'Minion']
card_sets = ['Hero Skins', 'Missions', 'Classic', 'Naxxramas', 'Tavern Brawl', 'System', 'Credits',
             'Blackrock Mountain', 'Basic', 'Debug', 'Promotion', 'Reward', 'The Grand Tournament', 'Goblins vs Gnomes',
             'The League of Explorers']
card_sets_available_in_store = ['Classic', 'Goblins vs Gnomes', 'The Grand Tournament']
card_rarities = ['Legendary', 'Epic', 'Rare', 'Common', 'Free']
probabilities_in_booster = {'Legendary': 0.01, 'Epic': 0.04, 'Rare': 0.2, 'Common': 0.75}
dust_cost_to_craft = {'Legendary': 1600, 'Epic': 400, 'Rare': 100, 'Common': 40}
dust_cost_to_sell = {'Legendary': 400, 'Epic': 100, 'Rare': 20, 'Common': 5}
card_factions = ['Neutral', 'Alliance', 'Horde']
card_races = ['Mech', 'Murloc', 'Demon', 'Totem', 'Dragon', 'Beast', 'Pirate']
player_classes = ['Warrior', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Hunter', 'Druid', 'Mage', 'Shaman']
CONSTRUCTED_DECK = 'constructed'
ARENA_DECK = 'arena'
legendaries = get_all_legendaries()
class_cards = get_cards_for_all_classes()
all_cards = get_all_cards_names()
