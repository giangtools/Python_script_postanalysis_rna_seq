import pandas as pd

# Đọc file TSV
df = pd.read_csv('d:/R/Script/GO_terms_frequency/go_freq.tsv', sep='\t')

# Hàm để đọc file OBO và tạo dictionary với key là GO_term và value là namespace và name
def parse_obo(file_path):
    go_namespace = {}
    go_name = {}
    with open(file_path, 'r') as f:
        current_term = None
        current_namespace = None
        current_name = None
        in_term = False
        for line in f:
            line = line.strip()
            if line == "[Term]":
                in_term = True
                if current_term and current_namespace:
                    go_namespace[current_term] = current_namespace
                if current_term and current_name:
                    go_name[current_term] = current_name
                current_term = None
                current_namespace = None
                current_name = None
            elif in_term:
                if line.startswith("id:"):
                    current_term = line.split("id:")[1].strip()
                elif line.startswith("namespace:"):
                    current_namespace = line.split("namespace:")[1].strip()
                elif line.startswith("name:"):
                    current_name = line.split("name:")[1].strip()
        # Thêm GO_term cuối cùng vào dictionary
        if current_term and current_namespace:
            go_namespace[current_term] = current_namespace
        if current_term and current_name:
            go_name[current_term] = current_name
    return go_namespace, go_name

# Đọc file OBO và tạo dictionary
obo_file = 'd:/Python/exp/annotation_handling/script/go.obo'
go_namespace_dict, go_name_dict = parse_obo(obo_file)

# Thêm cột namespace và name vào dataframe
df['namespace'] = df['GO_terms'].map(go_namespace_dict)
df['name'] = df['GO_terms'].map(go_name_dict)

df = df[['GO_terms', 'namespace', 'freq', 'name']]

# Lưu lại file TSV sau khi đã thêm cột namespace và name
df.to_csv('d:/R/Script/GO_terms_frequency/go_term_counts_namespace_name.tsv', sep='\t', index=False)
