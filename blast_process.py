import tempfile
import pandas as pd
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Application import ApplicationError
from tkinter import messagebox


def perform_local_blast(query: str, database, output_file):

    # Write the query sequence to a temporary FASTA file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as query_file:
        query_file.write(">Query\n")
        query_file.write(query)

    # Set up the BLAST command
    blastn_cline = NcbiblastnCommandline(
        query=query_file.name,
        db=database,
        out=output_file,
        outfmt=6,
        max_target_seqs=1000,
        evalue=0.001,
    )

    # Execute the BLAST search
    try:
        blastn_cline()
    except ApplicationError as e:
        messagebox.showerror("Error", e.stderr)
        return

    blast_table = pd.read_csv(output_file, sep="\t", header=None)
    blast_table.columns = [
        "qseqid",
        "sseqid",
        "pident",
        "length",
        "mismatch",
        "gapopen",
        "qstart",
        "qend",
        "sstart",
        "send",
        "evalue",
        "bitscore",
    ]

    query_length = len(query)

    # Filter out hits that are shorter than the query sequence
    filtered_blast_table = blast_table[blast_table["length"] >= query_length - 10]

    filtered_blast_table.to_csv(output_file, sep="\t", index=False)

    return
