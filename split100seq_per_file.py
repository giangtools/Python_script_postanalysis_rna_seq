import os
def read_fasta_file(file_path):
    sequences = {}
    current_sequence_name = None
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>'):
                current_sequence_name = line.strip()[1:]
                sequences[current_sequence_name] = ''
            else:
                sequences[current_sequence_name] += line.strip()
    return sequences

def write_fasta_file(sequences, output_directory, max_sequences_per_file=100):
    sequence_count = 0
    file_count = 1
    current_file = None
    
    for name, sequence in sequences.items():
        if sequence_count % max_sequences_per_file == 0:
            current_file = open(os.path.join(output_directory, f"output_{file_count}.fasta"), 'w')
            file_count += 1
        current_file.write(f">{name}\n{sequence}\n")
        sequence_count += 1
    
    if current_file:
        current_file.close()

input_file = "d:\Python\Data\cut_file\GCF_020906585.1_ASM2090658v1_protein.faa"
output_directory = "d:\Python\Data\cut_file"
max_sequences_per_file = 100

sequences = read_fasta_file(input_file)
write_fasta_file(sequences, output_directory, max_sequences_per_file)
