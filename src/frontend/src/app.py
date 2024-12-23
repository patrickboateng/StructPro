import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from main_window import MainWindow
from statusbar import Statusbar
from toolbar import HorizontalToolbar, VerticalToolbar


def load_img(filename: str, foldername: str, *, ext="png"):
    fp = Path(__file__).parent / "imgs" / foldername / f"{filename}.{ext}"
    return ImageTk.PhotoImage(Image.open(fp), size=(16, 16))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("StructPro")
        self.geometry("600x300+200+200")
        self.option_add("*tearOff", False)

        menubar = tk.Menu(self)

        foldername = "file"
        self.new_file_img = load_img("new", foldername)
        self.open_file_img = load_img("open", foldername)
        self.save_file_img = load_img("save", foldername)
        self.save_as_img = load_img("save_as", foldername)
        self.exit_img = load_img("exit", foldername)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="New", image=self.new_file_img, compound=tk.LEFT)
        filemenu.add_command(label="Open", image=self.open_file_img, compound=tk.LEFT)
        filemenu.add_separator()
        filemenu.add_command(label="Save", image=self.save_file_img, compound=tk.LEFT)
        filemenu.add_command(label="Save As", image=self.save_as_img, compound=tk.LEFT)
        filemenu.add_separator()
        filemenu.add_command(
            label="Exit", image=self.exit_img, compound=tk.LEFT, command=self.quit
        )
        menubar.add_cascade(label="File", menu=filemenu)

        foldername = "edit"
        self.undo_img = load_img("undo", foldername)
        self.redo_img = load_img("redo", foldername)
        editmenu = tk.Menu(menubar)
        editmenu.add_command(label="Undo", image=self.undo_img, compound=tk.LEFT)
        editmenu.add_command(label="Redo", image=self.redo_img, compound=tk.LEFT)
        menubar.add_cascade(label="Edit", menu=editmenu)

        foldername = "view"
        self.grid_limit_img = load_img("grid_limits", foldername)
        self.show_grid_img = load_img("show_grid", foldername)
        self.grid_snap_img = load_img("grid_snap", foldername)
        self.show_axes_img = load_img("diagram", foldername)
        self.zoom_in_img = load_img("zoom_in", foldername)
        self.zoom_out_img = load_img("zoom_out", foldername)
        self.zoom_fit_img = load_img("zoom_fit", foldername)
        self.refresh_view_img = load_img("refresh_view", foldername)
        viewmenu = tk.Menu(menubar)
        viewmenu.add_command(
            label="Set Grid Limits", image=self.grid_limit_img, compound=tk.LEFT
        )
        viewmenu.add_command(
            label="Show Grid", image=self.show_grid_img, compound=tk.LEFT
        )
        viewmenu.add_command(
            label="Grid Snap", image=self.grid_snap_img, compound=tk.LEFT
        )
        viewmenu.add_command(
            label="Show Axes", image=self.show_axes_img, compound=tk.LEFT
        )
        viewmenu.add_separator()
        viewmenu.add_command(label="Zoom In", image=self.zoom_in_img, compound=tk.LEFT)
        viewmenu.add_command(
            label="Zoom Out", image=self.zoom_out_img, compound=tk.LEFT
        )
        viewmenu.add_command(
            label="Zoom Fit", image=self.zoom_fit_img, compound=tk.LEFT
        )
        viewmenu.add_separator()
        viewmenu.add_command(
            label="Refresh View", image=self.refresh_view_img, compound=tk.LEFT
        )
        menubar.add_cascade(label="View", menu=viewmenu)

        definemenu = tk.Menu(menubar)
        definemenu.add_command(label="Materials")
        definemenu.add_command(label="Section")
        menubar.add_cascade(label="Define", menu=definemenu)

        foldername = "draw"
        self.node_img = load_img("node", foldername, ext="gif")
        drawmenu = tk.Menu(menubar)
        drawmenu.add_command(label="Joint/Node", image=self.node_img, compound=tk.LEFT)
        drawmenu.add_command(label="Member/Element")
        menubar.add_cascade(label="Draw", menu=drawmenu)

        analyzemenu = tk.Menu(menubar)
        analyzemenu.add_command(label="Run Static Analysis")
        menubar.add_cascade(label="Analyze", menu=analyzemenu)

        displaymenu = tk.Menu(menubar)
        displaymenu.add_command(label="Redraw Structure")
        displaymenu.add_command(label="Shear Force")
        displaymenu.add_command(label="Bending Moment")
        displaymenu.add_command(label="Deflection")
        displaymenu.add_command(label="Reactions")
        menubar.add_cascade(label="Display", menu=displaymenu)

        foldername = "help"
        self.about_img = load_img("about", foldername)
        self.check_update_img = load_img("check_update", foldername)
        helpmenu = tk.Menu(menubar)
        helpmenu.add_command(label="Quick Introduction")
        helpmenu.add_separator()
        helpmenu.add_command(label="License Information")
        helpmenu.add_separator()
        helpmenu.add_command(
            label="Check for Updates ...",
            image=self.check_update_img,
            compound=tk.LEFT,
        )
        helpmenu.add_separator()
        helpmenu.add_command(
            label="About",
            image=self.about_img,
            compound=tk.LEFT,
        )
        menubar.add_cascade(label="Help", menu=helpmenu)

        self["menu"] = menubar

        self.horizontal_toolbar = HorizontalToolbar(self)
        self.horizontal_toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.EW)

        self.vertical_toolbar = VerticalToolbar(self)
        self.vertical_toolbar.grid(row=1, column=0, sticky=tk.NS)

        self.main_window = MainWindow(self)
        self.main_window.grid(row=1, column=1, sticky=tk.NSEW)

        self.statusbar = Statusbar(self)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky=tk.EW)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)


if __name__ == "__main__":
    root = Application()
    root.mainloop()
