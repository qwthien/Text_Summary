import re
import numpy as np
import tkinter as tk
from tkinter import filedialog
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus.reader import wordnet
from nltk.stem import PorterStemmer



# Hàm để chọn tệp đầu vào
def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path if file_path else None

# Hàm để đọc tệp và trích xuất dữ liệu cần thiết
def read_file(file_path):
    output = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r'<s docid="([^"]+)" num="([^"]+)" wdcount="([^"]+)"> (.+?)</s>', line.strip())
            if match:
                docid, num, wdcount, textvalue = match.groups()
                output.append((docid, num, wdcount, textvalue))
    return output

# Xác định tài nguyên và công cụ của NLTK
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Hàm chuyển đổi từ loại câu thành từ loại của WordNet
def get_wordnet_pos(treebank_tag):
    return {
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'N': wordnet.NOUN,
        'R': wordnet.ADV
    }.get(treebank_tag[0], wordnet.NOUN)

# Hàm xử lý văn bản
def process_text(text):
    # Loại bỏ ký tự đặc biệt và tách văn bản thành các từ
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) #thay thế các từ đặc biệt thành ''
    tokens = text.split()   #sau khi loại bỏ các từ đặc biệt phía trên thì ghép các từ lại thành một tokens 
    
    # Loại bỏ stopwords và lemmatize
    lemmatizer = WordNetLemmatizer() #tạo đối tượng WordNetLemmatizer để lemmatize các từ
    #*
    # word: từ, pos: từ loại trong tokens
    # sử dụng thư viện pos_tag(tokens) để gán nhãn từ loại cho các từ trong tokens(key:word; value:pos)(đảm bảo lennatization sẽ đúng cách)
    # kiểm tra từ(word) nếu có nằm trong stop_words hay ko
    #  nếu ko thuộc trong stop_words:
    #   thì thực hiện lemmatization cho từ đó bằng cách gọi lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos))
    # kết qua là ta được 1 tokens mới ko có từ stop_word và đã được biến đổi thành từ ở dạng cơ sở   
    # *#
    tokens = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos)) for word, pos in pos_tag(tokens) if word.lower() not in stop_words]
    
    # Chuyển danh sách các từ trở lại thành một chuỗi
    return ' '.join(tokens)

# Lớp TextClass đại diện cho mỗi đoạn văn bản
class TextClass:
    def __init__(self, docid, num, wdcount, textvalue):
        self.docid = docid
        self.num = num
        self.wdcount = wdcount
        self.textvalue = process_text(textvalue)

# Hàm tính toán PageRank cho đồ thị tương tự
def calculate_page_rank(similarity_matrix, d=0.85, max_iterations=100, epsilon=1e-6):
    N = similarity_matrix.shape[0] #số nút trong đồ thị, tương ứng với kích thước hàng đầu tiên trong ma trận
    page_rank = np.ones(N) / N #khởi tạo pagerank ban đầu cho các nút, gán tất cả các pagerank bằng nhau, vì pagerank sẽ thay đổi
    degree = np.sum(similarity_matrix, axis=0) #Tính tổng các liên kết đến mỗi nút
    for iteration in range(max_iterations):
        previous_page_rank = page_rank.copy() #Sao chép giá trị PageRank từ vòng lặp trước vào previous_page_rank
        for i in range(N): #Vòng lặp này lặp qua từng nút (nút i) trong đồ thị
            inner_sum = sum(similarity_matrix[j][i] * page_rank[j] / max(degree[j], 1) for j in range(N) if i != j)
            page_rank[i] = (1 - d) / N + d * inner_sum #công thức tính page_rank((1-d)/N)+d*(bật hiện tại*)
        if np.all(np.abs(page_rank - previous_page_rank) < epsilon):
            break
    return page_rank

# Hàm xếp hạng các đoạn văn bản
def rank_sentences(texts):
    sentences = [TextClass(docid, num, wdcount, textvalue) for docid, num, wdcount, textvalue in texts]
    size = len(sentences)
    matrix = np.zeros((size, size))
    
    # Xây dựng ma trận kề dựa trên điều kiện
    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = 1
            else:
                words_i = set(sentences[i].textvalue.split())
                words_j = set(sentences[j].textvalue.split())
                if len(words_i.intersection(words_j)) >= 5:
                    matrix[i][j] = 1

    pagerank_scores = calculate_page_rank(matrix)
    sorted_sentences = sorted(sentences, key=lambda x: pagerank_scores[sentences.index(x)], reverse=True)
    
    return [(s.docid, s.num, s.wdcount, s.textvalue) for s in sorted_sentences]

# Hàm loại bỏ các đoạn trùng lặp
def remove_duplicate_sentences(sentence_list):
    seen_sentences = {}
    for docid, num, wdcount, textvalue in sentence_list:
        if textvalue not in seen_sentences:
            seen_sentences[textvalue] = (docid, num, wdcount, textvalue)
    
    return list(seen_sentences.values())


# Hàm để in ra các phần tử trong danh sách
def print_list_elements(lst):
    for element in lst:
        print(element)

# Hàm chính
def main():
    selected_file_path = choose_file()
    input_texts = read_file(selected_file_path)
    ranked_sentences = rank_sentences(input_texts)
    unique_sentences = remove_duplicate_sentences(ranked_sentences)
    print_list_elements(unique_sentences)

if __name__ == "__main__":
    main()
