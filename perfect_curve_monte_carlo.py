import random
from collections import defaultdict

debug = False


def log(log_message):
    if debug:
        print log_message


class CurveMontoCarlo(object):
    curve_init_decks = 1
    games_with_one_curve = 1
    game_length = 12

    def __init__(self):
        pass


class ImitateGame(object):
    def __init__(self, deck, game_length, allow_hp_usage=False):
        self.deck = deck
        self.game_length = game_length
        self.allow_hp_usage = allow_hp_usage
        self.hand = []
        is_going_first = random.randint(0, 1) == 1
        if is_going_first:
            cards_to_draw = 3
            self.has_coin = 0
        else:
            cards_to_draw = 4
            self.has_coin = 1

        for _ in xrange(cards_to_draw):
            self.draw_card()

    def get_all_spend_variants(self):
        result = defaultdict(list)
        for i in range(2 ** len(self.hand)):
            usage_mask = bin(i)[2:]
            usage_mask = '0' * (len(self.hand) - len(usage_mask)) + usage_mask
            used_cards = []
            for i in range(len(usage_mask)):
                if usage_mask[i] == '1':
                    used_cards.append(self.hand[i])
            result[sum(used_cards)].append(used_cards)
        return result

    def draw_card(self):
        drawn_card = self.deck.pop()
        log('Draw: %d' % drawn_card)
        hand_limit = 10
        if self.has_coin + len(self.hand) < hand_limit:
            self.hand.append(drawn_card)
        else:
            log('Card burned')

    def imitate_game(self):
        unspent_mana = 0
        for turn_number in xrange(1, self.game_length + 1):
            unspent_mana += self.imitate_turn(turn_number)
        return unspent_mana

    def imitate_turn(self, turn_number):
        total_mana = min(turn_number, 10)
        self.draw_card()
        log('Turn: %d' % turn_number)
        log('Hand: %s' % self.hand)
        all_variants = self.get_all_spend_variants()
        # Try to spend all mana
        # Check if you have coin and mana + 1 minion
        # Try to spend mana - 1 (with 0.25 spend coin + HP if possible)
        # Spend mana - 2 + HP
        use_hero_power = False
        use_coin = False
        if total_mana in all_variants:
            played_cards = random.choice(all_variants[total_mana])
        elif self.has_coin and total_mana + 1 in all_variants:
            played_cards = random.choice(all_variants[total_mana + 1])
            use_coin = True
        elif self.has_coin and total_mana - 1 in all_variants:
            played_cards = random.choice(all_variants[total_mana - 1])
            if self.allow_hp_usage and random.randint(1, 4) == 1:
                use_coin = True
                use_hero_power = True
        elif total_mana - 2 in all_variants:
            played_cards = random.choice(all_variants[total_mana - 2])
            if self.allow_hp_usage:
                use_hero_power = True
        else:
            max_mana = max([key for key in all_variants.keys() if key < total_mana])
            played_cards = random.choice(all_variants[max_mana])
            if self.allow_hp_usage and total_mana - sum(played_cards) >= 2:
                use_hero_power = True
        spent_mana = sum(played_cards)
        if use_hero_power:
            spent_mana += 2
        if use_coin:
            total_mana += 1
        unspent_mana = total_mana - spent_mana

        cost_k = 1
        if len(played_cards) == 0:
            cost_k = 2
        for card in played_cards:
            self.hand.remove(card)
        if use_coin:
            played_cards.append('(c)')
            self.has_coin = 0
        if use_hero_power:
            played_cards.append('(hp)')
        log('Played: %s' % ','.join(map(str, played_cards)))
        log('Unspent mana: %d' % unspent_mana)

        return unspent_mana * cost_k


class ManaCurve(object):
    def __init__(self, deck_size=30, max_per_mana=10):
        self.deck_size = deck_size
        self.max_per_mana = max_per_mana
        self.mana_curve = [0] * 11
        self._fill_initial_curve()

    def _fill_initial_curve(self):
        # self.mana_curve[0] = 5
        self.mana_curve[1] = 10
        self.mana_curve[2] = 10
        self.mana_curve[3] = 10

    def push_mana_curve(self):
        deck = self.get_deck()
        bucket1 = random.choice(deck)
        while bucket1 == 10:
            bucket1 = random.choice(deck)
        self.mana_curve[bucket1] -= 1
        self.mana_curve[bucket1 + 1] += 1

    def is_unusable(self):
        return sum(self.mana_curve[:5]) == 0 or sum(self.mana_curve[-3:]) >= 10

    def get_deck(self):
        deck = []
        for mana in xrange(0, 11):
            deck += [mana] * self.mana_curve[mana]
        random.shuffle(deck)
        return deck

    def __str__(self):
        return ':'.join(map(str, self.mana_curve))
