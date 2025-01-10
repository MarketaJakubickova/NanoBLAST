from tkinter import ttk
import tkinter as tk
import os
from tkinter import messagebox

from tkinter import filedialog
import threading

from sam_to_fasta import SAM_to_FASTA_convert
from blast_db_create import make_blast_db
from blast_process import perform_local_blast


class BlastTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        notebook.add(self, text="BLAST TOOL")
        self.create_widgets()

    def create_widgets(self):

        # file select for sam file

        self.label_tab1 = tk.Label(self, text="SAM CONVERSION TO FASTA")
        self.label_tab1.pack(pady=10)

        self.button_select_file = tk.Button(
            self, text="Select SAM File", command=self.select_sam_for_fasta, anchor="w"
        )
        self.button_select_file.pack()

        self.label_selected_sam_for_fasta = tk.Label(self, text="")
        self.label_selected_sam_for_fasta.pack()

        self.button_convert_to_fasta = tk.Button(
            self, text="CONVERT TO FASTA", command=self.convert_to_fasta
        )
        self.button_convert_to_fasta.pack(pady=10)

        # insert a separator
        self.separator1 = ttk.Separator(self, orient="horizontal")
        self.separator1.pack(fill="x", padx=10, pady=10)

        # file select for fasta file
        self.label_tab2 = tk.Label(self, text="CREATING BLAST DATABASE")
        self.label_tab2.pack(pady=10)

        self.button_select_file2 = tk.Button(
            self,
            text="Select FASTA File",
            command=self.select_fasta_for_blast,
            anchor="w",
        )
        self.button_select_file2.pack()

        self.label_selected_fasta_for_blast = tk.Label(self, text="")
        self.label_selected_fasta_for_blast.pack()

        self.button_create_blast_db = tk.Button(
            self, text="CREATE BLAST DATABASE", command=self.create_blast_db
        )
        self.button_create_blast_db.pack(pady=10)

        # insert a separator
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.separator2.pack(fill="x", padx=10)

        # run BLAST
        self.label_tab3 = tk.Label(self, text="BLAST SEARCH ALGORITHM")
        self.label_tab3.pack(pady=10)

        self.button_select_blast_db_dir = tk.Button(
            self,
            text="Select BLAST DATABASE Directory",
            command=self.select_blast_db_dir,
        )
        self.button_select_blast_db_dir.pack()

        self.label_selected_blast_db_dir = tk.Label(self, text="")
        self.label_selected_blast_db_dir.pack()

        self.entry_sequence = tk.Entry(self, width=50)
        self.entry_sequence.pack()

        self.button_run_blast = tk.Button(
            self, text="RUN BLAST", command=self.run_blast
        )
        self.button_run_blast.pack(pady=10)

    def select_sam_for_fasta(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("SAM files", "*.sam")], title="Select SAM file"
            )
            self.label_selected_sam_for_fasta.config(text=file_path)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

    def select_fasta_for_blast(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("FASTA files", "*.fasta")], title="Select FASTA file"
            )
            self.label_selected_fasta_for_blast.config(text=file_path)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

    def convert_to_fasta(self):
        sam_file = self.label_selected_sam_for_fasta.cget("text")
        # output_file = "output.fasta"

        if not sam_file:
            messagebox.showerror("Error", "Please select a SAM file")
            return

        try:
            output_file = filedialog.asksaveasfilename(
                title="Select file",
                filetypes=[("FASTA files", "*.fasta")],
                defaultextension=".fasta",
            )
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        if not output_file:
            return

        self.button_convert_to_fasta.config(state="disabled")

        def convert_to_fasta_thread():
            self.button_convert_to_fasta.config(text="Converting to fasta...")
            self.update()

            SAM_to_FASTA_convert(sam_file, output_file)

            self.button_convert_to_fasta.config(text="CONVERT TO FASTA", state="normal")
            self.update()

        # Create a new thread
        fasta_thread = threading.Thread(target=convert_to_fasta_thread)

        # Start the thread
        fasta_thread.start()

    def create_blast_db(self):
        fasta_file = self.label_selected_fasta_for_blast.cget("text")
        # output_dir = "blast_db/db"ň

        if not fasta_file:
            messagebox.showerror("Error", "Please select a FASTA file")
            return

        try:
            output_dir = filedialog.askdirectory(
                title="Select directory to save the blast database",
                mustexist=False,
            )
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        if not output_dir:
            return

        self.button_create_blast_db.config(state="disabled")

        def create_blast_db_thread():
            self.button_create_blast_db.config(text="Creating blast database...")
            self.update()

            # create the directory if it does not exist
            os.makedirs(os.path.dirname(output_dir), exist_ok=True)

            # Create the blast database
            make_blast_db(fasta_file, output_dir)

            self.button_create_blast_db.config(
                text="CREATE BLAST DATABASE", state="normal"
            )
            self.update()

        # Create a new thread
        blast_db_thread = threading.Thread(target=create_blast_db_thread)

        # Start the thread
        blast_db_thread.start()

    def select_blast_db_dir(self):
        try:
            directory = filedialog.askdirectory(
                title="Select directory containing the blast database"
            )
            self.label_selected_blast_db_dir.config(text=directory)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

    def run_blast(self):
        blast_db_dir = self.label_selected_blast_db_dir.cget("text")
        sequence = self.entry_sequence.get()

        if not blast_db_dir:
            messagebox.showerror("Error", "Please select a blast database directory")
            return

        if not sequence:
            messagebox.showerror("Error", "Please enter a sequence")
            return

        # output_file = "output.tsv"

        try:
            output_file = filedialog.asksaveasfilename(
                title="Select file",
                filetypes=[("TSV files", "*.tsv")],
                defaultextension=".tsv",
            )
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        if not output_file:
            return

        self.button_run_blast.config(state="disabled")

        def run_blast_thread():
            self.button_run_blast.config(text="Running BLAST...")
            self.update()

            perform_local_blast(sequence, blast_db_dir, output_file)

            self.button_run_blast.config(text="RUN BLAST", state="normal")
            self.update()

        # Create a new thread
        blast_thread = threading.Thread(target=run_blast_thread)

        # Start the thread
        blast_thread.start()
