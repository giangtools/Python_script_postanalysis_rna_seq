import os
import pandas as pd
folder_path = ''

#Columns list for dataframe
columns = ['draft_genome_1', 'draft_genome_2', 'draft_genome_3']

#Create a empty dataframe
df_path = pd.DataFrame(columns=columns)

#Scan every folder and file in root
for root, dirs, file in os.walk(folder_path):
    if file.endswith('.fasta'):
        genome_name = os.path.basename(root)
        file_path = os.path.join(root,file)
        with open(file_path, 'r') as f:
            data = f.read()
            if genome_name in df.columns:
                    df[genome_name].append(data)
            else:
                    df[genome_name] = [data]
                    
                    
df.to_excel("Output_df_path_test_rgi.xlsx", index=False)