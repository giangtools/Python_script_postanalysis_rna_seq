import pandas as pd

# Đọc file GFF và lọc các dòng gene và CDS
file_path = 'd:/Backup_data_lab/3192_analysis/NCBI_GCF/GCF_020906585.1_ASM2090658v1_genomic.gff'  # Thay thế bằng đường dẫn đến file GFF của bạn

locus_tag_list = []
protein_id_list = []

# Mở và đọc file GFF
with open(file_path, 'r') as file:
    for line in file:
        if line.startswith('#'):
            continue  # Bỏ qua các dòng bắt đầu bằng '#'
        columns = line.strip().split('\t')
        if len(columns) < 9:
            continue  # Bỏ qua các dòng không đủ cột
        attributes = columns[8]
        
        if columns[2] == 'CDS':
            locus_tag = None
            protein_id = None
            for attribute in attributes.split(';'):
                if attribute.startswith('locus_tag='):
                    locus_tag = attribute.split('=')[1]
                if attribute.startswith('protein_id='):
                    protein_id = attribute.split('=')[1]
            if locus_tag and protein_id:
                locus_tag_list.append(locus_tag)
                protein_id_list.append(protein_id)

# Tạo DataFrame từ danh sách đã thu thập
df = pd.DataFrame({
    'locus_tag': locus_tag_list,
    'protein_id': protein_id_list
})

# Lưu DataFrame vào file CSV nếu cần
output_file_path = 'd:/Backup_data_lab/3192_analysis/test.csv'  # Thay thế bằng đường dẫn bạn muốn lưu file CSV
df.to_csv(output_file_path, index=False)

# Hiển thị DataFrame
print(df)
