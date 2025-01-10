from Bio.Blast.Applications import NcbimakeblastdbCommandline
from Bio.Application import ApplicationError
from tkinter import messagebox


def make_blast_db(input_file, output_dir):
    makeblastdb_cline = NcbimakeblastdbCommandline(
        input_file=input_file, dbtype="nucl", out=output_dir
    )

    try:
        makeblastdb_cline()
    except ApplicationError as e:
        messagebox.showerror("Error", e.stderr)
        return

    return
