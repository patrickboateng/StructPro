from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QToolBar, QWidget, QSizePolicy

import resources_rc


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("StructPro")

        self.select_mode_action = QAction(QIcon(":/misc/select.svg"), "Select",
                                          self)
        self.select_mode_action.setCheckable(True)
        self.select_mode_action.setChecked(True)
        self.select_mode_action.triggered.connect(
            self.select_mode_action_clicked)

        self.menubar = self.menuBar()

        toolbar_icon_size = QSize(16, 16)
        self.top_toolbar = QToolBar()
        self.top_toolbar.setMovable(False)
        self.top_toolbar.setIconSize(toolbar_icon_size)

        self.left_toolbar = QToolBar(self)
        self.left_toolbar.setIconSize(toolbar_icon_size)
        self.left_toolbar.setMovable(False)
        self.left_toolbar.addAction(self.select_mode_action)
        self.left_toolbar.addSeparator()

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.bottom_toolbar = QToolBar()
        self.bottom_toolbar.setIconSize(toolbar_icon_size)
        self.bottom_toolbar.setMovable(False)
        self.bottom_toolbar.addWidget(spacer)

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

    def select_mode_action_clicked(self):
        self.select_mode_action.setChecked(True)

    def draw_node_action_clicked(self):
        self.select_mode_action.setChecked(False)

    def draw_member_action_clicked(self):
        self.select_mode_action.setChecked(False)

    def add_file_menu(self):
        new_action = QAction(QIcon(":/file/new.svg"), "New", self)
        new_action.setToolTip("<b>New</b><br>Creates a new document")
        new_action.setShortcut(QKeySequence.StandardKey.New)

        open_action = QAction(QIcon(":/file/open.svg"), "Open", self)
        open_action.setToolTip("<b>Open</b><br>Open an existing document")
        open_action.setShortcut(QKeySequence.StandardKey.Open)

        save_action = QAction(QIcon(":/file/save.svg"), "Save", self)
        save_action.setToolTip("<b>Save</b><br>Save document")
        save_action.setShortcut(QKeySequence.StandardKey.Save)

        save_as_action = QAction(QIcon(":/file/save_as.svg"), "Save As", self)
        save_as_action.setToolTip(
            "<b>Save As</b><br>Save document under a new name")
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

        exit_action = QAction(QIcon(":/file/exit.svg"), "Exit", self)
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
        undo_action = QAction(QIcon(":/edit/undo.svg"), "Undo", self)
        undo_action.setToolTip("<b>Undo</b><br>Undo last action")
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)

        redo_action = QAction(QIcon(":/edit/redo.svg"), "Redo", self)
        tip = "<b>Redo</b><br>Do again the last undone action"
        redo_action.setToolTip(tip)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        editmenu = self.menubar.addMenu("Edit")
        editmenu.addAction(undo_action)
        editmenu.addAction(redo_action)

        self.top_toolbar.addAction(undo_action)
        self.top_toolbar.addAction(redo_action)

    def add_view_menu(self):
        show_grid_action = QAction(QIcon(":/view/show_grid.svg"), "Show Grid",
                                   self)
        show_grid_action.setToolTip("<b>Show Grid</b><br>Make grid visible")
        show_grid_action.setCheckable(True)
        show_grid_action.setChecked(True)

        edit_grid_action = QAction(QIcon(":/view/edit_grid.svg"), "Edit Grid",
                                   self)
        edit_grid_action.setToolTip("<b>Grid Data</b><br>Edit grid data")

        grid_snap_action = QAction(QIcon(":/view/grid_snap.svg"), "Grid Snap",
                                   self)
        grid_snap_action.setCheckable(True)
        grid_snap_action.setChecked(True)
        grid_snap_action.setToolTip("<b>Grid Snap</b><br>Snap to nearest grid")

        show_axis_action = QAction(QIcon(":/view/diagram.svg"), "Show Axis",
                                   self)
        show_axis_action.setCheckable(True)
        show_axis_action.setChecked(True)
        tip = "<b>Show Axes</b><br>Display coordinate origin"
        show_axis_action.setToolTip(tip)
        show_axis_action.setStatusTip("Display coordinate origin")

        zoom_in_action = QAction(QIcon(":/view/zoom_in.svg"), "Zoom In", self)
        zoom_in_action.setToolTip("Zoom In")
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)

        zoom_out_action = QAction(QIcon(":/view/zoom_out.svg"), "Zoom Out",
                                  self)
        zoom_out_action.setToolTip("Zoom Out")
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)

        zoom_fit_action = QAction(QIcon(":/view/zoom_fit.svg"), "Zoom Fit",
                                  self)
        zoom_fit_action.setToolTip("Zoom Fit")

        refresh_view_action = QAction(
            QIcon(":/view/refresh_view.svg"), "Refresh View", self
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
        material_action = QAction(QIcon(":/define/material.svg"), "Material",
                                  self)
        material_action.setToolTip("Define material")

        section_action = QAction(QIcon(":/define/section.svg"), "Section",
                                 self)
        section_action.setToolTip("Define section")

        node_action = QAction(QIcon(":/define/node.svg"), "Node", self)
        node_action.setToolTip("Define node/joint")

        member_action = QAction(QIcon(":/define/member.svg"), "Member", self)
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
        draw_node_action = QAction(QIcon(":/draw/draw_node.svg"), "Draw Node",
                                   self)
        draw_node_action.setToolTip("Draw node")
        draw_node_action.triggered.connect(self.draw_node_action_clicked)

        draw_member_action = QAction(
            QIcon(":/draw/draw_member.svg"), "Draw member", self
        )
        draw_member_action.setToolTip("Draw member")
        draw_member_action.triggered.connect(self.draw_member_action_clicked)

        drawmenu = self.menubar.addMenu("Draw")
        drawmenu.addAction(draw_node_action)
        drawmenu.addAction(draw_member_action)

        self.left_toolbar.addAction(draw_node_action)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(draw_member_action)

    def add_assign_menu(self):
        joint_loads_action = QAction(
            QIcon(":/assign/joint_loads.svg"), "Joint loads", self
        )
        member_loads_action = QAction(
            QIcon(":/assign/member_loads.svg"), "Member loads", self
        )

        assignmenu = self.menubar.addMenu("Assign")
        assignmenu.addAction(joint_loads_action)
        assignmenu.addAction(member_loads_action)

        self.top_toolbar.addAction(joint_loads_action)
        self.top_toolbar.addAction(member_loads_action)

    def add_analyze_menu(self):
        run_static_analysis_action = QAction(
            QIcon(":/analyze/run.svg"), "Run Static Analysis", self
        )

        analyzemenu = self.menubar.addMenu("Analyze")
        analyzemenu.addAction(run_static_analysis_action)

        self.top_toolbar.addAction(run_static_analysis_action)
        self.top_toolbar.addSeparator()

    def add_display_menu(self):
        redraw_structure_action = QAction(
            QIcon(":/display/redraw_structure.svg"),
            "Draw undeformed structure", self
        )
        shear_force_action = QAction(
            QIcon(":/display/shear_force.svg"), "Draw shear force diagram",
            self
        )
        bending_moment_action = QAction(
            QIcon(":/display/bending_moment.svg"),
            "Draw bending moment diagram", self
        )
        deflection_action = QAction(
            QIcon(":/display/deflection.svg"), "Draw deflected shape", self
        )
        reactions_action = QAction(
            QIcon(":/display/reactions.svg"), "Draw reactions", self
        )

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
            QIcon(":/help/quick_intro.svg"), "Quick Introduction", self
        )
        license_info_action = QAction(
            QIcon(":/help/license.svg"), "License Information", self
        )
        check_updates_action = QAction(
            QIcon(":/help/check_update.svg"), "Check for Updates ...", self
        )
        about_action = QAction(QIcon(":/help/about.svg"), "About", self)

        helpmenu = self.menubar.addMenu("Help")
        helpmenu.addAction(quick_intro_action)
        helpmenu.addSeparator()
        helpmenu.addAction(license_info_action)
        helpmenu.addSeparator()
        helpmenu.addAction(check_updates_action)
        helpmenu.addSeparator()
        helpmenu.addAction(about_action)
