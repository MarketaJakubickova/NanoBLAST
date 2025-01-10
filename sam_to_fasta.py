def SAM_to_FASTA_convert(input_sam_file, output_fasta_file):
    """
    input_sam_file: Path to the SAM file created by basecalling. If more SAM files were created, merge them into one before using the function
    output_fasta_file: Path to the location of the created FASTA file
    """

    with open(input_sam_file, "r") as sam_file, open(output_fasta_file, "w") as fasta_file:
        for line in sam_file:
            if line.startswith("@"):
                continue

            fields = line.strip().split("\t")

            read_id = fields[0]
            sequence = fields[9]

            fasta_file.write(f">{read_id}\n{sequence}\n")
