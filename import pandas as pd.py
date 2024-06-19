import csv

# Đọc dữ liệu từ file CSV
csv_file_path = 'file.csv'
tsv_file_path = 'file.tsv'

# Tạo một từ điển lưu trữ dữ liệu từ file CSV
protein_go_map = {}

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Bỏ qua dòng tiêu đề
    for row in csv_reader:
        protein_id = row[0]
        go_terms = row[1].split('|')
        protein_go_map[protein_id] = go_terms

# Ghi dữ liệu vào file TSV
with open(tsv_file_path, mode='r', newline='', encoding='utf-8') as tsv_file:
    lines = tsv_file.readlines()

# Mở file TSV để ghi dữ liệu
with open(tsv_file_path, mode='w', newline='', encoding='utf-8') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    for line in lines:
        # Tách dòng thành các cột
        columns = line.strip().split('\t')
        # Lấy protein_id từ cột cuối cùng
        protein_id = columns[-1]
        # Nếu protein_id có trong từ điển, ghi thêm cột go vào dòng tương ứng
        if protein_id in protein_go_map:
            go_terms = '|'.join(protein_go_map[protein_id])
            columns.insert(-1, go_terms)
        # Ghi dòng mới vào file TSV
        tsv_writer.writerow(columns)
