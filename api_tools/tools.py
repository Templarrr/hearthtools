import config
import requests
from dataobjects.card import Card
import os
import json


def get_all_cards_data():
    cached_flie = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'all_cards.json'))
    if os.path.exists(cached_flie):
        with open(cached_flie) as f:
            return [Card(card_info) for card_info in json.load(f)]
    cards_final_info = []
    cards_raw_info = requests.get(config.MASHAPE_API_URL + 'cards?collectible=1',
                                  headers={'X-Mashape-Key': config.MASHAPE_API_KEY}).json()
    for card_set in cards_raw_info:
        for raw_card in cards_raw_info[card_set]:
            card = Card(raw_card)
            if card.type in ['Spell', 'Minion', 'Weapon']:
                cards_final_info.append(card)
    with open(cached_flie, 'w+') as f:
        json.dump([card.__dict__ for card in cards_final_info], f)
    return cards_final_info


def get_all_card_fields():
    card_fields = set()
    cards_raw_info = requests.get(config.MASHAPE_API_URL + 'cards',
                                  headers={'X-Mashape-Key': config.MASHAPE_API_KEY}).json()
    for card_set in cards_raw_info:
        for card in cards_raw_info[card_set]:
            for card_field in card:
                card_fields.add(card_field)
    return card_fields


def get_all_unique_values_for_card_field(card_field):
    values = set()
    cards_raw_info = requests.get(config.MASHAPE_API_URL + 'cards',
                                  headers={'X-Mashape-Key': config.MASHAPE_API_KEY}).json()
    for card_set in cards_raw_info:
        for card in cards_raw_info[card_set]:
            if card_field in card:
                values.add(card[card_field])
    return values


def get_all_elite_Cards():
    cards = []
    cards_raw_info = requests.get(config.MASHAPE_API_URL + 'cards',
                                  headers={'X-Mashape-Key': config.MASHAPE_API_KEY}).json()
    for card_set in cards_raw_info:
        for card in cards_raw_info[card_set]:
            if 'elite' in card and card['elite']:
                cards.append(card)
    return cards


def get_card_set_stats(collection_cards):
    all_cards = get_all_cards_data()
    stats = {}
    for card in all_cards:
        if card.cardSet not in stats:
            stats[card.cardSet] = {
                'Legendary': [0, 0, 0, [], []],
                'Epic': [0, 0, 0, [], []],
                'Rare': [0, 0, 0, [], []],
                'Common': [0, 0, 0, [], []],
                'Free': [0, 0, 0, [], []]}
        stats[card.cardSet][card.rarity][collection_cards[card.name]] += 1
        if collection_cards[card.name] != 2:
            stats[card.cardSet][card.rarity][collection_cards[card.name] + 3].append(card.name)
    return stats


def get_all_legendaries():
    cards = get_all_cards_data()
    legendaries = []
    for card in cards:
        if card.rarity == 'Legendary':
            legendaries.append(str(card.name))
    return legendaries


def get_class_cards(player_class):
    cards = get_all_cards_data()
    class_cards = []
    for card in cards:
        if card.playerClass == player_class:
            class_cards.append(card.name)
    return class_cards


def get_cards_for_all_classes():
    player_classes = ['Warrior', 'Rogue', 'Priest', 'Warlock', 'Paladin', 'Hunter', 'Druid', 'Mage', 'Shaman',
                      'Neutral']
    cards = get_all_cards_data()
    cards_per_class = {player_class: [] for player_class in player_classes}
    for card in cards:
        cards_per_class[card.playerClass].append(card.name)
    return cards_per_class


def get_all_cards_names():
    cards = get_all_cards_data()
    return [card.name for card in cards]
