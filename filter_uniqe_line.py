'''

import pandas as pd

# Giả sử df là DataFrame của bạn
# df = ...
file_path = 'd:\Python\Data\cut_file\GCF_020906585.1_ASM2090658v1_protein.faa.tsv'
df = pd.read_csv(file_path, sep='\t')
# Lấy ra tất cả các cột trong DataFrame
columns = df.columns

# Lấy ra các giá trị duy nhất của cột đầu tiên
unique_values = df[columns[0]].unique()

# Tạo một danh sách để lưu các DataFrame con
dfs_to_concat = []

# Duyệt qua từng giá trị duy nhất của cột đầu tiên
for value in unique_values:
    # Lọc ra các hàng có giá trị cột đầu tiên là value
    filtered_df = df[df[columns[0]] == value]
    
    # Gom các giá trị của cột thứ 14
    combined_value = filtered_df.iloc[:, 13].sum()  # Giả sử cột thứ 14 là cột 14 (index từ 0)
    
    # Tạo một DataFrame mới từ giá trị kết quả
    new_df = pd.DataFrame({columns[0]: [value], columns[13]: [combined_value]})
    
    # Thêm DataFrame mới vào danh sách
    dfs_to_concat.append(new_df)

# Nối (concatenate) tất cả các DataFrame con thành một DataFrame
result_df = pd.concat(dfs_to_concat, ignore_index=True)

# In ra kết quả
print(result_df)

output_file_path = r'd:\Python\Data\cut_file\result.csv'
result_df.to_csv(output_file_path, index=False)
'''
import csv
from collections import defaultdict

def merge_values(input_file, output_file):
    # Tạo một từ điển để lưu trữ các giá trị cho mỗi khóa
    values_dict = defaultdict(list)
    
    # Đọc file input
    with open(input_file, 'r', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            key = row[0]
            value = row[13]
            values_dict[key].append(value)
    
    # Ghi kết quả ra file output
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for key, values in values_dict.items():
            writer.writerow([key, ','.join(values)])

# Gọi hàm merge_values với tên file input và output
merge_values('d:\Python\exp\GCF_020906585.1_ASM2090658v1_protein.faa.tsv', 'output.tsv')
