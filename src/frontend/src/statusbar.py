import tkinter as tk
from tkinter import ttk


class Statusbar(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, relief=tk.SUNKEN, padding=2, **kwargs)

        new_btn = ttk.Button(self, text="testing")
        new_btn.grid(row=0, column=0)
