from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication

from frontend.main_window import MainWindow

app = QApplication([])

screen = QGuiApplication.primaryScreen().availableGeometry()
screen_width, screen_height = screen.width(), screen.height()

WINDOW_SCALE = 0.9

win_width = int(WINDOW_SCALE * screen_width)
win_height = int(WINDOW_SCALE * screen_height)

win = MainWindow(win_width, win_height)
win.show()

app.exec()
