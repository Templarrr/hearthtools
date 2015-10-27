import config
import requests
from dataobjects.card import Card
import json


def get_all_cards_data():
    cards_final_info = []
    cards_raw_info = requests.get(config.MASHAPE_API_URL + 'cards?collectible=1',
                                  headers={'X-Mashape-Key': config.MASHAPE_API_KEY}).json()
    for card_set in cards_raw_info:
        for raw_card in cards_raw_info[card_set]:
            card = Card()
            card.fill_from_dict(raw_card)
            if card.type in ['Spell', 'Minion', 'Weapon']:
                cards_final_info.append(card)
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
            stats[card.cardSet] = {'Legendary': [0, 0, 0], 'Epic': [0, 0, 0], 'Rare': [0, 0, 0], 'Common': [0, 0, 0],
                                   'Free': [0, 0, 0]}
        stats[card.cardSet][card.rarity][collection_cards[card.name]] += 1
    return stats


def get_all_legendaries():
    cards = get_all_cards_data()
    legendaries = []
    for card in cards:
        if card.rarity == 'Legendary':
            legendaries.append(str(card.name))
    return legendaries
