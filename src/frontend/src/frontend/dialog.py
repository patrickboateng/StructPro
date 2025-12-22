from types import SimpleNamespace

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator, QFontMetrics
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QTabWidget,
)

from .custom_events import GridUpdatedEvent
from .settings import load_settings


class DialogFormInputInt(QLineEdit):
    def __init__(self, text: str | int):
        super().__init__(text=str(text))

    def text(self):
        return int(super().text())


class DialogFormInputFloat(QLineEdit):
    def __init__(self, text: str | float):
        super().__init__(text=str(text))

    def text(self):
        return float(super().text())


class GridLinesDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setWindowTitle("Create Grid Lines")

        self.main_window = parent
        self.grid_settings = load_settings()["grid"]

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.btn_box = QDialogButtonBox(btns)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

        gridlines_group = QGroupBox("Number of Grid Lines")
        gridlines_layout = QFormLayout()

        self.gridlines_x_dir_input = DialogFormInputInt(
            text=self.grid_settings.gridlines_x_dir
        )
        self.gridlines_x_dir_input.setValidator(QIntValidator())

        self.gridlines_y_dir_input = DialogFormInputInt(
            text=self.grid_settings.gridlines_y_dir
        )
        self.gridlines_y_dir_input.setValidator(QIntValidator())

        gridlines_layout.addRow(
            "X direction",
            self.gridlines_x_dir_input,
        )
        gridlines_layout.addRow(
            "Y direction",
            self.gridlines_y_dir_input,
        )
        gridlines_group.setLayout(gridlines_layout)

        grid_spacing_group = QGroupBox("Grid Spacing")
        grid_spacing_layout = QFormLayout()

        self.grid_spacing_x_dir_input = DialogFormInputFloat(
            text=self.grid_settings.grid_spacing_x_dir
        )
        self.grid_spacing_x_dir_input.setValidator(QDoubleValidator(decimals=2))

        self.grid_spacing_y_dir_input = DialogFormInputFloat(
            text=self.grid_settings.grid_spacing_y_dir
        )
        self.grid_spacing_y_dir_input.setValidator(QDoubleValidator(decimals=2))

        grid_spacing_layout.addRow("X direction", self.grid_spacing_x_dir_input)
        grid_spacing_layout.addRow("Y direction", self.grid_spacing_y_dir_input)
        grid_spacing_group.setLayout(grid_spacing_layout)

        wgt = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(gridlines_group)
        layout.addWidget(grid_spacing_group)
        layout.addWidget(self.btn_box)
        wgt.setLayout(layout)

        tabs = QTabWidget(self)
        fm = QFontMetrics(tabs.font())
        font = fm.elidedText("2D Uniform Grid Spacing", Qt.ElideRight, 75)
        idx = tabs.addTab(wgt, "2D Uniform Grid Spacing")
        tabs.setTabText(idx, font)
        tabs.setTabToolTip(idx, "2D Uniform Grid Spacing")
        # tab.addTab(wgt, "2D Custom Grid Spacing")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)

        self.setLayout(main_layout)

    def get_grid_settings(self):
        return {
            "gridlines_x_dir": self.gridlines_x_dir_input.text(),
            "gridlines_y_dir": self.gridlines_y_dir_input.text(),
            "grid_spacing_x_dir": self.grid_spacing_x_dir_input.text(),
            "grid_spacing_y_dir": self.grid_spacing_y_dir_input.text(),
        }

    def update_settings(self):
        settings = load_settings()
        settings.grid.update(self.get_grid_settings())

    def accept(self):
        self.update_settings()
        self.grid_settings = load_settings()["grid"]
        QCoreApplication.sendEvent(
            self.main_window.editor.scene(), GridUpdatedEvent(grid=self.grid_settings)
        )
        super().accept()
