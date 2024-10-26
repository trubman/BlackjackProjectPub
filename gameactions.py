import time
from deck import Deck
from my_logging import my_logger
from uniplayer import UniPlayer
from collections import namedtuple

Result = namedtuple('Result', ['player_result', 'is_player_win', 'is_player_blackjack',
                               'dealer_result', 'is_dealer_win', 'is_dealer_blackjack'])

class GameActions:

    def __init__(self):
        self.dealer = UniPlayer(is_dealer=True)
        self.player = UniPlayer()
        self.game_deck = Deck()
        self.mover = self.dealer
        self.result = Result(0, False, False, 0, False, False)
        self.do_first_cards()

    def do_first_cards(self):
        self.player.set_card(self.game_deck.pop_card())
        self.dealer.set_card(self.game_deck.pop_card())
        self.player.set_card(self.game_deck.pop_card())
        my_logger.debug(f"Первый расклад сделан")

    def do_dealer_move(self):
        is_move = True
        card_sum = 0
        for card in self.dealer.get_hand():
            card_sum += card.cost
        if card_sum > 17:
            is_move = False
            self.dealer.set_stand()
        else:
            self.dealer.set_card(self.game_deck.pop_card())
        if self.mover == self.dealer:
            self.mover = self.player
        my_logger.debug(f"Дилер принял решение о ходе: {is_move}, значение суммы его карт = {card_sum}")
        return is_move

    def do_player_move(self, hvatit=False):
        result = True
        if not hvatit:
            if not self.player.get_stand():
                self.player.set_card(self.game_deck.pop_card())
        else:
            self.player.set_stand()
            result = False
        if self.mover == self.player:
            self.mover = self.dealer
        return result

    def check_results(self):
        return_value = True

        def ace_effect(hand):
            res = 0
            ace = []
            cards = []
            for card in hand:
                if card.rank == 'A':
                    ace.append(card)
                else:
                    cards.append(card)
            sum_cost = sum([x.cost for x in cards])
            if len(ace) and sum_cost < 11:
                res = sum_cost + (11 * len(ace))
            elif len(ace) and sum_cost > 11:
                res = sum_cost + (1 * len(ace))
            else:
                res = sum_cost
            return res

        def compare_values(player, dealer):
            nonlocal return_value
            result_list = []
            if player == 21 or dealer == 21:
                if player == 21 and dealer == 21:
                    result_list = Result(player, True, True, dealer, True, True) #[f'{player} (blackjack)', f'{dealer} (blackjack)', 'оба победили', 1, 0]
                elif dealer == 21:
                    result_list = Result(player, False, False, dealer, True, True) #[player, f'{dealer} (blackjack)', 'игрок c треском проиграл', 0, 1]
                elif player == 21:
                    result_list = Result(player, True, True, dealer, False, False) #[f'{player} (blackjack)', dealer, 'игрок победоносен', 2, 0]
                return_value = False
            elif player > 21 and dealer > 21:
                result_list = Result(player, False, False, dealer, False, False) #[player, dealer, 'ничья (оба проиграли)', 0, 0]
                return_value = False
            elif player > 21 or dealer > 21:
                if player < dealer:
                    result_list = Result(player, True, False, dealer, False, False) #[player, dealer, 'игрок победил', 1, 0]
                elif player > dealer:
                    result_list = Result(player, False, False, dealer, True, False) #[player, dealer, 'игрок проиграл', 0, 1]
                return_value = False
            else:
                if player > dealer:
                    result_list = Result(player, True, False, dealer, False, False) #[player, dealer, 'игрок победил', 1, 0]
                elif player < dealer:
                    result_list = Result(player, False, False, dealer, True, False) #[player, dealer, 'игрок проиграл', 0, 1]
                else:
                    result_list = Result(player, False, False, dealer, False, False) #[player, dealer, 'ничья', 0, 0]
            return result_list

        player_res = ace_effect(self.player.get_hand())
        dealer_res = ace_effect(self.dealer.get_hand())

        if not (self.player.get_stand() and self.dealer.get_stand()):
            self.result = compare_values(player_res, dealer_res)
        else:
            self.result = compare_values(player_res, dealer_res)
            return_value = False
        my_logger.debug(f"Суммы карт участников вычислены игрок={player_res}, дилер={dealer_res}. "
                        f"Сырой результат подготовлен: {self.result}")
        return return_value

