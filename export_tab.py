import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from parquet_tool import (
    extract_info_from_tsv,
    sam_file_signal_search,
    load_signals,
    dump_signals_parquet,
    dump_signals_csv,
)

import threading


class ExportTab(tk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        notebook.add(self, text="EXPORT TOOL")
        self.create_widgets()

    def create_widgets(self):
        self.label_tab3 = tk.Label(self, text="SIGNAL EXTRACTOR")
        self.label_tab3.pack(pady=5)

        self.grid = tk.Frame(self)

        self.button_select_directory_for_pq = tk.Button(
            self.grid,
            text="Select POD5/FAST5 Directory",
            command=self.select_fast_pod_dir_for_pq,
        )
        self.button_select_directory_for_pq.grid(row=0, column=0, padx=5)

        self.button_selected_sam_for_pq = tk.Button(
            self.grid,
            text="Select SAM File",
            command=self.select_sam_for_pq,
        )
        self.button_selected_sam_for_pq.grid(row=0, column=1, padx=5)

        self.button_select_tsv = tk.Button(
            self.grid,
            text="Select TSV File",
            command=self.select_tsv_for_pq,
        )
        self.button_select_tsv.grid(row=0, column=2, padx=5)

        self.grid.pack(fill="x", padx=10)

        self.button_select_directory_for_pq = tk.Button(
            self.grid,
            text="Select POD5/FAST5 Directory",
            command=self.select_fast_pod_dir_for_pq,
        )
        self.button_select_directory_for_pq.grid(row=0, column=0, padx=5)

        self.button_selected_sam_for_pq = tk.Button(
            self.grid,
            text="Select SAM File",
            command=self.select_sam_for_pq,
        )
        self.button_selected_sam_for_pq.grid(row=0, column=1, padx=5)

        self.button_select_tsv = tk.Button(
            self.grid,
            text="Select TSV File",
            command=self.select_tsv_for_pq,
        )
        self.button_select_tsv.grid(row=0, column=2, padx=5)

        self.grid.pack(fill="x", padx=10)

        self.label_selected_directory_for_pq = tk.Label(self, text="")
        self.label_selected_directory_for_pq.pack(padx=10)

        self.label_selected_sam_for_pq = tk.Label(self, text="")
        self.label_selected_sam_for_pq.pack(padx=10)

        self.label_selected_tsv_for_pq = tk.Label(self, text="")
        self.label_selected_tsv_for_pq.pack(padx=10)

        self.label_selected_directory = tk.Label(self, text="")
        self.label_selected_directory.pack(padx=10)

        self.create_grid = tk.Frame(self)

        self.button_create_parquet = tk.Button(
            self.create_grid,
            text="CREATE PARQUET FILE",
            command=self.create_parquet_file,
        )
        self.button_create_parquet.pack(fill="x", side="left", padx=5)

        self.button_create_csv = tk.Button(
            self.create_grid, text="CREATE CSV FILE", command=self.create_csv_file
        )
        self.button_create_csv.pack(fill="x", side="left", padx=5)

        self.create_grid.pack(fill="x", padx=10, pady=10)

    def select_fast_pod_dir_for_pq(self):
        try:
            directory = filedialog.askdirectory(
                title="Select directory containing the POD5/FAST5 files"
            )
            self.label_selected_directory_for_pq.config(text=directory)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

    def select_sam_for_pq(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("SAM files", "*.sam")], title="Select SAM file"
            )
            self.label_selected_sam_for_pq.config(text=file_path)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

    def select_tsv_for_pq(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("TSV files", "*.tsv")], title="Select TSV file"
            )
            self.label_selected_tsv_for_pq.config(text=file_path)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

    def create_parquet_file(self):
        sam_file = self.label_selected_sam_for_pq.cget("text")
        directory = self.label_selected_directory_for_pq.cget("text")
        tsv_file = self.label_selected_tsv_for_pq.cget("text")

        if not sam_file:
            messagebox.showerror("Error", "Please select a SAM file")
            return

        if not directory:
            messagebox.showerror("Error", "Please select a directory")
            return

        if not tsv_file:
            messagebox.showerror("Error", "Please select a TSV file")
            return

        # output_file = "signals.parquet"
        try:
            output_file = filedialog.asksaveasfilename(
                title="Select file",
                filetypes=[("Parquet files", "*.parquet")],
                defaultextension=".parquet",
            )
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        if not output_file:
            return

        self.button_create_parquet.config(state="disabled")

        def create_parquet_file_thread():
            self.button_create_parquet.config(text="Loading tsv file...")
            self.update()
            info = extract_info_from_tsv(tsv_file)

            self.button_create_parquet.config(
                text="Searching for signals in sam file..."
            )
            self.update()
            signal_ranges = sam_file_signal_search(sam_file, info.keys(), info)

            self.button_create_parquet.config(
                text="Loading signals from pod5/fast5 files..."
            )
            self.update()
            signals = load_signals(directory, signal_ranges)

            self.button_create_parquet.config(text="Dumping signals to parquet file...")
            self.update()
            dump_signals_parquet(signals, signal_ranges, output_file)

            self.button_create_parquet.config(
                text="CREATE PARQUET FILE", state="normal"
            )
            self.update()

        # Create a new thread
        parquet_thread = threading.Thread(target=create_parquet_file_thread)

        # Start the thread
        parquet_thread.start()

    def create_csv_file(self):
        sam_file = self.label_selected_sam_for_pq.cget("text")
        directory = self.label_selected_directory_for_pq.cget("text")
        tsv_file = self.label_selected_tsv_for_pq.cget("text")

        if not sam_file:
            messagebox.showerror("Error", "Please select a SAM file")
            return

        if not directory:
            messagebox.showerror("Error", "Please select a directory")
            return

        if not tsv_file:
            messagebox.showerror("Error", "Please select a TSV file")
            return

        # output_file = "signals.csv"
        try:
            output_file = filedialog.asksaveasfilename(
                title="Select file",
                filetypes=[("CSV files", "*.csv")],
                defaultextension=".csv",
            )
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        if not output_file:
            return

        self.button_create_csv.config(state="disabled")

        def create_csv_file_thread():
            self.button_create_csv.config(text="Loading tsv file...")
            self.update()
            info = extract_info_from_tsv(tsv_file)

            self.button_create_csv.config(text="Searching for signals in sam file...")
            self.update()
            signal_ranges = sam_file_signal_search(sam_file, info.keys(), info, mode="csv")

            self.button_create_csv.config(
                text="Loading signals from pod5/fast5 files..."
            )
            self.update()
            signals = load_signals(directory, signal_ranges, mode="csv")

            self.button_create_csv.config(text="Dumping signals to csv file...")
            self.update()
            dump_signals_csv(signals, signal_ranges, output_file)

            self.button_create_csv.config(text="CREATE CSV FILE", state="normal")
            self.update()

        # Create a new thread
        csv_thread = threading.Thread(target=create_csv_file_thread)

        # Start the thread
        csv_thread.start()
