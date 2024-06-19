import pandas as pd

# Đọc dữ liệu từ file "output_bỏ_cds.tsv"
df_output = pd.read_csv("D:/Python/exp/output_bỏ_cds.tsv", delimiter="\t")

# Đọc dữ liệu từ file "result.csv"
df_result = pd.read_csv("D:/Python/exp/result.csv")

# Merge hai dataframe dựa trên cột "protein_id"
merged_df = pd.merge(df_output, df_result, on="protein_id", how="left")

# Ghi nội dung của cột "go" vào file "output_bỏ_cds.tsv"
merged_df.to_csv("D:/Python/exp/output_bỏ_cds.tsv", sep="\t", index=False)

print("Ghi thành công!")
