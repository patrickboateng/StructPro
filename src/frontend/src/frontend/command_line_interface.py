from typing import Optional

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDockWidget,
    QLineEdit,
    QPushButton,
    QWidget,
    QHBoxLayout,
)

from . import resources_rc


class CommandLineInterface(QDockWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        drag_handle = QWidget()
        drag_handle.setFixedHeight(24)
        drag_handle.setCursor(Qt.OpenHandCursor)
        self.setTitleBarWidget(drag_handle)

        self.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable,
        )
        self.setFixedWidth(600)
        self.setFixedHeight(32)

        btn_size = QSize(32, 32)

        self.settings_btn = QPushButton()
        self.settings_btn.setFixedSize(btn_size)
        self.settings_btn.setIcon(QIcon(":/misc/settings"))

        self.command_line_wgt = QLineEdit()
        self.command_line_wgt.setFixedHeight(32)
        self.command_line_wgt.setPlaceholderText("Type a command")
        self.command_line_wgt.addAction(
            QIcon(":/misc/terminal"),
            QLineEdit.LeadingPosition,
        )
        self.command_line_wgt.returnPressed.connect(
            self.on_command_line_wgt_enter_pressed
        )

        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(btn_size)
        self.close_btn.setIcon(QIcon(":/misc/close"))
        self.close_btn.clicked.connect(self.on_close_btn_clicked)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.command_line_wgt, 1)
        layout.addWidget(self.close_btn)

        wgt = QWidget()
        wgt.setLayout(layout)
        self.setWidget(wgt)

    def on_command_line_wgt_enter_pressed(self):
        pass

    def on_close_btn_clicked(self):
        self.hide()
