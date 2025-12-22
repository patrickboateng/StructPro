from typing import Optional

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QPainter
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QWidget,
    QGraphicsEllipseItem,
    QGraphicsSceneWheelEvent,
    QGraphicsSceneMouseEvent,
)

from .settings import load_settings
from .custom_events import GRID_UPDATED_EVENT


# class Point(QGraphicsEllipseItem):
#     pen = QPen(Qt.GlobalColor.green)
#     brush = QBrush(Qt.GlobalColor.blue)
#
#     def __init__(
#         self,
#         x: float,
#         y: float,
#         w: float,
#         h: float,
#         scene=None,
#         main_window=None,
#     ):
#         super().__init__(x, y, w, h)
#
#         self.scene = scene
#         self.main_window = main_window
#
#         self.setPen(self.pen)
#         self.setBrush(self.brush)
#
#
# class GridNode(Point):
#     pen = QPen(Qt.GlobalColor.red)
#     brush = QBrush(Qt.GlobalColor.red)
#
#
# class GridPoint(Point):
#
#     def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
#         if (
#             event.button() == Qt.LeftButton
#             and self.main_window.draw_node_action.isChecked()
#         ):
#             print("left click received")
#
#             print(self.pos())
#             node = GridNode(0, 0, 10, 10, self.scene, self.main_window)
#             node.setPos(self.pos())
#             self.scene.addItem(node)
#
#         super().mousePressEvent(event)


# ellipse.setFlag(
#     QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
# )


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, pos: QPointF, radius: float = 5.0):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)

        self.setPos(pos)
        

class Scene(QGraphicsScene):

    def __init__(self, main_window):
        super().__init__(0, 0, 800, 800)

        self.main_window = main_window

        self.create_grid(load_settings()["grid"])

    def create_grid(self, grid):

        gridlines_x_dir = grid.gridlines_x_dir
        gridlines_y_dir = grid.gridlines_y_dir
        grid_spacing_x_dir = grid.grid_spacing_x_dir
        grid_spacing_y_dir = grid.grid_spacing_y_dir

        x_gridlines_len = (gridlines_y_dir - 1) * grid_spacing_y_dir
        y_gridlines_len = (gridlines_x_dir - 1) * grid_spacing_x_dir
        grid_scale_factor = (self.width() / grid_spacing_x_dir) / (
                gridlines_x_dir - 1)

        x_gridlines_len *= grid_scale_factor
        y_gridlines_len *= grid_scale_factor
        grid_spacing_x_dir *= grid_scale_factor
        grid_spacing_y_dir *= grid_scale_factor

        # Add gridlines in X direction
        for x in range(0, gridlines_x_dir):
            delta_x = grid_spacing_x_dir * x
            self.addLine(delta_x, 0, delta_x, x_gridlines_len)

        # Add gridlines in Y direction
        for y in range(0, gridlines_y_dir):
            delta_y = grid_spacing_y_dir * y
            self.addLine(0, delta_y, y_gridlines_len, delta_y)

    def update_grid(self, grid):
        self.clear()
        self.create_grid(grid)

    def event(self, event):
        if event.type() == GRID_UPDATED_EVENT:
            self.update_grid(event.grid)
            event.accept()
        return super().event(event)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent):
        if event.delta() > 0:
            self.main_window.zoom_in()
        else:
            self.main_window.zoom_out()
        event.accept()


class Editor(QGraphicsView):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setScene(Scene(parent))
        self.main_window = parent

        self.setRenderHints(QPainter.Antialiasing)

    def fitInView(self, item=None, aspect_ratio_mode=Qt.KeepAspectRatio):
        super().fitInView(
            self.scene().sceneRect() if item is None else item,
            aspect_ratio_mode
        )
