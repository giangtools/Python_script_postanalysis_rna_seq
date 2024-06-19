'''
def count_refseq(filename):
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            count += line.count("RefSeq")
    return count


# Thay đổi tên tệp văn bản theo nhu cầu của bạn
filename = "D:\Backup_data_lab\sequence.gff"
refseq_count = count_refseq(filename)
print("Số lần từ 'RefSeq' xuất hiện trong tệp {}: {}".format(filename, refseq_count))
'''


'''
def count_lines_with_refseq(filename):
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            if "Protein Homology" in line:
                count += 1
    return count

# Thay đổi tên tệp văn bản theo nhu cầu của bạn
filename = "D:\Backup_data_lab\sequence.gff"
lines_with_refseq_count = count_lines_with_refseq(filename)
print("Số dòng chứa từ 'RefSeq' trong tệp {}: {}".format(filename, lines_with_refseq_count))
'''
"""
def filter_lines(filename):
    with open(filename, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')  # Tách các trường bằng dấu tab
            if len(fields) > 1 and "Protein Homology" not in fields[1]:
                print(line.strip())

# Thay đổi tên tệp văn bản theo nhu cầu của bạn
filename = "D:\Backup_data_lab\sequence.gff"
print("Các dòng không chứa từ 'Protein Homology' ở trường thứ 2:")
filter_lines(filename)
"""
import os
import pandas as pd

gff_file_path = "D:\Python\Data\sequence_new_1_trna.gff"
gene_name_path = "D:\Python\Data\genename.tsv"
# Đọc dữ liệu từ tệp GFF
data_GFF = pd.read_csv(gff_file_path, sep="\t", header=None)
gene_name = pd.read_csv(gene_name_path, sep="\t", header = None)

# Lấy ID từ hàng đầu tiên của genename.tsv
gene_id_to_find = gene_name.iloc[0, 0]

# Biến để lưu trữ kết quả
result = ""

# Duyệt qua từng dòng của tệp GFF
for index, row in data_GFF.iterrows():
    if "ID=" + gene_id_to_find in row[8]:
        # Nếu tìm thấy ID, kiểm tra Ontology_term
        if "Ontology_term" in row[8]:
            result = row[8].split("Ontology_term=")[1].split(";")[0]
        else:
            result = "RefSeq:" + row[8].split("ID=")[1].split(";")[0]
        break  # Thoát khỏi vòng lặp sau khi tìm thấy ID

# In kết quả
print("Kết quả cho hàng 1 của genename.tsv:", result)