import pandas as pd

# Đường dẫn tới file GFF
input_gff_path = 'd:/pipeline_rnaseq/old_new_combine_annotation_cds_to_exon.gff'
output_excel_path = 'c:/Users/ADMIN/TGiang/GD_63_Postanalysis/Test/output_test.xlsx'

# Đọc file GFF và trích xuất thông tin
def extract_locus_tag_and_product(file_path, locus_names):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                parts = line.strip().split('\t')
                if len(parts) > 8:
                    attributes = parts[8]
                    locus_tag = None
                    product = None
                    for attr in attributes.split(';'):
                        if attr.startswith('locus_tag='):
                            locus_tag = attr.split('=')[1]
                        elif attr.startswith('product='):
                            product = attr.split('=')[1]
                    if locus_tag in locus_names and product is not None:
                        data.append({
                            'locus_tag': locus_tag,
                            'product': product
                        })
    return data

# List of locus_names to extract
locus_names = [
    "DZC36_00020", "DZC36_00105", "DZC36_00515", "DZC36_00595",
    "DZC36_00640", "DZC36_00710", "DZC36_01045", "DZC36_01485",
    "DZC36_01945", "DZC36_02055", "DZC36_02095", "DZC36_02265",
    "DZC36_02445", "DZC36_02995", "DZC36_03000", "DZC36_03010",
    "DZC36_03110", "DZC36_03260", "DZC36_03300", "DZC36_03305",
    "DZC36_03345", "DZC36_03355", "DZC36_03805", "DZC36_03825",
    "DZC36_04140", "DZC36_04150", "DZC36_04335", "DZC36_04545",
    "DZC36_04940", "DZC36_05040", "DZC36_05440", "DZC36_05465",
    "DZC36_05530", "DZC36_06070", "DZC36_06335", "DZC36_06360",
    "DZC36_06505", "DZC36_06620", "DZC36_06825", "DZC36_07205",
    "DZC36_07220", "DZC36_07255", "DZC36_07270"
]

# Extract sequences
data = extract_locus_tag_and_product(input_gff_path, locus_names)

# Create a DataFrame
df = pd.DataFrame(data, columns=["locus_tag", "product"])

# Save the DataFrame to an Excel file
df.to_excel(output_excel_path, index=False)

print("Extraction and writing to Excel file completed successfully.")
