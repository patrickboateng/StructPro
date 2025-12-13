from PySide6.QtWidgets import QApplication

from frontend.main_window import MainWindow

app = QApplication([])
app.setStyle("Fusion")

win = MainWindow()
win.show()

app.exec()
