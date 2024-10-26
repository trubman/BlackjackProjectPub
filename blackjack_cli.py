import random, time


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
            print("В колоде нет карт!")
            NoCard = Card("0", ['no card', 'нет карты'], 0)
            return NoCard


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


class GameActions:
    def __init__(self):
        self.dealer = UniPlayer(is_dealer=True)
        self.player = UniPlayer()
        self.game_deck = Deck()
        self.iteration = 1
        self.mover = self.dealer
        self.result = [0, 0, 0, 'add', 'subt']

    def start_game(self):
        print('*** Начнем игру BLACKJACK ***')
        players_bet_r = input('СТАВКА ИГРОКА: ').strip()
        def input_data(players_bet_r):
            try:
                players_bet = int(players_bet_r)
                if players_bet > 0:
                    self.player.set_bet(players_bet)
                    print(f'СТАВКА {players_bet} фишек ПРИНЯТА!')
                else:
                    raise ValueError
            except ValueError:
                print('Ошибка. НЕКОРРЕКТНЫЙ ВВОД:\n',
                    '___ставка игрока может быть только целым положительным числом', sep='')
                input_data(input('ПОПРОБУЙ СНОВА: ').strip())
        input_data(players_bet_r)

    def view_iteration(self):
        print(f'___ставка игрока: {self.player.get_bet()} фишек')
        players_hand_str = ', '.join([x.__str__() for x in self.player.get_hand()])
        print(f'___на руках у игрока: ({players_hand_str})')
        dealers_hand_str = ', '.join([x.__str__() for x in self.dealer.get_hand()])
        print(f'___на руках у дилера: ({dealers_hand_str})')

    def get_player_move(self):
        player_move_r = input("ИГРОК ДЕЛАЕТ ХОД: ").strip().lower()
        def input_data(player_move_r):
            moves = ["еще", "hit", "хватит", "stand", "удвоить", "double down"]
            try:
                if player_move_r in moves:
                    return player_move_r
                else:
                    raise ValueError
            except ValueError:
                print('Ошибка. НЕКОРРЕКТНЫЙ ВВОД:\n',
                      '___ход может быть только "Еще"("Hit"), "Хватит"("Stand") или "Удвоить"("Double down")', sep='')
                input_data(input('ПОПРОБУЙ СНОВА. ИГРОК ДЕЛАЕТ ХОД: ').strip().lower())
        return input_data(player_move_r)

    def do_move(self):
        if self.mover == self.player:
            move = self.get_player_move()
            if move == "хватит" or move == "stand":
                self.player.set_stand()
            elif move == "удвоить" or move == "double down":
                self.player.double_bet()
                print('___игрок удволи ставку!!!')
            self.do_iteration()
        elif self.mover == self.dealer:
            move = ''
            card_sum = 0
            for card in self.dealer.get_hand():
                card_sum += card.cost
            if card_sum > 17:
                move = 'Хватит'
                self.dealer.set_stand()
            else:
                move = 'Еще'
            print(f'ДИЛЕР ДЕЛАЕТ ХОД: {move}')
            self.do_iteration()

    def execution(self):
        if self.result[4] == 1:
            self.player.subt_bet(self.player.get_bet())
            self.dealer.add_bet(self.player.get_bet())
        elif self.result[3] == 1:
            self.dealer.subt_bet(self.player.get_bet())
            self.player.add_bet(self.player.get_bet())
        elif self.result[3] == 2:
            self.dealer.subt_bet(self.player.get_bet())
            self.player.add_bet(self.player.get_bet() * 2)
        else:
            pass

    def end_game(self):
        print('*** Игра окончена ***')
        # print(self.result)
        print('РЕЗУЛЬТАТ:\n',
              f'___игрок: {self.result[0]}\n',
              f'___дилер: {self.result[1]}\n',
              f'___{self.result[2]}\n',
              sep='')
        self.execution()
        self.iteration = 1
        self.result = [0, 0, 0, 'add', 'subt']

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
            if player > 21 and dealer > 21:
                result_list = [player, dealer, 'ничья (оба проиграли)', 0, 0]
                return_value = False
            elif player > 21 or dealer > 21:
                if player < dealer:
                    result_list = [player, dealer, 'игрок победил', 1, 0]
                elif player > dealer:
                    result_list = [player, dealer, 'игрок проиграл', 0, 1]
                return_value = False
            elif player == 21 or dealer == 21:
                if player == 21 and dealer == 21:
                    result_list = [f'{player} (blackjack)', f'{dealer} (blackjack)', 'оба победили', 1, 0]
                elif dealer == 21:
                    result_list = [player, f'{dealer} (blackjack)', 'игрок c треском проиграл', 0, 1]
                elif player == 21:
                    result_list = [f'{player} (blackjack)', dealer, 'игрок победоносен', 2, 0]
                return_value = False
            else:
                if player > dealer:
                    result_list = [player, dealer, 'игрок победил', 1, 0]
                elif player < dealer:
                    result_list = [player, dealer, 'игрок проиграл', 0, 1]
                else:
                    result_list = [player, dealer, 'ничья', 0, 0]
            return result_list

        player_res = ace_effect(self.player.get_hand())
        dealer_res = ace_effect(self.dealer.get_hand())

        if not (self.player.get_stand() and self.dealer.get_stand()):
            self.result = compare_values(player_res, dealer_res)
        else:
            self.result = compare_values(player_res, dealer_res)
            return_value = False

        return return_value

    def do_iteration(self):
        time.sleep(2)
        if self.iteration != 1:
            self.iteration += 1
            if self.mover == self.player:
                if not self.player.get_stand():
                    self.player.set_card(self.game_deck.pop_card())
                self.view_iteration()
                if self.check_results():
                    self.mover = self.dealer
                    self.do_move()
            elif self.mover == self.dealer:
                if not self.dealer.get_stand():
                    self.dealer.set_card(self.game_deck.pop_card())
                self.view_iteration()
                if self.check_results():
                    self.mover = self.player
                    self.do_move()
        else:
            self.player.set_card(self.game_deck.pop_card())
            self.dealer.set_card(self.game_deck.pop_card())
            self.player.set_card(self.game_deck.pop_card())
            self.iteration += 1
            self.view_iteration()
            if self.check_results():
                self.do_move()

    def do_game(self):
        self.start_game()
        self.do_iteration()
        self.end_game()


GAME = GameActions()
GAME.do_game()

