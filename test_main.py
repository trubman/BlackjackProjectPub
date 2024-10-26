import pytest, pytestqt

# from PyQt6 import QtCore
# from PyQt6.QtWidgets.QWidget import window

from main import MainWindow


@pytest.fixture
def app(qtbot):
    window = MainWindow()
    window.show()
    qtbot.addWidget(window)
    return window


def test_label(app):
    assert app.windowTitle() == "Synergy Blackjack"


# def test_label_after_click(app, qtbot):
#     qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
#     assert app.text_label.text() == "Changed!"