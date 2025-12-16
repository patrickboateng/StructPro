from typing import Optional

from PySide6.QtCore import Qt, QLine, QPoint, QRectF, QPointF
from PySide6.QtGui import QBrush, QPen, QPainter, QMouseEvent
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QWidget,
    QGraphicsItem,
    QGraphicsEllipseItem,
    QGraphicsSceneWheelEvent,
    QGraphicsSceneMouseEvent,
)


class Point(QGraphicsEllipseItem):
    pen = QPen(Qt.GlobalColor.green)
    brush = QBrush(Qt.GlobalColor.blue)

    def __init__(
            self,
            x: float,
            y: float,
            w: float,
            h: float,
            scene=None,
            main_window=None,
    ):
        super().__init__(x, y, w, h)

        self.scene = scene
        self.main_window = main_window

        self.setPen(self.pen)
        self.setBrush(self.brush)


class GridNode(Point):
    pen = QPen(Qt.GlobalColor.red)
    brush = QBrush(Qt.GlobalColor.red)


class GridPoint(Point):

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if (
                event.button() == Qt.LeftButton
                and self.main_window.draw_node_action.isChecked()
        ):
            print("left click received")

            print(self.pos())
            node = GridNode(0, 0, 10, 10, self.scene, self.main_window)
            node.setPos(self.pos())
            self.scene.addItem(node)

        super().mousePressEvent(event)


class Scene(QGraphicsScene):

    def __init__(self, main_window):
        super().__init__(0, 0, 800, 600)

        self.main_window = main_window

        self.addRect(self.sceneRect(), QPen(Qt.red))
        self.create_grid()

    def create_grid(self):

        for row in range(0, 800, 50):
            for col in range(0, 600, 50):
                ellipse = GridPoint(0, 0, 10, 10, self, self.main_window)
                ellipse.setPos(row + 20, col + 20)
                self.addItem(ellipse)
                # ellipse.setFlag(
                #     QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
                # )

    def wheelEvent(self, event: QGraphicsSceneWheelEvent):
        if event.delta() > 0:
            self.main_window.zoom_in()
        else:
            self.main_window.zoom_out()
        event.accept()


class Editor(QGraphicsView):

    def __init__(self, scene: QGraphicsScene,
                 parent: Optional[QWidget] = None):
        super().__init__(scene, parent)

        self.scene = scene
        self.parent = parent

        self.setRenderHints(QPainter.Antialiasing)
