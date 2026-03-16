import enum
import functools
import math
from typing import Optional

import numpy as np
from PySide6.QtCore import QLineF, QPointF, QRectF, Qt, Signal, QPoint
from PySide6.QtGui import (
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPen,
    QResizeEvent,
    QWheelEvent,
    QPixmap,
    QCursor,
)
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsView,
    QWidget,
    QGraphicsSceneEvent,
    QGraphicsSceneHoverEvent,
    QComboBox,
)

from .command_line_interface import CommandLineInterface
from .non_modal_dialog import CreateNodeDialog


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


class SceneMode(enum.StrEnum):
    SELECT_MODE = enum.auto()
    DRAW_NODE_MODE = enum.auto()
    DRAW_MEMBER_MODE = enum.auto()


class _NodeID:
    id = 0

    @classmethod
    def get_id(cls):
        cls.id += 1
        return cls.id


class _MemberID:
    id = 0

    @classmethod
    def get_id(cls):
        cls.id += 1
        return cls.id


class NodeItem(QGraphicsEllipseItem):

    def __init__(
            self,
            parent: Optional["Scene"],
            pos: QPointF,
            radius: float = 3.0,
            point_load_x_dir: Optional[float] = None,
            point_load_y_dir: Optional[float] = None,
            point_moment: Optional[float] = None,
            restraint_x_dir: Optional[bool] = None,
            restraint_y_dir: Optional[bool] = None,
            restraint_moment: Optional[bool] = None,
            user_defined: bool = True,
            frame_connected: Optional[str] = None,
    ):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)

        self.id = _NodeID.get_id()
        self.scene = parent
        self.point_load_x_dir = point_load_x_dir
        self.point_load_y_dir = point_load_y_dir
        self.point_moment = point_moment
        self.restraint_x_dir = restraint_x_dir
        self.restraint_y_dir = restraint_y_dir
        self.restraint_moment = restraint_moment
        self.user_defined = user_defined
        self.frame_connected = frame_connected
        self._hover_item = None

        pen = QPen(Qt.white, 1)
        pen.setCosmetic(True)

        self.setPos(pos)
        self.setBrush(QBrush(Qt.green))
        self.setPen(pen)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(10)
        self.setAcceptHoverEvents(True)

    def __str__(self) -> str:
        return f"Node {self.id}"

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        w = self.rect().width()
        self._hover_item = QGraphicsEllipseItem(-w, -w, 2 * w, 2 * w)
        self._hover_item.setPos(self.pos())
        self._hover_item.setPen(QPen(Qt.red))
        self.scene.addItem(self._hover_item)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if self._hover_item is not None:
            self.scene.removeItem(self._hover_item)
        super().hoverLeaveEvent(event)


class EdgeItem(QGraphicsLineItem):
    def __init__(self, start_node: QPointF, end_node: QPointF):
        super().__init__()

        self.id = _MemberID.get_id()

        self.start_node = start_node
        self.end_node = end_node

        self.setLine(QLineF(start_node, self.end_node))
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def __str__(self) -> str:
        return f"Member {self.id}"

    @property
    def length(self):
        delta_x = self.end_node.x() - self.start_node.x()
        delta_y = self.end_node.y() - self.start_node.y()
        return math.sqrt(delta_x ** 2 + delta_y ** 2)


class EdgePreview(QGraphicsLineItem):
    def __init__(self, start_node: QPointF, end_node: QPointF):
        super().__init__()

        pen = QPen(Qt.blue)
        pen.setStyle(Qt.DashLine)
        pen.setCosmetic(True)

        self.setZValue(10_000)  # on top
        self.setPen(pen)
        self.setLine(QLineF(start_node, end_node))


