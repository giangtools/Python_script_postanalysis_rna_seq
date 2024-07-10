import pandas as pd
import re
import ast

# Đọc file TSV và đặt tên cột
file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Interproscan/annot.faa.tsv'
column_names = [
    'Protein accession', 'Sequence MD5 digest', 'Sequence length', 'Analysis', 
    'Signature accession', 'Signature description', 'Start location', 'Stop location', 
    'Score', 'Status', 'Date', 'InterPro annotations - accession', 
    'InterPro annotations - description', 'GO annotations with their source(s)', 
    'Pathways annotations'
]

df = pd.read_csv(file_path, sep='\t', names=column_names)
# Chuyển đổi cột Score sang kiểu float
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
# Tạo DataFrame chứa các dòng có Score >= 1
filtered_out_df = df[df['Score'] >= 1]

# Lưu các dòng có Score >= 1 vào file khác
filtered_out_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Res/go_terms_python_merged/filtered_out_rows.tsv'
filtered_out_df.to_csv(filtered_out_file_path, sep='\t', index=False)
# Lọc bỏ các hàng có Score >= 1
df = df[df['Score'] < 1]

# Hàm trích xuất phần pro_id từ Protein accession
def extract_tmp(protein_accession):
    match = re.search(r'tmp_\d+', protein_accession)
    return match.group(0) if match else None

# Hàm trích xuất mã GO và loại bỏ phần trong ngoặc
def extract_go_annotations(go_annotations):
    if pd.isna(go_annotations):
        return []
    go_terms = re.findall(r'GO:\d+', go_annotations)
    return list(set(go_terms))  # Loại bỏ trùng lặp

# Áp dụng các hàm trên DataFrame
df['pro_id'] = df['Protein accession'].apply(extract_tmp)
df['GO_terms'] = df['GO annotations with their source(s)'].apply(extract_go_annotations)

# Lọc bỏ các hàng không có GO_terms
df_filtered = df[df['GO_terms'].apply(lambda x: len(x) > 0)]

# Gộp các hàng có pro_id trùng lặp và loại bỏ các GO_terms trùng lặp
def merge_go_terms(go_terms):
    merged_go_terms = set()
    for terms in go_terms:
        merged_go_terms.update(terms)
    return list(merged_go_terms)

df_grouped = df_filtered.groupby('pro_id').agg({
    'GO_terms': merge_go_terms
}).reset_index()


# Lưu kết quả vào file mới nếu cần
output_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Res/go_terms_python_merged/id_goterms.tsv'
df_grouped[['pro_id', 'GO_terms']].to_csv(output_file_path, sep='\t', index=False)

# Đọc dữ liệu từ file TSV của kết quả Salmon
salmon_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Data/modified/Giang_MolBiolab_result/Modified/salmon/salmon.merged.transcript_tpm.tsv'
#salmon_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/salmon.merged.transcript_tpm.tsv'
salmon_df = pd.read_csv(salmon_file_path, sep='\t')
# Lọc các dòng có giá trị 0 ở 1 hoặc 2 lần trong ba lần lặp
zero_filtered_df = salmon_df[(salmon_df[['Control1', 'Control2', 'Control3']] == 0).sum(axis=1).isin([1, 2])]
# Lưu các dòng đã lọc vào file khác
zero_filtered_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Res/go_terms_python_merged/zero_filtered_genes.tsv'
zero_filtered_df.to_csv(zero_filtered_file_path, sep='\t', index=False)

# Lọc bỏ các dòng có giá trị 0 ở 1 hoặc 2 lần trong ba lần lặp khỏi dataframe chính
#salmon_df = salmon_df[(salmon_df[['Control1', 'Control2', 'Control3']] != 0).sum(axis=1) == 3]
salmon_df = salmon_df[(salmon_df[['Control1', 'Control2', 'Control3']] == 0).sum(axis=1).isin([0, 3])]
# Đọc dữ liệu từ file TSV chứa id và Go_terms
go_terms_df = pd.read_csv(output_file_path, sep='\t', header=0)

# Tạo cột mean (trung bình) và sd (độ lệch chuẩn) và cột S/V
salmon_df['mean'] = salmon_df[['Control1', 'Control2', 'Control3']].mean(axis=1)
salmon_df['sd'] = salmon_df[['Control1', 'Control2', 'Control3']].std(axis=1)
salmon_df['S_V'] = (salmon_df['sd']/salmon_df['mean'])

# Sắp xếp lại kết quả hiển thị của file sắp xuất
salmon_df_1 = salmon_df
salmon_df_1 = salmon_df_1[['tx', 'gene_id', 'Control1', 'Control2', 'Control3', 'mean', 'sd', 'S_V']]

# Loại bỏ tiền tố phía trước id trong kết quả Salmon
salmon_df['id'] = salmon_df['gene_id'].apply(lambda x: x.split('-')[-1])
salmon_df['pro_id'] = salmon_df['id']

# Xuất file đầu tiên xử lý bao gồm mean, sd và độ lệch chuẩn
output_file_path_1 = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Res/go_terms_python_merged/salmon_results_with_mean_sd_sv.tsv'
salmon_df_1.to_csv(output_file_path_1, sep='\t', index=False)

