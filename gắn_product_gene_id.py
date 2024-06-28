import pandas as pd
import gffutils

# Đọc file TSV
tsv_file = 'c:/Users/ADMIN/Desktop/salmon.merged.transcript.tsv'
df_tsv = pd.read_csv(tsv_file, sep='\t')

# Đọc file GFF và tạo database tạm thời
gff_file = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Data/old_new_combine_annotation_cds_to_exon.gff'
db = gffutils.create_db(gff_file, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)

# Kiểm tra các ID trong file GFF và lấy các sản phẩm từ Parent=
product_dict = {}
for feature in db.all_features(featuretype='CDS'):
    parent_id = feature.attributes.get('Parent', [''])[0]
    product = feature.attributes.get('product', [''])[0]
    if parent_id and product:
        product_dict[parent_id] = product

# In dictionary các sản phẩm
print("\nProduct dictionary:")
for key, value in product_dict.items():
    print(f"Parent ID: {key}, Product: {value}")

# Thêm cột product vào DataFrame
def get_product(gene_id):
    return product_dict.get(gene_id, '')

df_tsv['product'] = df_tsv['gene_id'].apply(get_product)

# Kiểm tra các giá trị product được thêm vào DataFrame
print("\nDataFrame with product column:")
print(df_tsv[['gene_id', 'product']])

# Lưu lại DataFrame đã được cập nhật
df_tsv.to_csv('updated_file.tsv', sep='\t', index=False)
