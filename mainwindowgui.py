import os
import sys
import time
from PyQt6 import QtTest
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QImage, QPalette, QColor
from PyQt6.QtWidgets import (
  QMainWindow,
  QPushButton,
  QLabel,
  QWidget,
  QVBoxLayout,
  QInputDialog,
  QStackedLayout,
  QHBoxLayout,
  QPlainTextEdit,
  QGridLayout,
  QLineEdit,
  QMessageBox,
)
from gameactions import GameActions
from my_logging import my_logger

basedir = os.path.dirname(__file__)

# def resource_path(relative_path):
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # сырые значения
        self.player_name = 'игрок'
        self.player_summ = 0
        self.player_stavka = 0
        self.layout_num = 0
        self.game = ''
        self.player_hand = []
        self.dealer_hand = []
        self.endgame = False
        self.btn_enable = False

        # виджеты и их постоянные свойства
        ## свойства самого окна
        self.setWindowTitle("Synergy Blackjack")
        self.setFixedSize(QSize(1052, 869))
        ## первый слой окна
        ### верхняя и нижние картинки первого окна
        self.start_img_widget = QLabel("")
        img = QImage(os.path.join(basedir, "media/start.jpg")).scaled(1032, 600)
        # img = QImage(resource_path("media/start.jpg")).scaled(1032, 600)
        self.start_img_widget.setPixmap(QPixmap.fromImage(img))
        self.start_btm_img_widget = QLabel("")
        img = QImage(os.path.join(basedir, "media/btm.png")).scaled(1032, 100)
        self.start_btm_img_widget.setPixmap(QPixmap.fromImage(img))
        ### данные игрока в первом окне
        self.player_name_lable = QLabel("Кто ты, лудоман?")
        self.player_name_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_summ_lable = QLabel('Тю-тю')
        self.player_summ_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ### кнопки первого окна
        self.button_play = QPushButton("Сыграть!")
        self.button_play.setFixedSize(QSize(1032, 50))
        self.button_play.clicked.connect(self.start_game)
        self.button_play.setDefault(True)
        self.button_end = QPushButton("Забрать сумму...")
        self.button_end.setFixedSize(QSize(1032, 30))
        self.button_end.clicked.connect(self.end_app)
        ## второй слой окна
        ### верхняя и нижняя картинки второго окна
        self.upper_img_widget = QLabel("")
        upimg = QImage(os.path.join(basedir, "media/up.png")).scaled(1032, 100)
        self.upper_img_widget.setPixmap(QPixmap.fromImage(upimg))
        self.bottom_img_widget = QLabel("")
        btimg = QImage(os.path.join(basedir, "media/btm.png")).scaled(1032, 100)
        self.bottom_img_widget.setPixmap(QPixmap.fromImage(btimg))
        ### надпись дилера и игрока
        self.diler_cards_lable = QLabel("Расклад дилера:")
        self.diler_cards_lable.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.player_cards_lable = QLabel(f"...расклад для {self.player_name.upper()}")
        self.player_cards_lable.setAlignment(Qt.AlignmentFlag.AlignRight)
        ### отображение суммы и ставки игрока
        self.stavka_line_lable = QLabel("Ставка:")
        self.stavka_line = QLineEdit(f'{self.player_stavka}')
        self.stavka_line.setReadOnly(True)
        self.summ_line_lable = QLabel("Средства:")
        self.summ_line = QLineEdit(f'{self.player_summ}')
        self.summ_line.setReadOnly(True)
        self.button_play_again = QPushButton("Сыграть еще")
        self.button_play_again.setEnabled(False)
        self.button_play_again.clicked.connect(self.start_game)
        ### зона отображения карт
        self.widget_for_box = QWidget()
        #### создать пустую таблицу
        self.layoutggrid = QGridLayout()
        self.first_one = QLabel('')
        self.first_two = QLabel('')
        self.first_three = QLabel('')
        self.first_four = QLabel('')
        self.first_five = QLabel('')
        self.first_six = QLabel('')
        self.first_seven = QLabel('')
        self.second_one = QLabel('')
        self.second_two = QLabel('')
        self.second_three = QLabel('')
        self.second_four = QLabel('')
        self.second_five = QLabel('')
        self.second_six = QLabel('')
        self.second_seven = QLabel('')
        self.first_names = ['first_one', 'first_two', 'first_three', 'first_four', 'first_five', 'first_six',
                            'first_seven']
        self.second_names = ['second_one', 'second_two', 'second_three', 'second_four', 'second_five', 'second_six',
                             'second_seven']
        ### зона текстовых оповещений
        self.text_result_panel = QPlainTextEdit()
        self.text_result_panel.setReadOnly(True)
        ### кнопки игрока
        self.button_double = QPushButton("Удвоить ставку!")
        self.button_double.clicked.connect(self.bouble_stavka)
        self.button_more = QPushButton("Еще")
        self.button_more.setDefault(True)
        self.button_more.clicked.connect(self.more_btn)
        self.button_stop = QPushButton("Хватит")
        self.button_stop.clicked.connect(self.hvatit_btn)
        self.button_exit = QPushButton("Выйти")
        self.button_exit.clicked.connect(self.exit_game)

        # отрисовка окна
        ## визуализировать расклад карт
        self.create_card_visualisation()
        ## виджет для визуализации расклада карт
        self.widget_for_box = QWidget()
        self.widget_for_box.setAutoFillBackground(True)
        palette = self.widget_for_box.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        self.widget_for_box.setPalette(palette)
        self.widget_for_box.setLayout(self.layoutggrid)
        ## виджеты для возведения конструкции
        self.v_box_first_layout = QVBoxLayout()
        self.widget_for_first_layout = QWidget()
        self.money_info = QHBoxLayout()
        self.widget_for_money_info = QWidget()
        self.h_box_player_btn = QHBoxLayout()
        self.widget_for_box_player_btn = QWidget()
        self.v_box_second_layout = QVBoxLayout()
        self.widget_for_second_layout = QWidget()
        self.stacked_layout = QStackedLayout()
        self.widget_for_widget_stacked_layout = QWidget()
        ## функция, возводящая конструкцию
        self.building_window_construction()
        ## помещение пустого виджета для многослойного виджета в центр окна
        self.setCentralWidget(self.widget_for_widget_stacked_layout)
        my_logger.debug(f"Основное окно построено")

    def create_card_visualisation(self):
        for i in range(len(self.first_names)):
            self.layoutggrid.addWidget(self.__getattribute__(self.first_names[i]), 0, i)
        for i in range(len(self.second_names)):
            self.layoutggrid.addWidget(self.__getattribute__(self.second_names[i]), 1, i)
        my_logger.debug(f"Пустые виджеты вложены в сетку визуализации карт в основном окне")

    def update_hands(self):
        self.player_hand = self.game.player.get_hand()
        self.dealer_hand = self.game.dealer.get_hand()
        my_logger.debug(f"Обновлен расклад на руках у игрока и дилера")
        self.create_card_visualisation()

    def update_card_visualisation(self):
        ### обновить имеющиеся карты участников
        self.update_hands()
        ### создать список картинок
        player_card_img = []
        for i in self.player_hand:
            player_card_img.append(QImage(os.path.join(basedir, f"media/cards/{i.rank}-{i.suit[0]}.png")))
        dealer_card_img = []
        for i in self.dealer_hand:
            dealer_card_img.append(QImage(os.path.join(basedir, f"media/cards/{i.rank}-{i.suit[0]}.png")))
        ### заполнить таблицу картинками
        indx1 = 0
        for card in dealer_card_img:
            self.__getattribute__(self.first_names[indx1]).setPixmap(QPixmap.fromImage(card).scaled(150, 200))
            indx1 += 1
        indx2 = 6
        for card in player_card_img:
            self.__getattribute__(self.second_names[indx2]).setPixmap(QPixmap.fromImage(card).scaled(150, 200))
            indx2 -= 1
        my_logger.debug(f"Расклады на руках у игрока и дилера вложены в сетку отображения карт")

    def clean_cards(self):
        for i in self.first_names:
            self.__getattribute__(i).setText(" ")
        for i in self.second_names:
            self.__getattribute__(i).setText(" ")
        my_logger.debug(f"Сетка отображения карт в основном окне очищена")

    def building_window_construction(self):
        # конструирование первого слоя окна
        ## помещение в вертикалный контейнер:
        ### стартовой картинки
        self.v_box_first_layout.addWidget(self.start_img_widget)
        ### надписи, с обращением по имени к игроку
        self.v_box_first_layout.addWidget(self.player_name_lable)
        ### надписи с указанием суммы игрока
        self.v_box_first_layout.addWidget(self.player_summ_lable)
        ### кнопки начала игры
        self.v_box_first_layout.addWidget(self.button_play)
        ### кнопки вывода средств
        self.v_box_first_layout.addWidget(self.button_end)
        ### нижней картинки
        self.v_box_first_layout.addWidget(self.start_btm_img_widget)
        ## помещение вертикально контейнера первого слоя в пустой виджет
        self.widget_for_first_layout.setLayout(self.v_box_first_layout)

        # конструирование второго слоя окна
        ## создание подвиджетов второго окна
        ### отображение кнопки "сыграть еще"
        self.money_info.addWidget(self.button_play_again)
        ### отображение ставки игрока
        self.money_info.addWidget(self.stavka_line_lable)
        self.money_info.addWidget(self.stavka_line)
        ### отображение средств игрока
        self.money_info.addWidget(self.summ_line_lable)
        self.money_info.addWidget(self.summ_line)
        ### пустой виджет для подвиджета
        self.widget_for_money_info.setLayout(self.money_info)
        ## создание виджетов для отображения кнопок игрока
        ### размещение кнопок по горизонтали
        self.h_box_player_btn.addWidget(self.button_double)
        self.h_box_player_btn.addWidget(self.button_more)
        self.h_box_player_btn.addWidget(self.button_stop)
        self.h_box_player_btn.addWidget(self.button_exit)
        ### пустой виджет для горизонтального виджета кнопок
        self.widget_for_box_player_btn.setLayout(self.h_box_player_btn)
        ## помещение в вертикалный контейнер:
        ### верхней картинки
        self.v_box_second_layout.addWidget(self.upper_img_widget)
        ### надписи "расклад дилера"
        self.v_box_second_layout.addWidget(self.diler_cards_lable)
        ### визуализации карточного расклада
        self.v_box_second_layout.addWidget(self.widget_for_box)
        ### надписи "расклад игрока"
        self.v_box_second_layout.addWidget(self.player_cards_lable)
        ### панели текстовых отображений событий
        self.v_box_second_layout.addWidget(self.text_result_panel)
        ### данных о финансах игрока
        self.v_box_second_layout.addWidget(self.widget_for_money_info)
        ### кнопок игрока
        self.v_box_second_layout.addWidget(self.widget_for_box_player_btn)
        ### нижней картинки
        self.v_box_second_layout.addWidget(self.bottom_img_widget)
        ## помещение вертикально контейнера второго слоя в пустой виджет
        self.widget_for_second_layout.setLayout(self.v_box_second_layout)

        # собирание обоих слоев в одно окно
        ## вкладывание пустых виджетов слоев в единый многослойны виджет
        self.stacked_layout.addWidget(self.widget_for_first_layout)
        self.stacked_layout.addWidget(self.widget_for_second_layout)
        ## установка слоя по-умолчанию
        self.stacked_layout.setCurrentIndex(self.layout_num)
        ## помещение многослойного виджета в пустой виджет
        self.widget_for_widget_stacked_layout.setLayout(self.stacked_layout)
        my_logger.debug(f"Основное окно построено")

    # игровые действия
    def set_user_info(self):
        name, ok = QInputDialog.getText(
            self, "Кто ты, лудоман?", "Введите имя:"
        )
        self.player_name = name
        self.player_name_lable.setText(f'Приветствую тебя, {self.player_name}!')
        my_logger.debug(f"Получено имя игрока: {name}")

        summ, done = QInputDialog.getInt(
            self, 'Какую сумму прокутить?', 'Покажи купюры!')
        self.player_summ = summ
        self.player_summ_lable.setText(f'Твой депозит: {str(self.player_summ)}')
        my_logger.debug(f"Получена сумма, которую игрок хочет проиграть: {summ}")

    def update_player_info(self):
        self.player_cards_lable.setText(f"...расклад для {self.player_name.upper()}")
        self.stavka_line.setText(f'{self.player_stavka}')
        self.summ_line.setText(f'{self.player_summ}')
        my_logger.debug(f"Обновлена информация об игроке в основном окне: "
                        f"имя - {self.player_name.upper()}, ставка - {self.player_stavka}, сумма - {self.player_summ}")

    def set_text_to_result_panel(self, text):
        self.text_result_panel.appendPlainText(str(text))
        my_logger.debug(f"В текстовую панель результата добавлен текст: {text}")

    def raise_messagebox(self, title, text, icon=QMessageBox.Icon.Information):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.setIcon(icon)
        dlg.exec()
        my_logger.debug(f"Вызвано информационное окно: {title}")

    def update_btn_enable(self):
        if not self.btn_enable:
            self.button_double.setEnabled(False)
            self.button_more.setEnabled(False)
            self.button_stop.setEnabled(False)
            my_logger.debug(f"Доступность кнопок игрока отключена")
        else:
            self.button_double.setEnabled(True)
            self.button_more.setEnabled(True)
            self.button_stop.setEnabled(True)
            my_logger.debug(f"Доступность кнопок кнопок игрока включена")

    def start_game(self):
        self.layout_num = 1
        self.endgame = False
        self.button_play_again.setEnabled(False)
        self.game = GameActions()
        my_logger.debug(f"Создан новый экземпляр GameActions()")
        self.text_result_panel.clear()
        my_logger.debug(f"Текстовая панель результата очищена")
        self.text_result_panel.appendPlainText("ИГРА НАЧАЛАСЬ!")

        summ, done = QInputDialog.getInt(
            self, 'Какова твоя ставка?', f'Сделай ставку, {self.player_name}:')
        self.player_stavka = summ
        my_logger.debug(f"Получена ставка игрока: {summ}")

        self.clean_cards()
        self.stacked_layout.setCurrentIndex(self.layout_num)
        self.update_player_info()
        self.update_card_visualisation()
        self.update_btn_enable()
        self.set_text_to_result_panel("ПЕРВЫЙ РАСКЛАД ГОТОВ")
        self.dealer_move()

    def dealer_move(self):
        self.text_result_panel.appendPlainText("Ходит ДИЛЕР")
        QtTest.QTest.qWait(2000)
        my_logger.debug(f"Дилер задерживает алгоритм на 2000 милисекунд, притворяясь думающим человеком")
        move = self.game.do_dealer_move()
        if move:
            self.text_result_panel.appendPlainText("Ход ДИЛЕРА: Еще")
            self.update_card_visualisation()
        else:
            self.text_result_panel.appendPlainText("Ход ДИЛЕРА: Хватит")
        self.check_result()

    def create_end_msg(self):
        end_msg = ''
        results_dict = {
            '1111': ['У обоих BLACKJACK!!!', 1, 0],
            '0011': ['У Дилера BLACKJACK!!!', 0, 1],
            '1100': [f'У {self.player_name} BLACKJACK!!!', 2, 0],
            '0000': ['Ничья. Оба продули...', 0, 0],
            '1000': [f'{self.player_name} победил!', 1, 0],
            '0010': ['Дилер победил!', 0, 1],
        }
        a = int(self.game.result.is_player_win)
        b = int(self.game.result.is_player_blackjack)
        c = int(self.game.result.is_dealer_win)
        d = int(self.game.result.is_dealer_blackjack)
        result_str = f'{a}{b}{c}{d}'
        msg_draft = results_dict[result_str]
        self.text_result_panel.appendPlainText(f"Игра окончена: {msg_draft[0]}")
        self.text_result_panel.appendPlainText(f"Результат: Дилер - {self.game.result.dealer_result}, "
                                               f"{self.player_name} - {self.game.result.player_result}")
        self.raise_messagebox('GAMEOVER', msg_draft[0], icon=QMessageBox.Icon.Warning)
        my_logger.debug(f"Создан черновик сообщения о результате игры: {msg_draft}")
        return msg_draft

    def execution(self, exe_value):
        my_logger.debug(f"Черновик сообщения о результате игры передан на исполнение")
        if exe_value[2] == 1:
            self.player_summ = self.player_summ - self.player_stavka
            self.text_result_panel.appendPlainText(f"{self.player_name} оштрафован(а) на {self.player_stavka}. "
                                                   f"Оставшаяся сумма: {self.player_summ}")
            self.update_player_info()
        elif exe_value[1] == 2:
            self.player_summ = self.player_summ + self.player_stavka * 2
            self.text_result_panel.appendPlainText(f"{self.player_name} получил(а) "
                                                   f"{self.player_stavka} * 2 ({self.player_stavka * 2}). "
                                                   f"Итоговая сумма: {self.player_summ}")
            self.update_player_info()
        elif exe_value[1] == 1:
            self.player_summ = self.player_summ + self.player_stavka
            self.text_result_panel.appendPlainText(f"{self.player_name} получил(а) {self.player_stavka}. "
                                                   f"Итоговая сумма: {self.player_summ}")
            self.update_player_info()
        elif exe_value[1] == 0 and exe_value[2] == 0:
            self.text_result_panel.appendPlainText(f"Материальное состояние {self.player_name} не изменилось...")
        self.button_play_again.setEnabled(True)

    def check_result(self):
        is_end = self.game.check_results()
        my_logger.debug(f"Проверка результатов игры")
        if (self.game.player.get_stand == True) and (self.game.dealer.get_stand == True):
            self.endgame = True
        if not is_end:
            self.endgame = True
            exe_value = self.create_end_msg()
            self.execution(exe_value)
        else:
            self.btn_enable = True
            self.update_btn_enable()
            self.raise_messagebox(f"Пора ходить...", f"{self.player_name}, твой ход!")
            self.text_result_panel.appendPlainText(f"Ходит {self.player_name}")

    def bouble_stavka(self):
        my_logger.debug(f"{self.player_name} нажал кнопку 'удвоить ставку'")
        self.text_result_panel.appendPlainText(f"{self.player_name} удвоил(а) ставку! И требует еще карту.")
        self.player_stavka = self.player_stavka * 2
        self.raise_messagebox("Удвоение ставки!", f"{self.player_name} удвоил ставку!\nТеперь ставка {self.player_stavka}!",
                              icon=QMessageBox.Icon.Critical)
        self.stavka_line.setText(f'{self.player_stavka}')
        self.more_btn(double_stavka=True)

    def more_btn(self, double_stavka=False):
        my_logger.debug(f"{self.player_name} нажал кнопку 'еще'")
        if not double_stavka:
            self.text_result_panel.appendPlainText(f"Ход {self.player_name}: Еще")
        self.btn_enable = False
        self.update_btn_enable()
        self.game.do_player_move()
        self.update_card_visualisation()
        self.dealer_move()

    def hvatit_btn(self):
        my_logger.debug(f"{self.player_name} нажал кнопку 'хватит'")
        self.text_result_panel.appendPlainText(f"Ход {self.player_name}: Хватит")
        self.btn_enable = False
        self.update_btn_enable()
        self.game.do_player_move(hvatit=True)
        self.update_card_visualisation()
        self.dealer_move()

    def exit_game(self):
        my_logger.debug(f"{self.player_name} нажал кнопку 'выйти'")
        self.layout_num = 0
        if not self.endgame:
            self.raise_messagebox("Не хорошо так уходить...",
                                  f"Вы оштрафованы на {self.player_stavka}",
                                  icon=QMessageBox.Icon.Warning)
            self.player_summ = self.player_summ - self.player_stavka
        self.player_summ_lable.setText(f'Твой депозит: {self.player_summ}')
        self.stacked_layout.setCurrentIndex(self.layout_num)

    def end_app(self):
        my_logger.debug(f"{self.player_name} попытался вывести средства")
        if self.player_summ >= 0:
            self.raise_messagebox("Ошибка банковской операции...",
                                  "Сожалеем, но денег нет.\n¯\\_(ツ)_/¯",
                                  icon=QMessageBox.Icon.Question)
        elif self.player_summ < 0:
            self.raise_messagebox(f"Ты нам должен(на) {abs(self.player_summ)}!",
                                  f"Наши злобные коллекторы \nуже ищут тебя, {self.player_name}",
                                  icon=QMessageBox.Icon.Critical)
        sys.exit()

