from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDockWidget, QHBoxLayout, QLineEdit, QPushButton, \
    QWidget

from . import resources_rc


class CommandLineInterface(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setFixedWidth(500)
        self.setFixedHeight(32)

        btn_size = QSize(32, 32)

        self.drag_handle_btn = QPushButton()
        self.drag_handle_btn.setFixedSize(btn_size)
        self.drag_handle_btn.setIcon(QIcon(":/misc/drag-handle"))

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

        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(btn_size)
        self.close_btn.setIcon(QIcon(":/misc/close"))
        # self.close_btn.pressed.connect(self.on_close_btn_clicked)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.drag_handle_btn)
        main_layout.addWidget(self.settings_btn)
        main_layout.addWidget(self.command_line_wgt, 1)
        main_layout.addWidget(self.close_btn)

        self.setLayout(main_layout)

    def on_command_line_wgt_enter_pressed(self):
        pass

    def on_close_btn_clicked(self):
        self.hide()
