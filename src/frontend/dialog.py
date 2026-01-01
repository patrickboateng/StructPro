from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class DialogFormInputFloat(QLineEdit):
    def __init__(self, text: str | float):
        super().__init__(text=str(text))

        self.setValidator(QDoubleValidator())

    def text(self):
        return float(super().text())


class GridSpacingDialog(QDialog):
    grid_spacing_changed = Signal(float)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setWindowTitle("Grid Spacing")
        self.parent = parent

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.btn_box = QDialogButtonBox(btns)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

        self.grid_spacing_input = DialogFormInputFloat(20)
        grid_spacing_form_layout = QFormLayout()
        grid_spacing_form_layout.addRow("Grid spacing",
                                        self.grid_spacing_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_spacing_form_layout)
        main_layout.addWidget(self.btn_box)

        self.setLayout(main_layout)

    def accept(self):
        self.grid_spacing_changed.emit(self.grid_spacing_input.text())
        super().accept()
