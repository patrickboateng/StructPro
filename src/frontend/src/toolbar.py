import tkinter as tk
from tkinter import ttk


class HorizontalToolbar(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, relief=tk.SUNKEN, padding=2, **kwargs)

        self.parent = master

        new_btn = ttk.Button(self, image=self.parent.new_file_img)
        new_btn.grid(row=0, column=0)

        open_btn = ttk.Button(self, image=self.parent.open_file_img)
        open_btn.grid(row=0, column=1)

        save_btn = ttk.Button(self, image=self.parent.save_file_img)
        save_btn.grid(row=0, column=2)

        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.grid(row=0, column=3, sticky=tk.NS, padx=4)

        undo_btn = ttk.Button(self, image=self.parent.undo_img)
        undo_btn.grid(row=0, column=4)

        redo_btn = ttk.Button(self, image=self.parent.redo_img)
        redo_btn.grid(row=0, column=5)

        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.grid(row=0, column=6, sticky=tk.NS, padx=4)

        zoom_in_btn = ttk.Button(self, image=self.parent.zoom_in_img)
        zoom_in_btn.grid(row=0, column=7)

        zoom_out_btn = ttk.Button(self, image=self.parent.zoom_out_img)
        zoom_out_btn.grid(row=0, column=8)

        zoom_fit_btn = ttk.Button(self, image=self.parent.zoom_fit_img)
        zoom_fit_btn.grid(row=0, column=9)

        refresh_view_btn = ttk.Button(self, image=self.parent.refresh_view_img)
        refresh_view_btn.grid(row=0, column=10)

        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.grid(row=0, column=11, sticky=tk.NS, padx=4)

        material_btn = ttk.Button(self, text="Material")
        material_btn.grid(row=0, column=12)

        section_btn = ttk.Button(self, text="Section")
        section_btn.grid(row=0, column=13)

        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.grid(row=0, column=14, sticky=tk.NS, padx=4)

        run_btn = ttk.Button(self, text="Run")
        run_btn.grid(row=0, column=15)

        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.grid(row=0, column=16, sticky=tk.NS, padx=4)

        redraw_btn = ttk.Button(self, text="Redraw")
        redraw_btn.grid(row=0, column=17)

        shear_force_btn = ttk.Button(self, text="S")
        shear_force_btn.grid(row=0, column=18)

        moment_btn = ttk.Button(self, text="B")
        moment_btn.grid(row=0, column=19)

        deflection_btn = ttk.Button(self, text="D")
        deflection_btn.grid(row=0, column=20)

        reaction_btn = ttk.Button(self, text="R")
        reaction_btn.grid(row=0, column=21)


class VerticalToolbar(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, relief=tk.SUNKEN, padding=2, **kwargs)

        self.parent = master

        new_btn = ttk.Button(self, image=self.parent.new_file_img)
        new_btn.grid(row=0, column=0)
