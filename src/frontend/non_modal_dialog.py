from PySide6.QtCore import Qt, QSize, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QDialogButtonBox,
    QHeaderView,
    QAbstractItemView,
    QTableWidgetItem,
    QStyledItemDelegate,
    QLineEdit,
    QStyleOptionViewItem,
)


class FloatDelegate(QStyledItemDelegate):

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        editor = QLineEdit(parent)
        editor.setValidator(QDoubleValidator())
        return editor


class CreateNodeDialog(QDialog):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setModal(False)
        self.setWindowTitle("Node Position")
        self.setFixedSize(QSize(220, 150))

        self.parent = parent

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.btn_box = QDialogButtonBox(btns)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

        self.wgt = QTableWidget(self)
        self.wgt.setRowCount(2)
        self.wgt.setColumnCount(2)
        self.wgt.setSelectionMode(QAbstractItemView.SingleSelection)
        self.wgt.setSelectionBehavior(QAbstractItemView.SelectItems)
        horizontal_header = self.wgt.horizontalHeader()
        vertical_header = self.wgt.verticalHeader()
        horizontal_header.setVisible(False)
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
        vertical_header.setVisible(False)
        vertical_header.setSectionResizeMode(QHeaderView.Stretch)

        x_header = QTableWidgetItem("X")
        x_header.setFlags(x_header.flags() & ~Qt.ItemIsEditable)
        x_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        y_header = QTableWidgetItem("Y")
        y_header.setFlags(y_header.flags() & ~Qt.ItemIsEditable)
        y_header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wgt.setItem(0, 0, x_header)
        self.wgt.setItem(1, 0, y_header)

        self.wgt.setItemDelegateForColumn(1, FloatDelegate(self.wgt))
        self.wgt.cellClicked.connect(self.cell_selected)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.wgt)
        main_layout.addWidget(self.btn_box)
        self.setLayout(main_layout)

    def cell_selected(self, row, column):
        if row == 0 and column == 0:
            self.wgt.setCurrentCell(row, column + 1)
            return
        if row == 1 and column == 0:
            self.wgt.setCurrentCell(row, column + 1)
            return

        print(row, column)

    def accept(self):
        pass

    def reject(self, /):
        self.close()


class EditNodeDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setModal(False)

        self.parent = parent
