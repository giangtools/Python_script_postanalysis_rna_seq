import requests

def submit_sequences_to_interpro(sequences):
    # URL của trang web InterPro
    url = "https://www.ebi.ac.uk/interpro/search/sequence/"

    # Lấy HTML của trang web
    response = requests.get(url)
    if response.status_code == 200:
        # Tìm mã HTML của ô nhập trình tự
        input_start_index = response.text.find('<textarea')
        input_end_index = response.text.find('</textarea>', input_start_index)
        input_field = response.text[input_start_index:input_end_index]

        # Lấy giá trị của thuộc tính 'name' của ô nhập trình tự
        name_start_index = input_field.find('name="') + len('name="')
        name_end_index = input_field.find('"', name_start_index)
        input_name = input_field[name_start_index:name_end_index]

        # Tạo payload để gửi các trình tự
        payload = {input_name: sequences}

        # Gửi yêu cầu POST để nhập các trình tự
        response = requests.post(url, data=payload)

        # In kết quả
        print(response.text)
    else:
        print("Failed to retrieve InterPro website.")

# Đọc nội dung của file FASTA
def read_fasta_file(filename):
    sequences = []
    with open(filename, 'r') as file:
        sequence = ''
        for line in file:
            if line.startswith('>'):
                # Lưu trình tự trước đó vào danh sách nếu có
                if sequence:
                    sequences.append(sequence)
                # Bắt đầu một trình tự mới
                sequence = ''
            else:
                # Thêm các dòng không phải tiêu đề vào trình tự
                sequence += line.strip()
        # Lưu trình tự cuối cùng vào danh sách
        if sequence:
            sequences.append(sequence)
    return sequences

# Tên của file FASTA chứa các trình tự
fasta_filename = "D:\\Backup_data_lab\\HP_3192.faa"

# Đọc các trình tự từ file FASTA
sequences = read_fasta_file(fasta_filename)

# Gửi các trình tự đến InterPro
submit_sequences_to_interpro(sequences)
