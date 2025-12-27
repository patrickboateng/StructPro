from PySide6.QtWidgets import QApplication

from frontend.main_window import MainWindow

app = QApplication([])

win = MainWindow()
win.show()

app.exec()

# import sys
# import math
# from PySide6.QtCore import Qt, QPointF, QRectF
# from PySide6.QtGui import QPen, QPainter, QKeySequence
# from PySide6.QtWidgets import (
#     QApplication,
#     QGraphicsView,
#     QGraphicsScene,
#     QGraphicsEllipseItem,
#     QGraphicsLineItem,
# )
#
#
# # -------------------------
# # Helpers
# # -------------------------
# def dist2(a: QPointF, b: QPointF) -> float:
#     dx = a.x() - b.x()
#     dy = a.y() - b.y()
#     return dx * dx + dy * dy
#
#
# def snap_to_grid(p: QPointF, g: int) -> QPointF:
#     return QPointF(round(p.x() / g) * g, round(p.y() / g) * g)
#
#
# def snap_angle(start: QPointF, end: QPointF, step_degrees: float = 45.0) -> QPointF:
#     dx, dy = end.x() - start.x(), end.y() - start.y()
#     if dx == 0 and dy == 0:
#         return end
#     r = math.hypot(dx, dy)
#     ang = math.degrees(math.atan2(dy, dx))
#     snapped = round(ang / step_degrees) * step_degrees
#     rad = math.radians(snapped)
#     return QPointF(start.x() + r * math.cos(rad), start.y() + r * math.sin(rad))
#
#
# def constrain_orthogonal(start: QPointF, end: QPointF) -> QPointF:
#     dx, dy = end.x() - start.x(), end.y() - start.y()
#     if abs(dx) >= abs(dy):
#         return QPointF(end.x(), start.y())
#     return QPointF(start.x(), end.y())
#
#
# # -------------------------
# # Node and Line items
# # -------------------------
# class NodeItem(QGraphicsEllipseItem):
#     def __init__(self, pos: QPointF, radius: float = 5.0):
#         super().__init__(-radius, -radius, 2 * radius, 2 * radius)
#         self.setPos(pos)
#         self.radius = radius
#         self.lines = set()
#
#         self.setBrush(Qt.white)
#         self.setPen(QPen(Qt.black, 1))
#         self.setFlags(
#             QGraphicsEllipseItem.ItemIsMovable
#             | QGraphicsEllipseItem.ItemIsSelectable
#             | QGraphicsEllipseItem.ItemSendsGeometryChanges
#         )
#         self.setZValue(10)  # above lines
#
#     def add_line(self, line_item: "EdgeItem"):
#         self.lines.add(line_item)
#
#     def remove_line(self, line_item: "EdgeItem"):
#         self.lines.discard(line_item)
#
#     def itemChange(self, change, value):
#         if change == QGraphicsEllipseItem.ItemPositionChange:
#             # Update connected lines live while dragging
#             for ln in list(self.lines):
#                 ln.update_geometry()
#         return super().itemChange(change, value)
#
#
# class EdgeItem(QGraphicsLineItem):
#     def __init__(self, n1: NodeItem, n2: NodeItem, pen: QPen):
#         super().__init__()
#         self.n1 = n1
#         self.n2 = n2
#         self.setPen(pen)
#         self.setFlags(QGraphicsLineItem.ItemIsSelectable)
#         self.setZValue(1)
#         n1.add_line(self)
#         n2.add_line(self)
#         self.update_geometry()
#
#     def update_geometry(self):
#         p1 = self.n1.scenePos()
#         p2 = self.n2.scenePos()
#         self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
#
#     def detach(self):
#         self.n1.remove_line(self)
#         self.n2.remove_line(self)
#
#
# # -------------------------
# # Main View
# # -------------------------
# class GridLineEditor(QGraphicsView):
#     def __init__(self, grid_size=25):
#         super().__init__()
#         self.grid_size = grid_size
#
#         self.setScene(QGraphicsScene(self))
#         self.scene().setSceneRect(QRectF(-3000, -3000, 6000, 6000))
#
#         self.setRenderHint(QPainter.Antialiasing, True)
#         self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
#         self.setDragMode(QGraphicsView.RubberBandDrag)
#
#         # Pens
#         self.line_pen = QPen(Qt.black, 2)
#         self.preview_pen = QPen(Qt.black, 1, Qt.DashLine)
#
#         # Snapping
#         self.snap_grid_enabled = True
#         self.snap_vertex_enabled = True
#         self.vertex_snap_px = 14  # snap distance (pixels)
#
#         # Drawing state
#         self._drawing = False
#         self._start_node = None
#         self._preview_line = None
#         self._preview_end_node = None
#
#         # Pan support (middle mouse)
#         self._panning = False
#         self._pan_start = None
#
#     # ----- coordinate snapping -----
#     def vertex_snap_distance_scene2(self) -> float:
#         # Convert pixel threshold to scene units using current transform scale
#         # (approx: 1 px in view corresponds to 1/scale scene units)
#         scale = self.transform().m11() if self.transform().m11() != 0 else 1.0
#         d_scene = self.vertex_snap_px / scale
#         return d_scene * d_scene
#
#     def find_nearest_node(self, p_scene: QPointF):
#         d2_thr = self.vertex_snap_distance_scene2()
#         best = None
#         best_d2 = float("inf")
#         for item in self.scene().items():
#             if isinstance(item, NodeItem):
#                 d2 = dist2(item.scenePos(), p_scene)
#                 if d2 < best_d2 and d2 <= d2_thr:
#                     best_d2 = d2
#                     best = item
#         return best
#
#     def snap_point(
#         self, start: QPointF | None, p_scene: QPointF, mods: Qt.KeyboardModifiers
#     ) -> QPointF:
#         p = QPointF(p_scene)
#
#         # Constraints first (work on free point), then snap
#         if start is not None:
#             if mods & Qt.ControlModifier:
#                 p = constrain_orthogonal(start, p)
#             elif mods & Qt.ShiftModifier:
#                 p = snap_angle(start, p, 45.0)
#
#         # Grid snap
#         if self.snap_grid_enabled:
#             p = snap_to_grid(p, self.grid_size)
#
#         # Vertex snap (to existing node)
#         if self.snap_vertex_enabled:
#             node = self.find_nearest_node(p)
#             if node is not None:
#                 p = node.scenePos()
#
#         return p
#
#     def get_or_create_node(self, p_scene: QPointF) -> NodeItem:
#         # If snapping is on and a node is close, reuse it
#         if self.snap_vertex_enabled:
#             n = self.find_nearest_node(p_scene)
#             if n is not None:
#                 return n
#         n = NodeItem(p_scene, radius=5.0)
#         self.scene().addItem(n)
#         return n
#
#     # ----- background grid -----
#     def drawBackground(self, painter: QPainter, rect: QRectF):
#         super().drawBackground(painter, rect)
#         g = self.grid_size
#
#         # minor grid
#         painter.setPen(QPen(Qt.lightGray, 1))
#         left = int(rect.left()) - (int(rect.left()) % g)
#         top = int(rect.top()) - (int(rect.top()) % g)
#
#         x = left
#         while x < rect.right():
#             painter.drawLine(x, rect.top(), x, rect.bottom())
#             x += g
#
#         y = top
#         while y < rect.bottom():
#             painter.drawLine(rect.left(), y, rect.right(), y)
#             y += g
#
#         # major grid every 5 cells
#         major = g * 5
#         painter.setPen(QPen(Qt.gray, 1))
#         leftM = int(rect.left()) - (int(rect.left()) % major)
#         topM = int(rect.top()) - (int(rect.top()) % major)
#
#         x = leftM
#         while x < rect.right():
#             painter.drawLine(x, rect.top(), x, rect.bottom())
#             x += major
#
#         y = topM
#         while y < rect.bottom():
#             painter.drawLine(rect.left(), y, rect.right(), y)
#             y += major
#
#     # ----- interaction -----
#     def mousePressEvent(self, event):
#         # Middle mouse = pan
#         if event.button() == Qt.MiddleButton:
#             self._panning = True
#             self._pan_start = event.pos()
#             self.setCursor(Qt.ClosedHandCursor)
#             event.accept()
#             return
#
#         # Alt + Left = start drawing
#         if event.button() == Qt.LeftButton and (event.modifiers() & Qt.AltModifier):
#             raw = self.mapToScene(event.pos())
#             p0 = self.snap_point(None, raw, event.modifiers())
#             self._start_node = self.get_or_create_node(p0)
#
#             self._preview_line = QGraphicsLineItem()
#             self._preview_line.setPen(self.preview_pen)
#             self.scene().addItem(self._preview_line)
#
#             # Preview end node
#             self._preview_end_node = NodeItem(self._start_node.scenePos(), radius=4.0)
#             self._preview_end_node.setBrush(Qt.white)
#             self._preview_end_node.setPen(QPen(Qt.black, 1, Qt.DashLine))
#             self._preview_end_node.setFlags(
#                 QGraphicsEllipseItem.GraphicsItemFlag(0)
#             )  # not selectable/movable
#             self.scene().addItem(self._preview_end_node)
#
#             self._drawing = True
#             event.accept()
#             return
#
#         super().mousePressEvent(event)
#
#     def mouseMoveEvent(self, event):
#         if self._panning and self._pan_start is not None:
#             delta = event.pos() - self._pan_start
#             self._pan_start = event.pos()
#             self.horizontalScrollBar().setValue(
#                 self.horizontalScrollBar().value() - delta.x()
#             )
#             self.verticalScrollBar().setValue(
#                 self.verticalScrollBar().value() - delta.y()
#             )
#             event.accept()
#             return
#
#         if (
#             self._drawing
#             and self._start_node is not None
#             and self._preview_line is not None
#         ):
#             raw = self.mapToScene(event.pos())
#             start = self._start_node.scenePos()
#             end = self.snap_point(start, raw, event.modifiers())
#
#             self._preview_line.setLine(start.x(), start.y(), end.x(), end.y())
#             if self._preview_end_node is not None:
#                 self._preview_end_node.setPos(end)
#             event.accept()
#             return
#
#         super().mouseMoveEvent(event)
#
#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.MiddleButton and self._panning:
#             self._panning = False
#             self._pan_start = None
#             self.setCursor(Qt.ArrowCursor)
#             event.accept()
#             return
#
#         if event.button() == Qt.LeftButton and self._drawing:
#             # Commit final edge
#             line = self._preview_line.line()
#             p_end = QPointF(line.x2(), line.y2())
#
#             # Cleanup preview items
#             self.scene().removeItem(self._preview_line)
#             self._preview_line = None
#             if self._preview_end_node is not None:
#                 self.scene().removeItem(self._preview_end_node)
#                 self._preview_end_node = None
#
#             end_node = self.get_or_create_node(p_end)
#
#             # Avoid zero-length edges
#             if dist2(self._start_node.scenePos(), end_node.scenePos()) > 1e-9:
#                 edge = EdgeItem(self._start_node, end_node, self.line_pen)
#                 self.scene().addItem(edge)
#
#             self._start_node = None
#             self._drawing = False
#             event.accept()
#             return
#
#         super().mouseReleaseEvent(event)
#
#     def keyPressEvent(self, event):
#         # Delete key removes selected items
#         if event.matches(QKeySequence.Delete) or event.key() == Qt.Key_Delete:
#             self.delete_selected()
#             event.accept()
#             return
#         super().keyPressEvent(event)
#
#     def delete_selected(self):
#         selected = self.scene().selectedItems()
#
#         # If a node is deleted, also delete connected edges
#         for item in selected:
#             if isinstance(item, NodeItem):
#                 # remove edges first
#                 for ln in list(item.lines):
#                     ln.detach()
#                     self.scene().removeItem(ln)
#                 self.scene().removeItem(item)
#
#         # Delete any selected edges
#         for item in selected:
#             if isinstance(item, EdgeItem):
#                 item.detach()
#                 self.scene().removeItem(item)
#
#
# # -------------------------
# # Run
# # -------------------------
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     view = GridLineEditor(grid_size=25)
#     view.setWindowTitle("Grid + Draw Lines + Grid/Vertex/Angle/Ortho Snapping")
#     view.resize(1000, 650)
#     view.show()
#     sys.exit(app.exec())
