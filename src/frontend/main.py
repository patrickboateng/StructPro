import tkinter as tk
from pathlib import Path
from tkinter import simpledialog, ttk

import tksheet
from PIL import Image, ImageTk

img_folder = Path(__file__).parent / "imgs"


def load_img(img_path: str):
    img = Image.open(img_path)
    return ImageTk.PhotoImage(img)


def main():
    app = Application()
    app.mainloop()


class SectionDialog(simpledialog.Dialog):
    def body(self, master):
        # Type Name
        frame = ttk.LabelFrame(master, text="Type Name")
        self.type_name_wgt = ttk.Entry(frame)
        self.type_name_wgt.insert(0, "TYPE1")
        self.type_name_wgt.pack(fill=tk.X)
        frame.grid(sticky=tk.EW)

        # Elastic Modulus
        frame = ttk.LabelFrame(master, text="Material")
        elastic_modulus_label = ttk.Label(
            frame,
            text="Modulus of elasticity, E",
        )
        self.elastic_modulus_wgt = ttk.Entry(frame)
        elastic_modulus_label.grid(row=0, column=0)
        self.elastic_modulus_wgt.grid(row=0, column=1)
        frame.grid()

        # Geometric Properties
        properties_frame = ttk.LabelFrame(master, text="Geometric Properties")
        area_label = ttk.Label(properties_frame, text="Cross Sectional Area, A")
        self.area_wgt = ttk.Entry(properties_frame)
        moi_label = ttk.Label(properties_frame, text="Moment of Inertia, I")
        self.moment_of_inertia_wgt = ttk.Entry(properties_frame)
        calc_btn = ttk.Button(properties_frame, text="Calculate")
        area_label.grid(row=0, column=0)
        self.area_wgt.grid(row=0, column=1)
        moi_label.grid(row=1, column=0)
        self.moment_of_inertia_wgt.grid(row=1, column=1)
        calc_btn.grid(row=2, column=1, sticky=tk.E)
        properties_frame.grid()

        return self.type_name_wgt


class NodeDialog(simpledialog.Dialog):
    def body(self, master):
        col_headers = (
            "Node ID",
            "X",
            "Y",
            "Point Load",
            "Point Moment",
            "RX",
            "RY",
            "RM",
        )

        self.node_entry_wgt = tksheet.Sheet(
            master,
            headers=col_headers,
            show_row_index=False,
            show_top_left=False,
        )
        self.node_entry_wgt.enable_bindings("all")
        self.node_entry_wgt.grid()

        return self.node_entry_wgt

    def add_row(self):
        self.node_entry_wgt.insert_row(row_index=True)

    def buttonbox(self):
        box = ttk.Frame(self)

        w = ttk.Button(box, text="Add Node", width=10, command=self.add_row)
        w.grid(row=0, column=0, sticky=tk.E)
        w = ttk.Button(box, text="Ok", width=10, command=self.ok, default=tk.ACTIVE)
        w.grid(row=0, column=1, sticky=tk.E)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        # Retrieve selected data or perform an action when OK is pressed
        selected_item = self.node_entry_wgt.focus()
        if selected_item:
            self.result = self.node_entry_wgt.item(selected_item)["values"]
        else:
            self.result = None


class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=tk.SUNKEN)

        self.parent = parent

        self.section_btn = ttk.Button(
            self,
            text="Section",
            command=self.open_section_dialog,
        )
        self.section_btn.grid(row=0, column=0)

        self.node_img = load_img("./imgs/node.gif")
        self.node_btn = ttk.Button(
            self,
            text="Coordinates of Joints/Supports",
            image=self.node_img,  # type: ignore
            command=self.open_node_dialog,
        )
        self.node_btn.grid(row=0, column=1)

        self.member_img = load_img("./imgs/beam.gif")
        self.member_btn = ttk.Button(self, text="Member", image=self.member_img)
        self.member_btn.grid(row=0, column=2)

        self.force_btn = ttk.Button(self, text="Apply Loads")
        self.force_btn.grid(row=0, column=3)

        for wgt in self.winfo_children():
            wgt.bind("<Enter>", self.show_btn_desc)
            wgt.bind("<Leave>", self.clear_btn_desc)

    def open_section_dialog(self):
        self.section_dialog = SectionDialog(self.parent, title="Section Properties")

    def open_node_dialog(self):
        self.node_dialog = NodeDialog(
            self.parent,
            title="Coordinates of Joints/Supports",
        )

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


if __name__ == "__main__":
    main()