# Loại bỏ .1 từ cột protein_id
#salmon_df['pro_id'] = salmon_df['protein_id'].str.replace('.1$', '', regex=True)
######################
# Đoạn code để xử lý thông tin từ file GFF và thêm vào DataFrame
gff_file = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Data/old_new_combine_annotation_cds_to_exon.gff'  # Đường dẫn đến file GFF của bạn
# Đọc file GFF và lọc dữ liệu
gff_data = pd.read_csv(gff_file, sep='\t', header=None, comment='#', 
                       names=['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'])

# Tạo một cột 'product' trống trong DataFrame salmon_df
salmon_df['product'] = None

# Duyệt qua từng gene trong DataFrame salmon_df và trích xuất thông tin product từ file GFF
for index, row in salmon_df.iterrows():
    # Lấy giá trị tx của gene hiện tại
    tx_value = row['tx']
    
    # Chọn các dòng có type là 'exon' và có Parent trong attributes giống với tx của gene hiện tại
    exon_data = gff_data[(gff_data['type'] == 'exon') & (gff_data['attributes'].str.contains('Parent=' + tx_value))]
    
    # Kiểm tra nếu có ít nhất một dòng thỏa mãn điều kiện
    if len(exon_data) > 0:
        # Lấy giá trị product từ dòng đầu tiên thỏa mãn điều kiện
        product_value = exon_data['attributes'].str.extract(r'product=([^;]+);')[0].iloc[0]
    else:
        product_value = None
    
    # Gán giá trị product vào cột 'product' tương ứng với gene hiện tại
    salmon_df.at[index, 'product'] = product_value

# Hiển thị DataFrame sau khi đã thêm cột 'product'
print(salmon_df)
######################

# Kết hợp Go_terms vào kết quả Salmon
salmon_df = salmon_df.merge(go_terms_df, on='pro_id', how='left')

# Sắp xếp lại các cột để hiển thị
salmon_df = salmon_df[['tx', 'gene_id', 'Control1', 'Control2', 'Control3', 'mean', 'sd', 'S_V', 'GO_terms', 'product']]
print(salmon_df)

# Lưu kết quả vào file mới nếu cần
output_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Res/go_terms_python_merged/salmon_results_with_go_terms.tsv'
salmon_df.to_csv(output_file_path, sep='\t', index=False)



#######################
# Đọc file TSV chứa thông tin về preferredName
preferred_name_file_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Data/data_id_stringdb/string_mapping.tsv'
preferred_name_df = pd.read_csv(preferred_name_file_path, sep='\t')

# Trích xuất phần tmp_ từ cột queryItem
def extract_tmp_query(query_item):
    match = re.search(r'tmp_\d+', query_item)
    return match.group(0) if match else None

preferred_name_df['tmp_id'] = preferred_name_df['queryItem'].apply(extract_tmp_query)

# Trích xuất phần tmp_ từ cột tx trong salmon_df
def extract_tmp_tx(tx):
    match = re.search(r'tmp_\d+', tx)
    return match.group(0) if match else None

salmon_df['tmp_id'] = salmon_df['tx'].apply(extract_tmp_tx)

# Merge DataFrame dựa trên cột tmp_id
merged_df = salmon_df.merge(preferred_name_df[['tmp_id', 'preferredName']], on='tmp_id', how='left')

# Hiển thị DataFrame sau khi thêm cột preferredName
print(merged_df)

# Sắp xếp lại các cột để hiển thị
merged_df = merged_df[['tx', 'gene_id', 'Control1', 'Control2', 'Control3', 'mean', 'sd', 'S_V', 'GO_terms', 'product', 'preferredName']]
print(merged_df)
# Lưu kết quả vào file mới nếu cần
#output_file_path_with_preferred_name = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Data/data_id_stringdb/salmon_results_with_go_terms_and_preferred_name.tsv'
#merged_df.to_csv(output_file_path_with_preferred_name, sep='\t', index=False)
#######################


##############################################
# Tạo một cột 'name_gff' trống trong DataFrame salmon_df
merged_df['name_gff'] = None

# Duyệt qua từng gene trong DataFrame salmon_df và trích xuất thông tin 'Name' từ file GFF
for index, row in salmon_df.iterrows():
    # Lấy giá trị gene_id của gene hiện tại
    gene_id = row['gene_id']
    
    # Tìm thông tin về gene_id trong file GFF
    gff_info = gff_data[gff_data['attributes'].str.contains('gene=' + gene_id)]
    
    # Kiểm tra nếu có ít nhất một dòng thỏa mãn điều kiện
    if len(gff_info) > 0:
        # Lấy giá trị 'Name' từ dòng đầu tiên thỏa mãn điều kiện
        name_value = gff_info['attributes'].str.extract(r'Name=([^;]+);')[0].iloc[0]
        if pd.isna(name_value):  # Xử lý trường hợp không tìm thấy giá trị 'Name'
            name_value = 'N/A'
    else:
        name_value = 'N/A'
    
    # Gán giá trị 'Name' vào cột 'name_gff' tương ứng với gene hiện tại
    merged_df.at[index, 'name_gff'] = name_value

# Hiển thị DataFrame sau khi đã thêm cột 'name_gff' và điền giá trị
print(merged_df)
output_file_path_with_preferred_name = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Data/data_id_stringdb/salmon_results_with_preferredname_gffname.tsv'
merged_df.to_csv(output_file_path_with_preferred_name, sep='\t', index=False)
############################################################