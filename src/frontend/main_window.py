import math
from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QIcon,
    QKeySequence,
    QUndoCommand,
    QUndoStack,
)
from PySide6.QtWidgets import (
    QDockWidget,
    QGraphicsItem,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QUndoView,
    QWidget,
    QTabWidget,
    QComboBox,
)

from . import resources_rc

from .dialog import GridSpacingDialog
from .editor import Editor, Scene, SceneDrawMode


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

        self.setText(str(graphics_item))

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

    def undo(self):
        for graphics_item in self.selected_graphics_item:
            self.scene.addItem(graphics_item)
            self.scene.update()

    def redo(self):
        for graphics_item in self.selected_graphics_item:
            self.scene.removeItem(graphics_item)
            self.scene.update()


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("StructPro")

        self.undo_stack = QUndoStack(self)

        self.editor = Editor(self)
        self.editor.scene_pos_changed.connect(self.update_coord_display_label)
        self.editor.scene().graphics_item_created.connect(
            self.add_graphics_item)

        self.grid_spacing_dialog = GridSpacingDialog(self)
        self.grid_spacing_dialog.grid_spacing_changed.connect(
            self.editor.set_grid_size)

        self.select_mode_action = QAction(QIcon(":/misc/select"), "Select",
                                          self)
        self.select_mode_action.setCheckable(True)
        self.select_mode_action.setChecked(True)
        self.select_mode_action.setData(SceneDrawMode.SELECT_MODE)

        self.coord_display_label = QLabel("X: - Y: -")
        self.coord_display_label.setContentsMargins(28, 0, 0, 0)

        self.menubar = self.menuBar()

        toolbar_icon_size = QSize(16, 16)
        self.top_toolbar = QToolBar()
        self.top_toolbar.setMovable(False)
        self.top_toolbar.setIconSize(toolbar_icon_size)

        self.left_toolbar = QToolBar(self)
        self.left_toolbar.setIconSize(toolbar_icon_size)
        self.left_toolbar.setMovable(False)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.bottom_toolbar = QToolBar()
        self.bottom_toolbar.setIconSize(QSize(20, 20))
        self.bottom_toolbar.setMovable(False)
        self.bottom_toolbar.addWidget(self.coord_display_label)
        self.bottom_toolbar.addWidget(spacer)

        self._create_file_menu_actions()
        self._add_file_menu()

        self._create_edit_menu_actions()
        self._add_edit_menu()

        self._create_view_menu_actions()
        self._add_view_menu()

        self._create_define_menu_actions()
        self._add_define_menu()

        self._create_draw_menu_actions()
        self._add_draw_menu()

        self._create_assign_menu_actions()
        self._add_assign_menu()

        self._create_analyze_menu_actions()
        self._add_analyze_menu()

        self._create_display_menu_actions()
        self._add_display_menu()

        self._create_help_menu_actions()
        self._add_help_menu()

        self.workbench_mode = QComboBox()
        self.workbench_mode.setEditable(False)
        self.workbench_mode.setInsertPolicy(QComboBox.NoInsert)
        self.workbench_mode.addItem("2D")

        # ADD FILE MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.new_action)
        self.top_toolbar.addAction(self.open_action)
        self.top_toolbar.addAction(self.save_action)
        self.top_toolbar.addSeparator()

        # ADD EDIT MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.undo_action)
        self.top_toolbar.addAction(self.redo_action)
        self.top_toolbar.addSeparator()

        # ADD VIEW MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.zoom_in_action)
        self.top_toolbar.addAction(self.zoom_out_action)
        self.top_toolbar.addAction(self.zoom_fit_action)
        self.top_toolbar.addSeparator()

        # ADD VIEW MENU ITEMS TO BOTTOM TOOLBAR
        self.bottom_toolbar.addAction(self.show_axis_action)
        self.bottom_toolbar.addAction(self.edit_grid_action)
        self.bottom_toolbar.addAction(self.show_grid_action)
        self.bottom_toolbar.addAction(self.grid_snap_action)
        self.bottom_toolbar.addSeparator()

        # ADD DEFINE MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.material_action)
        self.top_toolbar.addAction(self.section_action)
        self.top_toolbar.addSeparator()

        # ADD SELECT MODE ACTION TO LEFT TOOLBAR
        self.left_toolbar.addAction(self.select_mode_action)
        self.left_toolbar.addSeparator()

        # ADD DRAW MENU ITEMS TO LEFT TOOLBAR
        self.left_toolbar.addAction(self.draw_node_action)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(self.draw_member_action)

        # ADD ASSIGN MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.joint_loads_action)
        self.top_toolbar.addAction(self.member_loads_action)
        self.top_toolbar.addSeparator()

        # ADD ANALYZE MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.run_static_analysis_action)
        self.top_toolbar.addSeparator()

        # ADD DISPLAY MENU ITEMS TO TOP TOOLBAR
        self.top_toolbar.addAction(self.redraw_structure_action)
        self.top_toolbar.addAction(self.shear_force_diagram_action)
        self.top_toolbar.addAction(self.bending_moment_diagram_action)
        self.top_toolbar.addAction(self.deflection_diagram_action)
        self.top_toolbar.addAction(self.reactions_diagram_action)
        self.top_toolbar.addSeparator()

        # ADD WORKBENCH MODE TO TOP TOOLBAR
        self.top_toolbar.addWidget(self.workbench_mode)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_toolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.left_toolbar)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.bottom_toolbar)

        self.create_side_panel()

        self.setCentralWidget(self.editor)

    def add_graphics_item(self, scene: Scene, graphics_item: QGraphicsItem):
        self.undo_stack.push(AddCommand(scene, graphics_item))

    def delete_graphics_item(self):
        self.undo_stack.push(DeleteCommand(self.editor.scene()))

    def create_side_panel(self):
        side_panel_dock_widget = QDockWidget(self)
        side_panel_dock_widget.setTitleBarWidget(QWidget())
        side_panel_dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        side_panel_dock_widget.setFeatures(QDockWidget.DockWidgetClosable)
        side_panel_dock_widget.setMaximumWidth(400)

        commnad_history_view = QUndoView(self.undo_stack)

        model_explorer = QWidget()

        side_panel_tab_widget = QTabWidget()
        side_panel_tab_widget.setTabsClosable(True)
        side_panel_tab_widget.setMovable(True)
        side_panel_tab_widget.setUsesScrollButtons(True)
        side_panel_tab_widget.setDocumentMode(True)
        side_panel_tab_widget.setTabShape(QTabWidget.Rounded)
        side_panel_tab_widget.setElideMode(Qt.ElideRight)
        side_panel_tab_widget.addTab(model_explorer, "Model Explorer")
        side_panel_tab_widget.addTab(commnad_history_view, "Command History")

        side_panel_dock_widget.setWidget(side_panel_tab_widget)

        self.addDockWidget(Qt.RightDockWidgetArea, side_panel_dock_widget)

    def update_coord_display_label(self, x, y):
        self.coord_display_label.setText(f"X: {x :.3f}, Y: {y:.3f}")

    def show_grid_lines_dialog(self):
        self.grid_spacing_dialog.exec()

    def on_zoom_in_action_clicked(self):
        self.editor.zoom_in()

    def on_zoom_out_action_clicked(self):
        self.editor.zoom_out()

    def on_zoom_fit_action_clicked(self):
        self.editor.zoom_fit()

    def _create_file_menu_actions(self):
        self.new_action = QAction(QIcon(":/file/new"), "New", self)
        self.new_action.setToolTip("<b>New</b><br>Creates a new document")
        self.new_action.setShortcut(QKeySequence.StandardKey.New)

        self.open_action = QAction(QIcon(":/file/open"), "Open", self)
        self.open_action.setToolTip("<b>Open</b><br>Open an existing document")
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)

        self.save_action = QAction(QIcon(":/file/save"), "Save", self)
        self.save_action.setToolTip("<b>Save</b><br>Save document")
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)

        self.save_as_action = QAction(QIcon(":/file/save_as"), "Save As", self)
        self.save_as_action.setToolTip(
            "<b>Save As</b><br>Save document under a new name"
        )
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

        self.exit_action = QAction(QIcon(":/misc/close"), "Exit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)

    def _add_file_menu(self):
        filemenu = self.menubar.addMenu("File")
        filemenu.addAction(self.new_action)
        filemenu.addAction(self.open_action)
        filemenu.addSeparator()
        filemenu.addAction(self.save_action)
        filemenu.addAction(self.save_as_action)
        filemenu.addSeparator()
        filemenu.addAction(self.exit_action)

    def _create_edit_menu_actions(self):
        self.undo_action = self.undo_stack.createUndoAction(self,
                                                            self.tr("&Undo"))
        self.undo_action.setIcon(QIcon(":/edit/undo"))
        self.undo_action.setToolTip("<b>Undo</b><br>Undo last action")
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)

        self.redo_action = self.undo_stack.createRedoAction(self,
                                                            self.tr("&Redo"))
        self.redo_action.setIcon(QIcon(":/edit/redo"))
        tip = "<b>Redo</b><br>Do again the last undone action"
        self.redo_action.setToolTip(tip)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        self.delete_action = QAction(QIcon(":/edit/delete"), "Delete", self)
        self.delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        self.delete_action.triggered.connect(self.delete_graphics_item)

    def _add_edit_menu(self):
        editmenu = self.menubar.addMenu("Edit")
        editmenu.addAction(self.undo_action)
        editmenu.addAction(self.redo_action)
        editmenu.addAction(self.delete_action)

    def _create_view_menu_actions(self):
        self.show_grid_action = QAction(QIcon(":/view/show_grid"), "Show Grid",
                                        self)
        self.show_grid_action.setToolTip(
            "<b>Show Grid</b><br>Make grid visible")
        self.show_grid_action.setCheckable(True)
        self.show_grid_action.setChecked(True)

        self.edit_grid_action = QAction(QIcon(":/view/edit_grid"), "Edit Grid",
                                        self)
        self.edit_grid_action.setToolTip("<b>Grid Data</b><br>Edit grid data")
        self.edit_grid_action.triggered.connect(self.show_grid_lines_dialog)

        self.grid_snap_action = QAction(QIcon(":/view/grid_snap"), "Grid Snap",
                                        self)
        self.grid_snap_action.setCheckable(True)
        self.grid_snap_action.setChecked(True)
        self.grid_snap_action.setToolTip(
            "<b>Grid Snap</b><br>Snap to nearest grid")
        self.grid_snap_action.triggered.connect(self.editor.set_snap_enabled)

        self.show_axis_action = QAction(QIcon(":/view/diagram"), "Show Axis",
                                        self)
        self.show_axis_action.setCheckable(True)
        self.show_axis_action.setChecked(True)
        tip = "<b>Show Axes</b><br>Display coordinate origin"
        self.show_axis_action.setToolTip(tip)
        self.show_axis_action.setStatusTip("Display coordinate origin")

        self.zoom_in_action = QAction(QIcon(":/view/zoom-in"), "Zoom In", self)
        self.zoom_in_action.setToolTip("Zoom In")
        self.zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        self.zoom_in_action.triggered.connect(self.on_zoom_in_action_clicked)

        self.zoom_out_action = QAction(QIcon(":/view/zoom-out"), "Zoom Out",
                                       self)
        self.zoom_out_action.setToolTip("Zoom Out")
        self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        self.zoom_out_action.triggered.connect(self.on_zoom_out_action_clicked)

        self.zoom_fit_action = QAction(QIcon(":/view/zoom-fit"), "Zoom Fit",
                                       self)
        self.zoom_fit_action.setToolTip("Zoom Fit")
        self.zoom_fit_action.triggered.connect(self.on_zoom_fit_action_clicked)

        self.refresh_view_action = QAction(
            QIcon(":/view/refresh_view"), "Refresh View", self
        )
        self.refresh_view_action.setToolTip("Refresh window")

    def _add_view_menu(self):
        viewmenu = self.menubar.addMenu("View")
        viewmenu.addAction(self.show_grid_action)
        viewmenu.addAction(self.edit_grid_action)
        viewmenu.addAction(self.grid_snap_action)
        viewmenu.addAction(self.show_axis_action)
        viewmenu.addSeparator()
        viewmenu.addAction(self.zoom_in_action)
        viewmenu.addAction(self.zoom_out_action)
        viewmenu.addAction(self.zoom_fit_action)
        viewmenu.addSeparator()
        viewmenu.addAction(self.refresh_view_action)

    def _create_define_menu_actions(self):
        self.material_action = QAction(QIcon(":/define/material"), "Material",
                                       self)
        self.material_action.setToolTip("Define material")

        self.section_action = QAction(QIcon(":/define/section"), "Section",
                                      self)
        self.section_action.setToolTip("Define section")

    def _add_define_menu(self):
        definemenu = self.menubar.addMenu("Define")
        definemenu.addAction(self.material_action)
        definemenu.addAction(self.section_action)

    def _create_draw_menu_actions(self):
        self.draw_node_action = QAction(
            QIcon(":/draw/draw_node"),
            "Draw Node",
            self,
        )
        self.draw_node_action.setCheckable(True)
        self.draw_node_action.setToolTip("Draw node")
        self.draw_node_action.setData(SceneDrawMode.DRAW_NODE_MODE)

        self.draw_member_action = QAction(
            QIcon(":/draw/draw_member"), "Draw member", self
        )
        self.draw_member_action.setCheckable(True)
        self.draw_member_action.setToolTip("Draw member")
        self.draw_member_action.setData(SceneDrawMode.DRAW_MEMBER_MODE)

        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        action_group.addAction(self.select_mode_action)
        action_group.addAction(self.draw_node_action)
        action_group.addAction(self.draw_member_action)
        action_group.triggered.connect(
            lambda action: self.editor.set_tool_mode(action.data())
        )

    def _add_draw_menu(self):
        drawmenu = self.menubar.addMenu("Draw")
        drawmenu.addAction(self.draw_node_action)
        drawmenu.addAction(self.draw_member_action)

    def _create_assign_menu_actions(self):
        self.joint_loads_action = QAction(
            QIcon(":/assign/joint_loads"), "Assign Joint loads", self
        )
        self.member_loads_action = QAction(
            QIcon(":/assign/member_loads"), "Assign Member loads", self
        )

    def _add_assign_menu(self):
        assignmenu = self.menubar.addMenu("Assign")
        assignmenu.addAction(self.joint_loads_action)
        assignmenu.addAction(self.member_loads_action)

    def _create_analyze_menu_actions(self):
        # ADD ANALYZE MENU
        self.run_static_analysis_action = QAction(
            QIcon(":/analyze/run"), "Run Static Analysis", self
        )

    def _add_analyze_menu(self):
        analyzemenu = self.menubar.addMenu("Analyze")
        analyzemenu.addAction(self.run_static_analysis_action)

    def _create_display_menu_actions(self):
        self.redraw_structure_action = QAction(
            QIcon(":/display/redraw_structure"), "Draw undeformed structure",
            self
        )
        self.shear_force_diagram_action = QAction(
            QIcon(":/display/shear_force"), "Draw shear force diagram", self
        )
        self.bending_moment_diagram_action = QAction(
            QIcon(":/display/bending_moment"), "Draw bending moment diagram",
            self
        )
        self.deflection_diagram_action = QAction(
            QIcon(":/display/deflection"), "Draw deflected shape", self
        )
        self.reactions_diagram_action = QAction(
            QIcon(":/display/reactions"), "Draw reactions", self
        )

    def _add_display_menu(self):
        displaymenu = self.menubar.addMenu("Display")
        displaymenu.addAction(self.redraw_structure_action)
        displaymenu.addSeparator()
        displaymenu.addAction(self.shear_force_diagram_action)
        displaymenu.addAction(self.bending_moment_diagram_action)
        displaymenu.addAction(self.deflection_diagram_action)
        displaymenu.addAction(self.reactions_diagram_action)

    def _create_help_menu_actions(self):
        self.quick_intro_action = QAction(
            QIcon(":/help/quick_intro"), "Quick Introduction", self
        )
        self.license_info_action = QAction(
            QIcon(":/help/license"), "License Information", self
        )
        self.check_updates_action = QAction(
            QIcon(":/help/check_update"), "Check for Updates ...", self
        )
        self.about_action = QAction(QIcon(":/help/about"), "About", self)

    def _add_help_menu(self):
        helpmenu = self.menubar.addMenu("Help")
        helpmenu.addAction(self.quick_intro_action)
        helpmenu.addSeparator()
        helpmenu.addAction(self.license_info_action)
        helpmenu.addSeparator()
        helpmenu.addAction(self.check_updates_action)
        helpmenu.addSeparator()
        helpmenu.addAction(self.about_action)
