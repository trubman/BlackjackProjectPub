import sys
from PyQt6.QtWidgets import QApplication
from mainwindowgui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.set_user_info()

    app.exec()

