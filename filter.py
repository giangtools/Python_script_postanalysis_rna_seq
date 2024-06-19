import pandas as pd

# Đọc file TSV
df = pd.read_csv('d:/R/Script/GO_terms_frequency/go_term_counts.tsv', sep='\t')

# Loại bỏ các ký tự không mong muốn ở cột GO_term
df['GO_term'] = df['GO_term'].str.replace(r"[\[\]']", '', regex=True)

# Ghi lại file TSV đã được xử lý
df.to_csv('d:/R/Script/GO_terms_frequency/go_term_counts_clean.tsv', sep='\t', index=False)


# Hàm để đọc file OBO và tạo dictionary với key là GO_term và value là namespace
def parse_obo(file_path):
    go_namespace = {}
    with open(file_path, 'r') as f:
        current_term = None
        current_namespace = None
        in_term = False
        for line in f:
            line = line.strip()
            if line == "[Term]":
                in_term = True
                if current_term and current_namespace:
                    go_namespace[current_term] = current_namespace
                current_term = None
                current_namespace = None
            elif in_term:
                if line.startswith("id:"):
                    current_term = line.split("id:")[1].strip()
                elif line.startswith("namespace:"):
                    current_namespace = line.split("namespace:")[1].strip()
        # Thêm GO_term cuối cùng vào dictionary
        if current_term and current_namespace:
            go_namespace[current_term] = current_namespace
    return go_namespace

# Đọc file OBO và tạo dictionary
obo_file = 'd:/Python/exp/annotation_handling/script/go.obo'
go_namespace_dict = parse_obo(obo_file)

# Thêm cột namespace vào dataframe
df['namespace'] = df['GO_term'].map(go_namespace_dict)

# Lưu lại file TSV sau khi đã thêm cột namespace
df.to_csv('d:/R/Script/GO_terms_frequency/go_term_counts_namespace.tsv', sep='\t', index=False)