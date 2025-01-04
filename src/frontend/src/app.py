from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget

from assets import resources  # noqa: F401


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("StructPro")

        TOOLBAR_ICON_SIZE = QSize(16, 16)

        menubar = self.menuBar()

        new_action = QAction(QIcon(":/file/new.svg"), "New", self)
        new_action.setToolTip("<b>New</b><br>Creates a new document")
        new_action.setStatusTip("Creates a new document")
        new_action.setShortcut(QKeySequence.StandardKey.New)

        open_action = QAction(QIcon(":/file/open.svg"), "Open", self)
        open_action.setToolTip("<b>Open</b><br>Open an existing document")
        open_action.setStatusTip("Open an existing document")
        open_action.setShortcut(QKeySequence.StandardKey.Open)

        save_action = QAction(QIcon(":/file/save.svg"), "Save", self)
        save_action.setToolTip("<b>Save</b><br>Save document")
        save_action.setStatusTip("Save document")
        save_action.setShortcut(QKeySequence.StandardKey.Save)

        save_as_action = QAction(QIcon(":/file/save_as.svg"), "Save As", self)
        save_as_action.setStatusTip("Save document under a new name")
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

        exit_action = QAction(QIcon(":/file/exit.svg"), "Exit", self)
        exit_action.setStatusTip("Close application")
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)

        filemenu = menubar.addMenu("File")
        filemenu.addAction(new_action)
        filemenu.addAction(open_action)
        filemenu.addSeparator()
        filemenu.addAction(save_action)
        filemenu.addAction(save_as_action)
        filemenu.addSeparator()
        filemenu.addAction(exit_action)

        undo_action = QAction(QIcon(":/edit/undo.svg"), "Undo", self)
        undo_action.setToolTip("<b>Undo</b><br>Undo last action")
        undo_action.setStatusTip("Undo last action")
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)

        redo_action = QAction(QIcon(":/edit/redo.svg"), "Redo", self)
        redo_action.setToolTip("<b>Redo</b><br>Do again the last undone action")
        redo_action.setStatusTip("Do again the last undone action")
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        editmenu = menubar.addMenu("Edit")
        editmenu.addAction(undo_action)
        editmenu.addAction(redo_action)

        set_grid_limit_action = QAction(
            QIcon(":/view/grid_limits.svg"),
            "Set Grid Limits",
            self,
        )
        set_grid_limit_action.setToolTip("<b>Grid Limits</b><br>Set grid limits")
        set_grid_limit_action.setStatusTip("Set grid limits")

        show_grid_action = QAction(
            QIcon(":/view/show_grid.svg"),
            "Show Grid",
            self,
        )
        show_grid_action.setCheckable(True)
        show_grid_action.setChecked(True)
        show_grid_action.setToolTip("<b>Show Grid</b><br>Make grid visible")
        show_grid_action.setStatusTip("Make grid visible")

        grid_snap_action = QAction(
            QIcon(":/view/grid_snap.svg"),
            "Grid Snap",
            self,
        )
        grid_snap_action.setCheckable(True)
        grid_snap_action.setChecked(True)
        grid_snap_action.setToolTip("<b>Grid Snap</b><br>Snap to nearest grid")
        grid_snap_action.setStatusTip("Snap to nearest grid")

        show_axes_action = QAction(
            QIcon(":/view/diagram.svg"),
            "Show Axes",
            self,
        )
        show_axes_action.setCheckable(True)
        show_axes_action.setChecked(True)
        show_axes_action.setToolTip("<b>Show Axes</b><br>Display coordinate origin")
        show_axes_action.setStatusTip("Display coordinate origin")

        zoom_in_action = QAction(QIcon(":/view/zoom_in.svg"), "Zoom In", self)
        zoom_in_action.setToolTip("Zoom In")
        zoom_in_action.setStatusTip("Zoom In")
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)

        zoom_out_action = QAction(
            QIcon(":/view/zoom_out.svg"),
            "Zoom Out",
            self,
        )
        zoom_out_action.setToolTip("Zoom Out")
        zoom_out_action.setStatusTip("Zoom Out")
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)

        zoom_fit_action = QAction(
            QIcon(":/view/zoom_fit.svg"),
            "Zoom Fit",
            self,
        )
        zoom_fit_action.setToolTip("Zoom Fit")
        zoom_fit_action.setStatusTip("Zoom Fit")

        refresh_view_action = QAction(
            QIcon(":/view/refresh_view.svg"),
            "Refresh View",
            self,
        )
        refresh_view_action.setToolTip("Refresh window")
        refresh_view_action.setStatusTip("Refresh window")

        viewmenu = menubar.addMenu("View")
        viewmenu.addAction(set_grid_limit_action)
        viewmenu.addAction(show_grid_action)
        viewmenu.addAction(grid_snap_action)
        viewmenu.addAction(show_axes_action)
        viewmenu.addSeparator()
        viewmenu.addAction(zoom_in_action)
        viewmenu.addAction(zoom_out_action)
        viewmenu.addAction(zoom_fit_action)
        viewmenu.addSeparator()
        viewmenu.addAction(refresh_view_action)

        material_action = QAction(QIcon(":/define/material.svg"), "Material", self)
        material_action.setToolTip("Define material")
        material_action.setStatusTip("Define material")

        section_action = QAction(QIcon(":/define/section.svg"), "Section", self)
        section_action.setToolTip("Define section")
        section_action.setStatusTip("Define section")

        node_action = QAction(QIcon(":/define/node.svg"), "Node", self)
        node_action.setToolTip("Define node/joint")
        node_action.setStatusTip("Define node/joint")

        member_action = QAction(QIcon(":/define/member.svg"), "Member", self)
        member_action.setToolTip("Define member")
        member_action.setStatusTip("Define member")

        definemenu = menubar.addMenu("Define")
        definemenu.addAction(material_action)
        definemenu.addAction(section_action)
        definemenu.addSeparator()
        definemenu.addAction(node_action)
        definemenu.addAction(member_action)

        draw_node_action = QAction(QIcon(":/draw/draw_node.svg"), "Draw Node", self)
        draw_node_action.setToolTip("Draw node")
        draw_node_action.setStatusTip("Draw node")

        draw_member_action = QAction(QIcon(":/draw/draw_member.svg"), "Draw member", self)
        draw_member_action.setToolTip("Draw member")
        draw_member_action.setStatusTip("Draw member")

        drawmenu = menubar.addMenu("Draw")
        drawmenu.addAction(draw_node_action)
        drawmenu.addAction(draw_member_action)

        joint_loads_action = QAction(QIcon(":/assign/joint_loads.svg"), "Joint loads", self)
        member_loads_action = QAction(QIcon(":/assign/member_loads.svg"), "Member loads", self)

        assignmenu = menubar.addMenu("Assign")
        assignmenu.addAction(joint_loads_action)
        assignmenu.addAction(member_loads_action)

        run_static_analysis_action = QAction(
            QIcon(":/analyze/run.svg"),
            "Run Static Analysis", self,
        )

        analyzemenu = menubar.addMenu("Analyze")
        analyzemenu.addAction(run_static_analysis_action)

        redraw_structure_action = QAction(QIcon(":/display/redraw_structure.svg"), "Redraw Structure", self)
        shear_force_action = QAction(QIcon(":/display/shear_force.svg"), "Shear Force", self)
        bending_moment_action = QAction(QIcon(":/display/bending_moment.svg"), "Bending Moment", self)
        deflection_action = QAction(QIcon(":/display/deflection.svg"), "Deflection", self)
        reactions_action = QAction(QIcon(":/display/reactions.svg"), "Show Reactions", self)

        displaymenu = menubar.addMenu("Display")
        displaymenu.addAction(redraw_structure_action)
        displaymenu.addSeparator()
        displaymenu.addAction(shear_force_action)
        displaymenu.addAction(bending_moment_action)
        displaymenu.addAction(deflection_action)
        displaymenu.addAction(reactions_action)

        quick_intro_action = QAction(QIcon(":/help/quick_intro.svg"), "Quick Introduction", self)
        license_info_action = QAction(QIcon(":/help/license.svg"), "License Information", self)
        check_updates_action = QAction(
            QIcon(":/help/check_update.svg"),
            "Check for Updates ...",
            self,
        )
        about_action = QAction(QIcon(":/help/about.svg"), "About", self)

        helpmenu = menubar.addMenu("Help")
        helpmenu.addAction(quick_intro_action)
        helpmenu.addSeparator()
        helpmenu.addAction(license_info_action)
        helpmenu.addSeparator()
        helpmenu.addAction(check_updates_action)
        helpmenu.addSeparator()
        helpmenu.addAction(about_action)

        horizontal_toolbar = QToolBar()
        horizontal_toolbar.setMovable(False)
        horizontal_toolbar.setIconSize(TOOLBAR_ICON_SIZE)
        horizontal_toolbar.addAction(new_action)
        horizontal_toolbar.addAction(open_action)
        horizontal_toolbar.addAction(save_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(undo_action)
        horizontal_toolbar.addAction(redo_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(zoom_in_action)
        horizontal_toolbar.addAction(zoom_out_action)
        horizontal_toolbar.addAction(zoom_fit_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(material_action)
        horizontal_toolbar.addAction(section_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(node_action)
        horizontal_toolbar.addAction(member_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(joint_loads_action)
        horizontal_toolbar.addAction(member_loads_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(run_static_analysis_action)
        horizontal_toolbar.addSeparator()
        horizontal_toolbar.addAction(redraw_structure_action)
        horizontal_toolbar.addAction(shear_force_action)
        horizontal_toolbar.addAction(bending_moment_action)
        horizontal_toolbar.addAction(deflection_action)
        horizontal_toolbar.addAction(reactions_action)

        select_mode_action = QAction(QIcon(":/misc/select.svg"), "Select", self)
        select_mode_action.setCheckable(True)
        select_mode_action.setChecked(True)

        vertical_toolbar = QToolBar(self)
        vertical_toolbar.setIconSize(TOOLBAR_ICON_SIZE)
        vertical_toolbar.setMovable(False)
        vertical_toolbar.addAction(select_mode_action)
        vertical_toolbar.addSeparator()
        vertical_toolbar.addAction(draw_node_action)
        vertical_toolbar.addAction(draw_member_action)
        vertical_toolbar.addSeparator()
        vertical_toolbar.addAction(set_grid_limit_action)
        vertical_toolbar.addAction(show_grid_action)
        vertical_toolbar.addAction(grid_snap_action)
        vertical_toolbar.addAction(show_axes_action)
        vertical_toolbar.addSeparator()

        statusbar = self.statusBar()

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, horizontal_toolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, vertical_toolbar)

        self.setStatusBar(statusbar)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    win = MainWindow()
    win.show()

    app.exec()