class Scene(QGraphicsScene):
    graphics_item_created = Signal(QGraphicsScene, QGraphicsItem)

    def __init__(self, parent=None, grid_size: float = 20.0):
        super().__init__(parent)

        self._grid_size = grid_size
        self.snap = True
        self.tool_mode = SceneMode.SELECT_MODE

        # member drawing state
        self._member_start_node: QPointF | None = None
        self._member_preview: EdgePreview = EdgePreview(QPointF(0, 0),
                                                        QPointF(0, 0))

    @property
    def grid_size(self) -> float:
        return self._grid_size

    @grid_size.setter
    def grid_size(self, grid_size: float):
        self._grid_size = grid_size
        self.update()

    @property
    def draw_node_clicked(self):
        return self.tool_mode == SceneMode.DRAW_NODE_MODE

    @property
    def draw_member_clicked(self):
        return self.tool_mode == SceneMode.DRAW_MEMBER_MODE

    @staticmethod
    def snap_to_grid(pos: QPointF, grid_size: float) -> QPointF:
        x = round(pos.x() / grid_size) * grid_size
        y = round(pos.y() / grid_size) * grid_size
        return QPointF(x, y)

    def set_snap_position(self, pos: QPointF) -> QPointF:
        if self.snap:
            pos = self.snap_to_grid(pos, self.grid_size)
        return pos

    @staticmethod
    @functools.lru_cache
    def _grid_coord(left: float, top: float, grid_size: float):
        left = math.floor(left / grid_size) * grid_size
        top = math.floor(top / grid_size) * grid_size
        return left, top

    def _draw_grid_lines(self, painter: QPainter, rect: QRectF):
        left, top = self._grid_coord(rect.left(), rect.top(), self.grid_size)
        pen = QPen(QColor(75, 75, 75), 1, Qt.SolidLine, Qt.FlatCap,
                   Qt.RoundJoin)
        pen.setCosmetic(True)
        painter.setPen(pen)

        x_grid_lines = [
            QLineF(x, rect.top(), x, rect.bottom())
            for x in np.arange(left, rect.right(), step=self.grid_size)
        ]
        y_grid_lines = [
            QLineF(rect.left(), y, rect.right(), y)
            for y in np.arange(top, rect.bottom(), step=self.grid_size)
        ]

        painter.drawLines(x_grid_lines)
        painter.drawLines(y_grid_lines)

    @staticmethod
    def _draw_grid_center_lines(painter: QPainter, rect: QRectF):
        x_axis_pen = QPen(QColor("red"), 2)
        x_axis_pen.setCosmetic(True)

        y_axis_pen = QPen(QColor("green"), 2)
        y_axis_pen.setCosmetic(True)

        painter.setPen(x_axis_pen)
        painter.drawLine(QLineF(rect.left(), 0, rect.right(), 0))

        painter.setPen(y_axis_pen)
        painter.drawLine(QLineF(0, rect.top(), 0, rect.bottom()))

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(55, 55, 55, 255)))
        painter.drawRect(rect)

        self._draw_grid_lines(painter, rect)
        self._draw_grid_center_lines(painter, rect)

    def mousePressEvent(self, event):
        mouse_pos = self.set_snap_position(event.scenePos())

        button_pressed = event.button()
        draw_node_mode = button_pressed == Qt.LeftButton and self.draw_node_clicked

        if draw_node_mode:
            node_item = NodeItem(self, mouse_pos)
            self.graphics_item_created.emit(self, node_item)
            event.accept()
            return

        draw_member_mode = button_pressed == Qt.LeftButton and self.draw_member_clicked

        if draw_member_mode:
            first_mouse_left_click = self._member_start_node is None
            if first_mouse_left_click:
                self._member_start_node = mouse_pos
                self.addItem(self._member_preview)
                event.accept()
            # Second mouse left click in draw member mode
            else:
                end_node = mouse_pos
                member = EdgeItem(self._member_start_node, end_node)
                self.graphics_item_created.emit(self, member)
                self.removeItem(self._member_preview)
                self._member_start_node = None
                event.accept()

            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        draw_member_mode = (
                self.tool_mode == SceneMode.DRAW_MEMBER_MODE
                and self._member_start_node is not None
        )

        if draw_member_mode:
            mouse_pos = event.scenePos()
            self._member_preview.setLine(
                QLineF(self._member_start_node, mouse_pos))
            event.accept()
            return

        super().mouseMoveEvent(event)


class Editor(QGraphicsView):
    scene_pos_changed = Signal(float, float)

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.setAcceptDrops(True)

        self.parent = parent
        self.setScene(Scene(parent))
        self.scale(1, -1)
        self.setRenderHints(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.command_line_interface = CommandLineInterface(self)
        self.command_line_interface.raise_()
        self.command_line_interface.adjustSize()
        self._position_command_line()

        self.workbench_mode = QComboBox(self)
        self.workbench_mode.setMaxCount(2)
        self.workbench_mode.setEditable(False)
        self.workbench_mode.setInsertPolicy(QComboBox.NoInsert)
        self.workbench_mode.addItems(["2D"])
        self._position_workbench_mode()

        # Pan support (middle mouse)
        # TODO: Rewrite panning code
        self._panning = False
        self._pan_start_x = None
        self._pan_start_y = None

    def _position_workbench_mode(self):
        viewport_width = self.viewport_width
        viewport_height = self.viewport_height
        wgt_width = self.workbench_mode.width()
        wgt_height = self.workbench_mode.height()
        x = viewport_width - wgt_width
        y = viewport_height - wgt_height
        self.workbench_mode.move(x, y)

    @property
    def viewport_width(self):
        return self.viewport().width()

    @property
    def viewport_height(self):
        return self.viewport().height()

    def _position_command_line(self):
        viewport_width = self.viewport_width
        viewport_height = self.viewport_height
        wgt_width = self.command_line_interface.width()
        wgt_height = self.command_line_interface.height()
        x = (viewport_width - wgt_width) // 2
        y = viewport_height - wgt_height
        self.command_line_interface.move(QPoint(x, y))

    def set_snap_enabled(self, enabled: bool):
        self.scene().snap = enabled

    def set_grid_size(self, grid_size: float):
        self.scene().grid_size = grid_size

    def set_tool_mode(self, mode: SceneMode):
        self.scene().tool_mode = mode
        if mode == SceneMode.DRAW_NODE_MODE:
            self.dlg = CreateNodeDialog(self)
            self.dlg.show()

    def scene(self) -> Scene:
        return super().scene()

    def _set_view_cursor(self):
        if self.scene().draw_node_clicked:
            cursor = QCursor(QPixmap(":/misc/node"), 4, 4)
            self.setCursor(cursor)
        elif self.scene().draw_member_clicked:
            cursor = QCursor(QPixmap(":/misc/member"), 3, 3)
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    # TODO: Rewrite logic
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start_x = event.x()
            self._pan_start_y = event.y()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    # TODO: Rewrite logic
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

        self._set_view_cursor()

        # TODO rewrite panning code

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

    # TODO: rewrite resizeEvent logic
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        w = self.rect().width()
        h = self.rect().height()
        self.setSceneRect(QRectF(-w / 2, -h / 2, w, h))
        self.centerOn(QPointF(0, 0))
        self._position_command_line()
        self._position_workbench_mode()

    def zoom_in(self):
        self.scale(1.2, 1.2)

    def zoom_out(self):
        self.scale(1 / 1.2, 1 / 1.2)

    # TODO: rewrite logic
    def zoom_fit(self):
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        event.accept()
