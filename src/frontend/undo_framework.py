from typing import Optional

from PySide6.QtCore import QPointF
from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import QGraphicsItem, QWidget

from .editor import Scene


class AddCommand(QUndoCommand):
    def __init__(
        self,
        scene: Scene,
        graphics_item: QGraphicsItem,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.scene = scene
        self.graphics_item = graphics_item

        self.setText(f"Add {str(graphics_item)}")

    def undo(self):
        self.scene.removeItem(self.graphics_item)
        self.scene.update()

    def redo(self):
        self.scene.addItem(self.graphics_item)
        self.scene.clearSelection()
        self.scene.update()


class DeleteCommand(QUndoCommand):
    def __init__(self, scene: Scene):
        super().__init__(None)
        self.scene = scene
        self.selected_graphics_item = self.scene.selectedItems()

        self.set_text(self.selected_graphics_item)

    def set_text(self, items: list[QGraphicsItem]):
        text = f"Delete {", ".join([str(item) for item in items])}"
        self.setText(text)

    def undo(self):
        for graphics_item in self.selected_graphics_item:
            self.scene.addItem(graphics_item)
            self.scene.update()

    def redo(self):
        for graphics_item in self.selected_graphics_item:
            self.scene.removeItem(graphics_item)
            self.scene.update()


class MoveCommand(QUndoCommand):
    def __init__(
        self,
        scene: Scene,
        graphics_item: QGraphicsItem,
        new_pos: QPointF,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self.scene = scene
        self.graphics_item = graphics_item
        self.new_pos = new_pos
        self.old_pos = self.graphics_item.pos()

        self.setText(f"Move {str(self.graphics_item)}")

    def undo(self):
        self.graphics_item.setPos(self.old_pos)
        self.scene.update()

    def redo(self):
        self.graphics_item.setPos(self.new_pos)
        self.scene.update()
