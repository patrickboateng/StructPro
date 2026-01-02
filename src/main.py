from PySide6.QtWidgets import QApplication

from frontend.main_window import MainWindow

app = QApplication([])

win = MainWindow()
win.show()

app.exec()
