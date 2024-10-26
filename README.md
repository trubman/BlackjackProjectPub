# BlackjackProject

## Проект по двум модулям учебной программы "Python-разработчик" Университета Синергия

Этот проект выполняет сразу два проектных задания:
- реализовать консольную версию карточной игры blackjack (модуль "Основы языка программирования Python");
- создать и заполнить свой репозиторий на GitHub (модуль "Git").

## О приложении "Synergy Blackjack"

Игра blackjack имеет две реализации:
- в виде консольного приложения с CLI;
- в виде оконного приложения с GUI.

### Правила игры:

Blackjack - карточная игра, в которой игрок соревнуется с Дилером.
Исходом может быть:
- проигрыш (игрок теряет ставку),
- ничья (игрок остается при своей ставке),
- победа (игрок получает выигрыш в виде ставки).

Используется колода 52 карты. Выигрывает тот, у кого очков на карте больше чем у соперника и отсутствует перебор.

   ![Очки](/README_img/ochki.jpg)

### Как играть в консольное приложение?

Необходимо запустить файл `blackjack_cli.py` и вводить команды в терминале:

1. Введите ставку:

   ![Ставка](/README_img/stavka.jpg)

2. После этого игра сделает первый расклад и предоставит ход Вашему сопернику - Дилеру. Когда Дилер сообщит о своем решении - ход перйдет к Вам.

   ![Ход](/README_img/first_hod.jpg)

   Вам доступны три варианта хода:
      - "Еще" - сообщите игре, что хотите получить еще одну карту;
      - "Хватит" - после этого игра перестанет пополнять Ваш расклад;
      - "Удвоить" - Ваша ставка умножается на два.

3. Игра снова раздает карты Вам и Дилеру (в зависимости от ваших решений).
4. Игра будет продолжаться пока результат не станет очевиден.

   ![Конец игры](/README_img/end_game.jpg)

### Как играть в оконное приложение?

Необходимо запустить файл `main.py`:
(Обратите внимание, что GUI реализовано с помощью библиотеки `PyQt6`)

1. Игра потребует Ваше имя:

   ![Имя](/README_img/name.jpg)

2. Игра потребует сумму, которую Вы хотите проиграть:

   ![Сумма](/README_img/summ.jpg)

3. Теперь, Вы можете начать игру - нажмите "Сыграть!":

   ![Сыграть](/README_img/start_w.jpg)

4. Введите ставку:

   ![Ставка](/README_img/stavka_v.jpg)

4. Игра уже приготовила для Вас расклад. Первым ходит Дилер, а потом Ваш черед:

   ![Сыграть](/README_img/first_hod_w.jpg)
   
   Вам доступны следующие кнопки:
      - "Удвоить ставку!" - Ваша ставка умножается на два;
      - "Еще" - запросить еще карту;
      - "Хватит" - воздержаться от получения карты;
      - "Выйти" - перейти в стартовое окно.

5. Игра будет продолжаться пока результат не станет ясен:

   ![Итог](/README_img/result_w.jpg)

   Теперь Вы можете уйти на стартовое окно - нажмите "Выйти", или продолжить проигрывать свои деньги - нажмите "Сыграть еще".

## Описание файлов и папок

| Файл               | Описание                                                                                                                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.gitignore`       | содержит список всех указанных файлов и папок проекта, которые Git должен игнорировать                                                                                                                |
| `README.md`        | описание проекта                                                                                                                                                                                      |
| `blackjack_cli.py` | консольный вариант игры                                                                                                                                                                               |
| `deck.py`          | содержит класс колоды `Deck`, а также класс карт `Card`. При инициализации, `Deck` создает колоду из 52 карт, перемешивает её случайным образом и выдает по одной когда это необходимо                |
| `gameactions.py`   | описывает основные игровые действия: ход Игрока, ход Дилера, проверку результатов. При инициализации создает колоду `Deck`, экземпляры `UniPlayer` для Игрока и Дилера, а также делает первый расклад |
| `main.py`          | запускает игру, создает экземпляр `QApplication` и основное окно `MainWindow` , необходимые для функционирования `PyQt6`                                                                              |
| `mainwindowgui.py` | содержит класс `MainWindow`, который строит виджеты GUI, отслеживает нажатие кнопок, передает команды экземпляру класса `GameActions` для выполнения игровых действий                                 |
| `my_logging.py`    | файл настройки логирования                                                                                                                                                                            |
| `test_main.py`     | нереализованное тестирование `PyQt6` через `pytest-qt`                                                                                                                                                |
| `uniplayer.py`     | содержит описание класса `UniPlayer` для представления Игрока и Дилера                                                                                                                                |

| Папка        | Описание                                               |
| ------------ | ------------------------------------------------------ |
| `media`      | содержит изображения для окон, а также игральные карты |
| `README_img` | содержит скриншоты для `README.md`                     |


