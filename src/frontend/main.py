import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageTk

img_folder = Path(__file__).parent / "imgs"


def load_img(img_path: str):
    img = Image.open(img_path)
    return ImageTk.PhotoImage(img)


def main():
    app = Application()
    app.mainloop()


class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=tk.SUNKEN)

        self.section_btn = ttk.Button(self, text="Section")
        self.section_btn.grid(row=0, column=0)

        self.node_img = load_img("./imgs/node.gif")
        self.node_btn = ttk.Button(
            self,
            text="Coordinates of Joints/Supports",
            image=self.node_img,  # type: ignore
        )
        self.node_btn.grid(row=0, column=1)

        self.member_img = load_img("./imgs/beam.gif")
        self.member_btn = ttk.Button(self, text="Member", image=self.member_img)
        self.member_btn.grid(row=0, column=2)

        self.force_btn = ttk.Button(self, text="Force")
        self.force_btn.grid(row=0, column=3)

        for wgt in self.winfo_children():
            wgt.bind("<Enter>", self.show_btn_desc)
            wgt.bind("<Leave>", self.clear_btn_desc)

    def clear_btn_desc(self, event: tk.Event):
        statusbar = self.master.get_statusbar()  # type: ignore
        statusbar.tooltip.set("")

    def show_btn_desc(self, event: tk.Event):
        wgt = event.widget
        statusbar = self.master.get_statusbar()  # type: ignore
        statusbar.tooltip.set(wgt["text"])


class Statusbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=tk.SUNKEN)

        self.tooltip = tk.StringVar()
        self._tooltip = ttk.Label(
            self,
            relief=tk.SUNKEN,
            textvariable=self.tooltip,
            anchor=tk.W,
        )
        self._tooltip.grid(row=0, column=0)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SAS")
        self.geometry("700x500")

        self.columnconfigure(0, weight=1)

        # self.rowconfigure(0, weight=1)

        # s = ttk.Style()
        # s.configure("Danger.TFrame", background="red", borderwidth=5, relief="raised")

        self.toolbar = Toolbar(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.statusbar = Statusbar(self)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_toolbar(self):
        return self.toolbar

    def get_statusbar(self):
        return self.statusbar


# class Frame(ttk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent)

#         self.btn = ttk.Button(self, text="Test")
#         self.btn.pack(side=tk.LEFT, padx=2, pady=2)

#         self.pack(side=tk.TOP, fill=tk.X)


if __name__ == "__main__":
    main()
