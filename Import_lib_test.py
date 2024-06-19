# Import lib
import os
import pandas as pd
import numpy as np
# 1. Change working directory
wdPath = "D:\Python\Data"
os.chdir(wdPath)
df_cols = ["SeqID", "Source", "FeatureType",
           "Start", "End",
           "Score", "Strand", "Phase", "Attribute"]

# 2. Import dataframes
def import_df(file_name):
    df = pd.read_csv(file_name, skiprows = 5,sep ="\t")

    df.columns = df_cols # Add column names
    df = df[["SeqID", "FeatureType", "Start", "End",
             "Strand", "Attribute"]]    
    # Create TotalID as key for merging dataframes
    df[["Start", "End"]] = df[["Start", "End"]].astype(str)
    df['TotalID'] = df[["FeatureType", "Start", "End","Strand"]].agg('_'.join, axis=1)
    return df

new_df = import_df("D:/Python/Data/compare_annot/new_annot.gff")
old_df = import_df("D:/Python/Data/compare_annot/old_annot.gff")

# Checking dataframe
# If numerical dataframe:
    #print(new_df).describe()
# If informative dataframe:
#print(new_df.head(n = 3))
#print("Num of lines new annot: " + str(len(new_df.index)) )

#print(old_df.head(n = 3))
#print("Num of lines new annot: " + str(len(old_df.index)) )
# 3. Merge dataframes by TotalID
merged_df = old_df.merge(new_df, how = "outer", on = "TotalID",
                         suffixes = ("_old","_new"))
#print(merged_df.head(n=3))
#print(len(merged_df.index))
# Add "Diff" column
def add_Diff_col(row):
    compare_list = ["FeatureType", "Start", "End", "Strand"]
   
    for item in compare_list:
        if row[item + "_old"] != row[item + "_new"]:
            #print("yes")
            if len(row["Diff"]) == 0:
                row["Diff"] = item
            else:
                row["Diff"] += "," + item
    return row

                         
merged_df["Diff"] = ""
merged_df2 = merged_df.apply(add_Diff_col, axis = 1)


# Write table
merged_df2.drop("TotalID", axis = 1, inplace = True)
merged_df2.to_csv("test_mergedOldNew1.tsv", sep = "\t", index = False)


# Diff GENE/CDS processing
diff_compare_annot = 'D:\Python\Data\compare_annot\diff_compare_annot.xlsx'
df_diff = pd.read_excel(diff_compare_annot, header=0)
df_diff["product"] = None
#Extract NAME in Attribute
for index, row in df_diff.iterrows():
    # Kiểm tra nếu giá trị là chuỗi
    if isinstance(row['Attribute_new'], str):
        attribute_new = row['Attribute_new'].split(';')
        for attr in attribute_new:
            keyvalue = attr.split('=')
            if keyvalue[0] == 'product':
                df_diff.at[index, 'product'] = keyvalue[1]
    else:
        if isinstance(row['Attribute_old'], str):
            attribute_old = row['Attribute_old'].split(';')
            for attr in attribute_old:
                keyvalue = attr.split('=')
                if keyvalue[0] == 'product':
                    df_diff.at[index, 'product'] = keyvalue[1]
        # Nếu không phải là chuỗi, gán giá trị None cho cột 'product'
        #df_diff.at[index, 'product'] = None
print(df_diff)
df_diff.to_csv("diff_extract.tsv",sep = "\t", index = False)