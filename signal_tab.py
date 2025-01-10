from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from signal_plot import plot_signal
from tkinter import messagebox
import time
import threading
from signal_plot import load_signal, sam_file_signal_search, plot_signal


def time_it(func):
    def wrapper(*args, **kwargs):

        global func_time
        if "func_time" not in globals():
            func_time = {}

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        if func.__name__ not in func_time:
            func_time[func.__name__] = 0

        func_time[func.__name__] += end - start
        return result

    return wrapper


class SignalTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        notebook.add(self, text="SIGNAL TOOL")
        self.create_widgets()

        self.sam_file = None
        self.signals_dir = None

    def create_widgets(self):
        # file select for sam file
        self.label_choose_sam = tk.Label(
            self, text="SELECT SAM FILE"
        )
        self.label_choose_sam.pack(pady=10)

        self.button_select_file = tk.Button(
            self, text="Select File", command=self.select_sam_file, anchor="w"
        )
        self.button_select_file.pack()

        self.label_chosen_sam = tk.Label(self, text="")
        self.label_chosen_sam.pack()

        # insert a separator
        self.separator1 = ttk.Separator(self, orient="horizontal")
        self.separator1.pack(fill="x", padx=10, pady=10)

        # directory select for fast5/pod5
        self.label_select_dir = tk.Label(
            self, text="SELECT FAST5/POD5 DIRECTORY"
        )
        self.label_select_dir.pack(pady=10)

        self.button_select_dir = tk.Button(
            self, text="Select Directory", command=self.select_fast_pod_dir, anchor="w"
        )
        self.button_select_dir.pack()

        self.label_chosen_dir = tk.Label(self, text="")
        self.label_chosen_dir.pack()

        # insert a separator
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.separator2.pack(fill="x", padx=10, pady=10)

        # edit for read id
        self.label_read_id = tk.Label(self, text="PROVIDE A READ ID")
        self.label_read_id.pack(pady=10)

        self.entry_read_id = tk.Entry(self, width=50)
        self.entry_read_id.pack()

        # insert a separator
        self.separator3 = ttk.Separator(self, orient="horizontal")
        self.separator3.pack(fill="x", padx=10, pady=10)

        # button for signal plotting
        self.button_plot = tk.Button(
            self, text="PLOT SIGNAL", command=self.plot_signal, font=("Arial", 20)
        )
        self.button_plot.pack(pady=20)

    def select_fast_pod_dir(self):
        try:
            directory = filedialog.askdirectory(
                title="Select a directory containing fast5/pod5 files"
            )
        except Exception as e:
            self.show_error(str(e))
            return

        self.label_chosen_dir.config(text=directory)
        self.signals_dir = directory

    def select_sam_file(self):
        try:
            filename = filedialog.askopenfilename(
                title="Select a SAM file", filetypes=[("SAM files", "*.sam")]
            )
        except Exception as e:
            self.show_error(str(e))
            return

        self.label_chosen_sam.config(text=filename)
        self.sam_file = filename

    def plot_signal(self):
        read_id = self.entry_read_id.get()

        if not read_id:
            self.show_error("Please provide a read ID")
            return
    
        if not self.sam_file:
            self.show_error("Please select a SAM file")
            return
        
        if not self.signals_dir:
            self.show_error("Please select a directory")
            return

        self.button_plot.config(state="disabled")

        def plot_signal_thread():
            self.button_plot.config(text="Searching for read ID in SAM file...")
            sam_search_result = sam_file_signal_search(self.sam_file, read_id)

            if sam_search_result is None:
                messagebox.showerror("Error", "Read ID not found in SAM file.")
                return

            self.button_plot.config(text="Loading signal...")
            signal_tuple = load_signal(self.signals_dir, read_id)
            if signal_tuple is None:
                messagebox.showerror("Error", "Signal not found.")

            self.button_plot.config(text="Plotting signal...")
            plot_signal(signal_tuple, sam_search_result, read_id)

            self.button_plot.config(state="normal", text="PLOT SIGNAL")

        thread = threading.Thread(target=plot_signal_thread)
        thread.start()
        return

    def show_error(self, message):
        messagebox.showerror("Error", message)
