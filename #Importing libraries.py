#Importing libraries
import os 
import pandas as pd 
import numpy as np

# 1. Change working directory
wdPath = "/media/molbiolab320/829eea22-fcb5-45d2-82ab-bad97f8c3820/home/mobiolab3/TG_data_backup/data/HP_GD63/compare_annot"
os.chdir(wdPath)

df_cols = ["SeqID", "Source", "FeatureType",
           "Start", "End",
           "Score", "Strand", "Phase", "Attribute"]

# 2. Import Dataframes
def import_df(file_name):
    df = pd.read_csv(file_name, skiprows=5, sep="\t")
    
    df.columns = df_cols
    df = df[["SeqID", "FeatureType", "Start", "End",
                         "Strand", "Attribute"]]
# 3. Create TotalID as a key for merging dataframes
    df[["Start", "End"]] = df[["Start", "End"]].astype(str)
    df['TotalID'] = df[["FeatureType", "Start", "End", "Strand"]].agg('_'.join, axis=1)
    return df

new_df = import_df("new_annot.gff")
old_df = import_df("old_annot.gff")

print(new_df.head(n=3))
print("Num of new annot: " + str(len(new_df.index)))

print(old_df.head(n=3))
print("Num of old annot" + str(len(old_df.index)))

#Merge dataframes by TotalID
merged_df = old_df.merge(new_df, how = "outer", on = "TotalID",
                         suffixes = ("_old", "_new"))
print(merged_df.head(n=3))
print(len(merged_df.index))

# Add "Diff" column
def add_Diff_col(row):
    compare_list = ["FeatureType", "Start", "End", "Strand"]
   
    for item in compare_list:
        if row[item + "_old"] != row[item + "_new"]:
            print("yes")
            if len(row["Diff"]) == 0:
                row["Diff"] = item
            else:
                row["Diff"] += "," + item
    return row

merged_df["Diff"] = ""
merged_df2 = merged_df.apply(add_Diff_col, axis = 1)


