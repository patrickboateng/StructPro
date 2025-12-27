import math
from typing import Optional

import numpy as np

from PySide6.QtCore import Qt, QPointF, QRectF, Signal, QLineF
from PySide6.QtGui import (
    QBrush,
    QPen,
    QPainter,
    QMouseEvent,
    QWheelEvent,
    QResizeEvent,
    QColor,
)
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QWidget,
    QGraphicsEllipseItem,
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

# def _draw_grid_points(self, painter: QPainter, rect: QRectF):
#     left, top = self._grid_coord(rect)
#     painter.setPen(QPen(Qt.blue))
#     points = []
#     x = left
#     while x < rect.right():
#         y = top
#         while y < rect.bottom():
#             points.append(QPointF(x, y))
#             y += self.grid_size
#         x += self.grid_size
#
#     if points:
#         painter.drawPoints(points)


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, pos: QPointF, radius: float = 5.0):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)

        self.setPos(pos)

        self.setBrush(Qt.white)
        self.setPen(QPen(Qt.black, 1))


class Scene(QGraphicsScene):
    def __init__(self, parent=None, grid_size: float = 35.0):
        super().__init__(parent)
        self.grid_size = grid_size

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)

        # --- Background fill (like drawRect(rect) with a brush) ---
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(55, 55, 55, 255)))
        painter.drawRect(rect)

        self._draw_grid_thin_lines(painter, rect)
        self._draw_grid_thick_lines(painter, rect)
        self._draw_grid_center_lines(painter, rect)

    def _grid_coord(self, rect: QRectF):
        left = math.floor(rect.left() / self.grid_size) * self.grid_size
        top = math.floor(rect.top() / self.grid_size) * self.grid_size
        return left, top

    def _draw_grid_thin_lines(self, painter: QPainter, rect: QRectF):
        left, top = self._grid_coord(rect)
        x_lines = [
            QLineF(x, rect.top(), x, rect.bottom())
            for x in np.arange(left, rect.right(), step=self.grid_size)
        ]
        y_lines = [
            QLineF(rect.left(), y, rect.right(), y)
            for y in np.arange(top, rect.bottom(), step=self.grid_size)
        ]
        pen_thin = QPen(QColor(75, 75, 75), 1, Qt.SolidLine, Qt.FlatCap,
                        Qt.RoundJoin)
        pen_thin.setCosmetic(True)  # keep width constant while zooming
        painter.setPen(pen_thin)

        lines = x_lines + y_lines

        if lines:
            painter.drawLines(lines)

    @staticmethod
    def _draw_grid_center_lines(painter: QPainter, rect: QRectF):
        x_axis_pen = QPen(QColor("red"), 2)
        x_axis_pen.setCosmetic(True)  # stays 2px even when zooming

        y_axis_pen = QPen(QColor("green"), 2)
        y_axis_pen.setCosmetic(True)

        painter.setPen(x_axis_pen)
        painter.drawLine(QLineF(0, 0, rect.right(), 0))

        painter.setPen(y_axis_pen)
        painter.drawLine(QLineF(0, 0, 0, rect.bottom()))

    def _draw_grid_thick_lines(self, painter: QPainter, rect: QRectF):
        step = self.grid_size * 5.0
        left, top = self._grid_coord(rect)

        x_thick_lines = [
            QLineF(x, rect.top(), x, rect.bottom())
            for x in np.arange(left, rect.right(), step)
        ]

        y_thick_lines = [
            QLineF(rect.left(), y, rect.right(), y)
            for y in np.arange(top, rect.bottom(), step)
        ]

        thick_lines = x_thick_lines + y_thick_lines

        pen_thick = QPen(
            QColor(100, 100, 100), 2, Qt.SolidLine, Qt.FlatCap, Qt.RoundJoin
        )
        pen_thick.setCosmetic(True)
        painter.setPen(pen_thick)

        if thick_lines:
            painter.drawLines(thick_lines)

    def snap_to_grid(self, p: QPointF) -> QPointF:
        x = round(p.x() / self.grid_size) * self.grid_size
        y = round(p.y() / self.grid_size) * self.grid_size
        return QPointF(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            snapped = self.snap_to_grid(event.scenePos())
            self.addItem(NodeItem(snapped))
            event.accept()
            return
        super().mousePressEvent(event)


#     def event(self, event):
#         if event.type() == GRID_UPDATED_EVENT:
#             self.update()
#             event.accept()
#         return super().event(event)


class Editor(QGraphicsView):
    scene_pos_changed = Signal(float, float)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

        self.parent = parent
        self.setScene(Scene(parent))
        self.scale(1, -1)
        self.setRenderHints(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        # optional: hide scrollbars (still pans fine)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Pan support (middle mouse)
        self._panning = False
        self._pan_start_x = None
        self._pan_start_y = None

    def scene(self) -> Scene:
        return super().scene()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start_x = event.x()
            self._pan_start_y = event.y()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = self.mapToScene(event.pos())
        self.scene_pos_changed.emit(pos.x(), pos.y())

        if self._panning:

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - (
                            event.x() - self._pan_start_x)
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - (
                            event.y() - self._pan_start_y)
            )

            self._pan_start_x = event.x()
            self._pan_start_y = event.y()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        w = self.rect().width()
        h = self.rect().height()
        self.setSceneRect(QRectF(-w / 2, -h / 2, w, h))
        self.centerOn(QPointF(0, 0))

    def leaveEvent(self, event):
        self.scene_pos_changed.emit(float("nan"), float("nan"))
        super().leaveEvent(event)

    def zoom_in(self):
        self.scale(1.2, 1.2)

    def zoom_out(self):
        self.scale(1 / 1.2, 1 / 1.2)

    def zoom_fit(self):
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        event.accept()
