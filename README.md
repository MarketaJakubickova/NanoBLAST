# NanoBLAST

NanoBLAST is a Python-based tool designed for handling FAST5 and POD5 formats and facilitating various bioinformatics tasks, including sequence searching and signal processing. The tool is associated with the research paper [available here](https://dspace.vut.cz/bitstreams/75230bec-9bd6-476f-97db-2aaabb7ba50c/download).

## Authors
This project was developed by:
- **Martin Suriak**
- **Markéta Nykrýnová**

This work was supported by a grant project from the Czech Science Foundation [GA23-05845S].

## Structure

The tool is composed of the following Python scripts:

- `blast_db_create.py` – For creating BLAST databases.
- `blast_process.py` – Processes BLAST output data.
- `blast_tab.py` – Handles tabulated BLAST outputs.
- `export_tab.py` – Exports tabulated data.
- `main.py` – Main script to execute the tool.
- `parquet_tool.py` – Manages Parquet data processing.
- `sam_to_fasta.py` – Converts SAM files to FASTA format.
- `signal_plot.py` – Plots signal squiggles.
- `signal_tab.py` – Handles tabulated signal data.

## How to Use

1. **Run the Main Script**  
   Start the tool by executing `main.py`.

2. **Handling SAM Files**  
   - If the chosen process requires working with a SAM file, ensure it is a complete SAM file.  
   - For FAST5 data, it may be necessary to merge BAM files into a single file and convert it to SAM format before processing.

3. **BLAST Tool Guidelines**  
   - Write nucleotide sequences in uppercase letters in editable fields.  
   - When selecting a directory containing the BLAST database, individual files that constitute the database will not appear. This is expected behavior, and the process should still work.  
   - Similarly, for selecting FAST5 or POD5 directories in other parts of the tool, the files may not be individually displayed, but functionality is unaffected.
