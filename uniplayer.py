

class UniPlayer:
    def __init__(self, is_dealer=False):
        self.is_dealer = is_dealer
        self._hand = []
        self._bet = 0
        self._is_stand = False

    def set_bet(self, bet):
        self._bet = int(bet)

    def get_bet(self):
        return self._bet

    def double_bet(self):
        self._bet *= 2

    def add_bet(self, num):
        self._bet += int(num)

    def subt_bet(self, num):
        self._bet -= int(num)

    def set_card(self, card):
        self._hand.append(card)

    def get_hand(self):
        return self._hand

    def set_stand(self):
        self._is_stand = True

    def get_stand(self):
        return self._is_stand