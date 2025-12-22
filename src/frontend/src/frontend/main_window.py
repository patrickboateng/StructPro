from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QWidget,
    QSizePolicy,
)

from . import resources_rc

from .editor import Editor
from .dialog import GridLinesDialog
from .settings import save_settings


# from .command_line_interface import CommandLineInterface


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("StructPro")

        self.select_mode_action = QAction(QIcon(":/misc/select"), "Select",
                                          self)

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
        self.bottom_toolbar.addWidget(spacer)

        self.add_select_mode_action_2_toolbar()
        self.add_file_menu()
        self.add_edit_menu()
        self.add_view_menu()
        self.add_define_menu()
        self.add_draw_menu()
        self.add_assign_menu()
        self.add_analyze_menu()
        self.add_display_menu()
        self.add_help_menu()

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_toolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.left_toolbar)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.bottom_toolbar)

        self.gridlines_dialog = GridLinesDialog(self)

        self.editor = Editor(self)
        self.setCentralWidget(self.editor)

    def create_grid_lines_dialog(self):
        self.gridlines_dialog.exec()

    def zoom_in(self):
        self.editor.scale(1.2, 1.2)

    def zoom_out(self):
        self.editor.scale(0.8, 0.8)

    def zoom_fit(self):
        self.editor.fitInView()

    def on_select_mode_action_clicked(self):
        self.draw_node_action.setChecked(False)
        self.draw_member_action.setChecked(False)
        self.select_mode_action.setChecked(True)

    def on_draw_node_action_clicked(self):
        self.select_mode_action.setChecked(False)
        self.draw_member_action.setChecked(False)
        self.draw_node_action.setChecked(True)

    def on_draw_member_action_clicked(self):
        self.draw_node_action.setChecked(False)
        self.select_mode_action.setChecked(False)
        self.draw_member_action.setChecked(True)

    def on_zoom_in_action_clicked(self):
        self.zoom_in()

    def on_zoom_out_action_clicked(self):
        self.zoom_out()

    def on_zoom_fit_action_clicked(self):
        self.zoom_fit()

    def add_select_mode_action_2_toolbar(self):
        self.select_mode_action.setCheckable(True)
        self.select_mode_action.setChecked(True)
        self.select_mode_action.triggered.connect(
            self.on_select_mode_action_clicked)
        self.left_toolbar.addAction(self.select_mode_action)
        self.left_toolbar.addSeparator()

    def add_file_menu(self):
        new_action = QAction(QIcon(":/file/new"), "New", self)
        new_action.setToolTip("<b>New</b><br>Creates a new document")
        new_action.setShortcut(QKeySequence.StandardKey.New)

        open_action = QAction(QIcon(":/file/open"), "Open", self)
        open_action.setToolTip("<b>Open</b><br>Open an existing document")
        open_action.setShortcut(QKeySequence.StandardKey.Open)

        save_action = QAction(QIcon(":/file/save"), "Save", self)
        save_action.setToolTip("<b>Save</b><br>Save document")
        save_action.setShortcut(QKeySequence.StandardKey.Save)

        save_as_action = QAction(QIcon(":/file/save_as"), "Save As", self)
        save_as_action.setToolTip(
            "<b>Save As</b><br>Save document under a new name")
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

        exit_action = QAction(QIcon(":/misc/close"), "Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)

        filemenu = self.menubar.addMenu("File")
        filemenu.addAction(new_action)
        filemenu.addAction(open_action)
        filemenu.addSeparator()
        filemenu.addAction(save_action)
        filemenu.addAction(save_as_action)
        filemenu.addSeparator()
        filemenu.addAction(exit_action)

        self.top_toolbar.addAction(new_action)
        self.top_toolbar.addAction(open_action)
        self.top_toolbar.addAction(save_action)
        self.top_toolbar.addSeparator()

    def add_edit_menu(self):
        undo_action = QAction(QIcon(":/edit/undo"), "Undo", self)
        undo_action.setToolTip("<b>Undo</b><br>Undo last action")
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)

        redo_action = QAction(QIcon(":/edit/redo"), "Redo", self)
        tip = "<b>Redo</b><br>Do again the last undone action"
        redo_action.setToolTip(tip)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        editmenu = self.menubar.addMenu("Edit")
        editmenu.addAction(undo_action)
        editmenu.addAction(redo_action)

        self.top_toolbar.addAction(undo_action)
        self.top_toolbar.addAction(redo_action)
        self.top_toolbar.addSeparator()

    def add_view_menu(self):
        show_grid_action = QAction(QIcon(":/view/show_grid"), "Show Grid",
                                   self)
        show_grid_action.setToolTip("<b>Show Grid</b><br>Make grid visible")
        show_grid_action.setCheckable(True)
        show_grid_action.setChecked(True)

        edit_grid_action = QAction(QIcon(":/view/edit_grid"), "Edit Grid",
                                   self)
        edit_grid_action.setToolTip("<b>Grid Data</b><br>Edit grid data")
        edit_grid_action.triggered.connect(self.create_grid_lines_dialog)

        grid_snap_action = QAction(QIcon(":/view/grid_snap"), "Grid Snap",
                                   self)
        grid_snap_action.setCheckable(True)
        grid_snap_action.setChecked(True)
        grid_snap_action.setToolTip("<b>Grid Snap</b><br>Snap to nearest grid")

        show_axis_action = QAction(QIcon(":/view/diagram"), "Show Axis", self)
        show_axis_action.setCheckable(True)
        show_axis_action.setChecked(True)
        tip = "<b>Show Axes</b><br>Display coordinate origin"
        show_axis_action.setToolTip(tip)
        show_axis_action.setStatusTip("Display coordinate origin")

        zoom_in_action = QAction(QIcon(":/view/zoom-in"), "Zoom In", self)
        zoom_in_action.setToolTip("Zoom In")
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)

        zoom_out_action = QAction(QIcon(":/view/zoom-out"), "Zoom Out", self)
        zoom_out_action.setToolTip("Zoom Out")
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)

        zoom_fit_action = QAction(QIcon(":/view/zoom-fit"), "Zoom Fit", self)
        zoom_fit_action.setToolTip("Zoom Fit")
        zoom_fit_action.triggered.connect(self.zoom_fit)

        refresh_view_action = QAction(
            QIcon(":/view/refresh_view"), "Refresh View", self
        )
        refresh_view_action.setToolTip("Refresh window")

        viewmenu = self.menubar.addMenu("View")
        viewmenu.addAction(show_grid_action)
        viewmenu.addAction(edit_grid_action)
        viewmenu.addAction(grid_snap_action)
        viewmenu.addAction(show_axis_action)
        viewmenu.addSeparator()
        viewmenu.addAction(zoom_in_action)
        viewmenu.addAction(zoom_out_action)
        viewmenu.addAction(zoom_fit_action)
        viewmenu.addSeparator()
        viewmenu.addAction(refresh_view_action)

        self.top_toolbar.addAction(zoom_in_action)
        self.top_toolbar.addAction(zoom_out_action)
        self.top_toolbar.addAction(zoom_fit_action)
        self.top_toolbar.addSeparator()

        self.bottom_toolbar.addAction(show_axis_action)
        self.bottom_toolbar.addAction(edit_grid_action)
        self.bottom_toolbar.addAction(show_grid_action)
        self.bottom_toolbar.addAction(grid_snap_action)
        self.bottom_toolbar.addSeparator()

    def add_define_menu(self):
        material_action = QAction(QIcon(":/define/material"), "Material", self)
        material_action.setToolTip("Define material")

        section_action = QAction(QIcon(":/define/section"), "Section", self)
        section_action.setToolTip("Define section")

        node_action = QAction(QIcon(":/define/node"), "Node", self)
        node_action.setToolTip("Define node/joint")

        member_action = QAction(QIcon(":/define/member"), "Member", self)
        member_action.setToolTip("Define member")

        definemenu = self.menubar.addMenu("Define")
        definemenu.addAction(material_action)
        definemenu.addAction(section_action)
        definemenu.addSeparator()
        definemenu.addAction(node_action)
        definemenu.addAction(member_action)

        self.top_toolbar.addAction(material_action)
        self.top_toolbar.addAction(section_action)
        self.top_toolbar.addAction(node_action)
        self.top_toolbar.addAction(member_action)
        self.top_toolbar.addSeparator()

    def add_draw_menu(self):
        self.draw_node_action = QAction(QIcon(":/draw/draw_node"), "Draw Node",
                                        self)
        self.draw_node_action.setCheckable(True)
        self.draw_node_action.setToolTip("Draw node")
        self.draw_node_action.triggered.connect(
            self.on_draw_node_action_clicked)

        self.draw_member_action = QAction(
            QIcon(":/draw/draw_member"), "Draw member", self
        )
        self.draw_member_action.setCheckable(True)
        self.draw_member_action.setToolTip("Draw member")
        self.draw_member_action.triggered.connect(
            self.on_draw_member_action_clicked)

        drawmenu = self.menubar.addMenu("Draw")
        drawmenu.addAction(self.draw_node_action)
        drawmenu.addAction(self.draw_member_action)

        self.left_toolbar.addAction(self.draw_node_action)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(self.draw_member_action)

    def add_assign_menu(self):
        joint_loads_action = QAction(QIcon(":/assign/joint_loads"),
                                     "Joint loads", self)
        member_loads_action = QAction(
            QIcon(":/assign/member_loads"), "Member loads", self
        )

        assignmenu = self.menubar.addMenu("Assign")
        assignmenu.addAction(joint_loads_action)
        assignmenu.addAction(member_loads_action)

        self.top_toolbar.addAction(joint_loads_action)
        self.top_toolbar.addAction(member_loads_action)
        self.top_toolbar.addSeparator()

    def add_analyze_menu(self):
        run_static_analysis_action = QAction(
            QIcon(":/analyze/run"), "Run Static Analysis", self
        )

        analyzemenu = self.menubar.addMenu("Analyze")
        analyzemenu.addAction(run_static_analysis_action)

        self.top_toolbar.addAction(run_static_analysis_action)
        self.top_toolbar.addSeparator()

    def add_display_menu(self):
        redraw_structure_action = QAction(
            QIcon(":/display/redraw_structure"), "Draw undeformed structure",
            self
        )
        shear_force_action = QAction(
            QIcon(":/display/shear_force"), "Draw shear force diagram", self
        )
        bending_moment_action = QAction(
            QIcon(":/display/bending_moment"), "Draw bending moment diagram",
            self
        )
        deflection_action = QAction(
            QIcon(":/display/deflection"), "Draw deflected shape", self
        )
        reactions_action = QAction(QIcon(":/display/reactions"),
                                   "Draw reactions", self)

        displaymenu = self.menubar.addMenu("Display")
        displaymenu.addAction(redraw_structure_action)
        displaymenu.addSeparator()
        displaymenu.addAction(shear_force_action)
        displaymenu.addAction(bending_moment_action)
        displaymenu.addAction(deflection_action)
        displaymenu.addAction(reactions_action)

        self.top_toolbar.addAction(redraw_structure_action)
        self.top_toolbar.addAction(shear_force_action)
        self.top_toolbar.addAction(bending_moment_action)
        self.top_toolbar.addAction(deflection_action)
        self.top_toolbar.addAction(reactions_action)
        self.top_toolbar.addSeparator()

    def add_help_menu(self):
        quick_intro_action = QAction(
            QIcon(":/help/quick_intro"), "Quick Introduction", self
        )
        license_info_action = QAction(
            QIcon(":/help/license"), "License Information", self
        )
        check_updates_action = QAction(
            QIcon(":/help/check_update"), "Check for Updates ...", self
        )
        about_action = QAction(QIcon(":/help/about"), "About", self)

        helpmenu = self.menubar.addMenu("Help")
        helpmenu.addAction(quick_intro_action)
        helpmenu.addSeparator()
        helpmenu.addAction(license_info_action)
        helpmenu.addSeparator()
        helpmenu.addAction(check_updates_action)
        helpmenu.addSeparator()
        helpmenu.addAction(about_action)

    def closeEvent(self, event):
        save_settings()
        event.accept()
