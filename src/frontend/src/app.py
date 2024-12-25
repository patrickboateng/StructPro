from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("StructPro")

        menubar = self.menuBar()

        new_action = QAction(QIcon("/imgs/file/new.png"), "New", self)
        open_action = QAction(QIcon(), "Open", self)
        save_action = QAction(QIcon(), "Save", self)
        save_as_action = QAction(QIcon(), "Save As", self)
        exit_action = QAction(QIcon(), "Exit", self)
        exit_action.triggered.connect(QApplication.quit)

        filemenu = menubar.addMenu("File")
        filemenu.addAction(new_action)
        filemenu.addAction(open_action)
        filemenu.addSeparator()
        filemenu.addAction(save_action)
        filemenu.addAction(save_as_action)
        filemenu.addSeparator()
        filemenu.addAction(exit_action)

        undo_action = QAction(QIcon(), "Undo", self)
        redo_action = QAction(QIcon(), "Redo", self)

        editmenu = menubar.addMenu("Edit")
        editmenu.addAction(undo_action)
        editmenu.addAction(redo_action)

        set_grid_limit_action = QAction(QIcon(), "Set Grid Limits", self)
        show_grid_action = QAction(QIcon(), "Show Grid", self)
        show_axes_action = QAction(QIcon(), "Show Axes", self)
        zoom_in_action = QAction(QIcon(), "Zoom In", self)
        zoom_out_action = QAction(QIcon(), "Zoom Out", self)
        zoom_fit_action = QAction(QIcon(), "Zoom Fit", self)
        refresh_view_action = QAction(QIcon(), "Refresh View", self)

        viewmenu = menubar.addMenu("View")
        viewmenu.addAction(set_grid_limit_action)
        viewmenu.addAction(show_grid_action)
        viewmenu.addAction(show_axes_action)
        viewmenu.addSeparator()
        viewmenu.addAction(zoom_in_action)
        viewmenu.addAction(zoom_out_action)
        viewmenu.addAction(zoom_fit_action)
        viewmenu.addSeparator()
        viewmenu.addAction(refresh_view_action)

        define_material_action = QAction(QIcon(), "Materials", self)
        define_section_action = QAction(QIcon(), "Section", self)

        definemenu = menubar.addMenu("Define")
        definemenu.addAction(define_material_action)
        definemenu.addAction(define_section_action)

        node_action = QAction(QIcon(), "Create Node", self)
        member_action = QAction(QIcon(), "Create Member", self)

        drawmenu = menubar.addMenu("Draw")
        drawmenu.addAction(node_action)
        drawmenu.addAction(member_action)

        joint_restraint_action = QAction(QIcon(), "Joint Restraint", self)
        joint_loads_action = QAction(QIcon(), "Joint Loads", self)
        member_loads_action = QAction(QIcon(), "Member loads", self)

        assignmenu = menubar.addMenu("Assign")
        assignmenu.addAction(joint_restraint_action)
        assignmenu.addSeparator()
        assignmenu.addAction(joint_loads_action)
        assignmenu.addAction(member_loads_action)

        run_static_analysis_action = QAction(QIcon(), "Run Static Analysis", self)

        analyzemenu = menubar.addMenu("Analyze")
        analyzemenu.addAction(run_static_analysis_action)

        redraw_structure_action = QAction(QIcon(), "Redraw Structure", self)
        shear_force_action = QAction(QIcon(), "Shear Force", self)
        bending_moment_action = QAction(QIcon(), "Bending Moment", self)
        deflection_action = QAction(QIcon(), "Deflection", self)
        reactions_action = QAction(QIcon(), "Reactions", self)

        displaymenu = menubar.addMenu("Display")
        displaymenu.addAction(redraw_structure_action)
        displaymenu.addSeparator()
        displaymenu.addAction(shear_force_action)
        displaymenu.addAction(bending_moment_action)
        displaymenu.addAction(deflection_action)
        displaymenu.addAction(reactions_action)

        quick_intro_action = QAction(QIcon(), "Quick Introduction", self)
        license_info_action = QAction(QIcon(), "License Information", self)
        check_updates_action = QAction(QIcon(), "Check for Updates ...", self)
        about_action = QAction(QIcon(), "About", self)

        helpmenu = menubar.addMenu("Help")
        helpmenu.addAction(quick_intro_action)
        helpmenu.addSeparator()
        helpmenu.addAction(license_info_action)
        helpmenu.addSeparator()
        helpmenu.addAction(check_updates_action)
        helpmenu.addSeparator()
        helpmenu.addAction(about_action)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    win = MainWindow()
    win.show()

    app.exec()
