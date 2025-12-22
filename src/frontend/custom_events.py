from PySide6.QtCore import QEvent

GRID_UPDATED_EVENT = QEvent.Type(QEvent.registerEventType())


class GridUpdatedEvent(QEvent):
    def __init__(self, grid):
        super().__init__(GRID_UPDATED_EVENT)

        self.grid = grid
