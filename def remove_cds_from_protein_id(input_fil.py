def remove_cds_from_protein_id(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    with open(output_file, 'w') as f:
        f.write(lines[0])  # Write header
        for line in lines[1:]:
            parts = line.split('\t')
            protein_id = parts[-1].strip()
            if protein_id.startswith("cds-"):
                protein_id = protein_id[4:]  # Remove "cds-"
            parts[-1] = protein_id + '\n'
            new_line = '\t'.join(parts)
            f.write(new_line)

# Đường dẫn đến file kết quả và file output
input_file = 'd:\Python\exp\gene_id_sample.tsv'
output_file = 'output_bỏ_cds.tsv'

# Gọi hàm để loại bỏ chuỗi "cds-" từ cột protein_id và lưu vào file output
remove_cds_from_protein_id(input_file, output_file)
