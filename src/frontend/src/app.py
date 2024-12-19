import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk


def load_img(filename: str, foldername: str):
    fp = Path(__file__).parent / "imgs" / foldername / f"{filename}.png"
    return ImageTk.PhotoImage(Image.open(fp), size=(16, 16))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("StructPro")
        self.option_add("*tearOff", False)

        menubar = tk.Menu(self)

        foldername = "file"
        self.newimg = load_img("new", foldername)
        self.openimg = load_img("open", foldername)
        self.saveimg = load_img("save", foldername)
        self.saveasimg = load_img("save_as", foldername)
        self.exitimg = load_img("cross", foldername)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="New", image=self.newimg, compound=tk.LEFT)
        filemenu.add_command(label="Open", image=self.openimg, compound=tk.LEFT)
        filemenu.add_separator()
        filemenu.add_command(label="Save", image=self.saveimg, compound=tk.LEFT)
        filemenu.add_command(label="Save As", image=self.saveasimg, compound=tk.LEFT)
        filemenu.add_separator()
        filemenu.add_command(
            label="Exit", image=self.exitimg, compound=tk.LEFT, command=self.quit
        )
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar)
        editmenu.add_command(label="Undo")
        editmenu.add_command(label="Redo")
        menubar.add_cascade(label="Edit", menu=editmenu)

        viewmenu = tk.Menu(menubar)
        viewmenu.add_command(label="Set Limits")
        viewmenu.add_command(label="Show Grid")
        viewmenu.add_command(label="Show Axes")
        viewmenu.add_separator()
        viewmenu.add_command(label="Zoom In")
        viewmenu.add_command(label="Zoom Out")
        viewmenu.add_command(label="Zoom Extent")
        viewmenu.add_separator()
        viewmenu.add_command(label="Refresh Window")
        viewmenu.add_command(label="Refresh View")
        menubar.add_cascade(label="View", menu=viewmenu)

        definemenu = tk.Menu(menubar)
        definemenu.add_command(label="Materials")
        definemenu.add_command(label="Section")
        menubar.add_cascade(label="Define", menu=definemenu)

        drawmenu = tk.Menu(menubar)
        drawmenu.add_command(label="Joint/Node")
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

        helpmenu = tk.Menu(menubar)
        helpmenu.add_command(label="Quick Introduction")
        helpmenu.add_separator()
        helpmenu.add_command(label="License Information")
        helpmenu.add_separator()
        helpmenu.add_command(label="Check Updates")
        helpmenu.add_separator()
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=helpmenu)

        self["menu"] = menubar
