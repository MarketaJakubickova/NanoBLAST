from tkinter import filedialog
from tkinter import *
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

from blast_tab import BlastTab
from signal_tab import SignalTab
from export_tab import ExportTab

# Create the main window
root = tk.Tk()
root.title("NANOBLAST")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# First tab
blas_tab = BlastTab(notebook)

# Second tab
export_tab = ExportTab(notebook)

# Third tab
signal_tab = SignalTab(notebook)

if __name__ == "__main__":
    root.mainloop()
