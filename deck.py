import random


class Card:
    def __init__(self, rank, suit, cost):
        self.rank = rank
        self.suit = suit
        self.cost = cost

    def __str__(self):
        return f"{self.rank}-{self.suit[1]}"


class Deck:
    def __init__(self):
        self.layout_list = []
        self.order_list = []
        self.rank_list = [
            ('2', 2),
            ('3', 3),
            ('4', 4),
            ('5', 5),
            ('6', 6),
            ('7', 7),
            ('8', 8),
            ('9', 9),
            ('10', 10),
            ('J', 10),
            ('Q', 10),
            ('K', 10),
            ('A', 11),
        ]
        self.suit_list = [
            ['clabs', 'трефы'],
            ['diamonds', 'бубны'],
            ['hearts', 'червы'],
            ['spades', 'пики'],
        ]
        self._gen_order_list()
        self._gen_layout_list()

    def _gen_order_list(self):
        for suit_name in self.suit_list:
            for rank_name in self.rank_list:
                self.order_list.append((rank_name[0], suit_name, rank_name[1]))

    def _gen_layout_list(self):
        for item in range(len(self.order_list)):
            r = random.randint(0, len(self.order_list) - 1)
            card = self.order_list.pop(r)
            C = Card(card[0], card[1], card[2])
            self.layout_list.append(C)

    def pop_card(self):
        if len(self.layout_list) > 0:
            return self.layout_list.pop(len(self.layout_list) - 1)
        else:
            NoCard = Card("0", ['no card', 'нет карты'], 0)
            return NoCard