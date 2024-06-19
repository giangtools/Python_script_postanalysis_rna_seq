import os

def concatenate_tsv_files(directory, output_file):
    # Mở file đầu ra để ghi
    with open(output_file, 'w') as outfile:
        # Lặp qua tất cả các file trong thư mục
        for filename in os.listdir(directory):
            if filename.endswith(".tsv"):
                filepath = os.path.join(directory, filename)
                # Mở và đọc nội dung của file TSV
                with open(filepath, 'r') as infile:
                    # Ghi nội dung của file vào file đầu ra
                    outfile.write(infile.read())
                    # Thêm ký tự xuống dòng vào cuối mỗi file
                    outfile.write('\n')

# Thư mục chứa các file TSV
directory = 'd:\Interproscan\HP_3192'

# Tên của file đầu ra
output_file = 'output.tsv'

# Gọi hàm để nối các file TSV
concatenate_tsv_files(directory, output_file)

print("Đã nối tất cả các file TSV thành công!")
