# Text_Summary
<s docid="AP880911-0016" num="10" wdcount="17"> The storm was approaching from the southeast with sustained winds of 75 mph gusting to 92 mph.</s>
docid: đoạn 
num: vị trí câu trong đoạn
wdcount: tổng số lượng từ có trong câu

'D:/That/NLP/train-20231020T112403Z-001/train/d061j'
 'D:/That/NLP/train-20231020T112403Z-001/d070f'
Bước 1: đọc tệp văn bản có định dạng sau: 
	<s docid="AP880911-0016" num="9" wdcount="28"> Hurricane Gilbert swept toward the Dominican Republic Sunday, and the Civil Defense alerted its heavily populated south coast to prepare for high winds, heavy rains and high seas.</s>
Bước 2: tiến hành xử lý văn bản vừa đọc bằng cách lọc danh sách tag chứa từ khóa tag ví dụ như sau:
	def tienxuly(textfile):
		filter_files = []
		for text in textfiles:
			if "P>" in text:
				continue
			if "TEXT>" in text:
				continue
			if "SUBJECT>" in text:
Tạo 1 lớp đưa các thuộc tính như {docid, num, wdcount, textvalue} để dễ xử lý:
	class TextClass:
		def __init__(self,docid,num,wdcount,textvalue):
			self.docid = docid
			self.num = num
			self.wdcount = wdcount
			self.textvalue = textvalue
Sau khi loại bỏ ký tự thừa trong từng câu: 
	+ Loại bỏ ký tự đặt biệt
	+ Chuyển hoa thành thường
	+ Loại bỏ Stopword
	+ Đưa về từ nguyên mẫu
Ta sẽ tổ hợp thành 1 danh sách các câu trong văn bản.
Bước 3: Sau khi tổ hợp thành một danh sách bao gồm các câu, ta đi tách từ trong câu đó ra.
Bước 4: Đồ thị hóa văn bản và tạo ra một ma trận
	Để đồ thị hóa văn bản: 
		ta quy ước mỗi câu là một đỉnh
		mối quan hệ giữa 2 câu là có nếu chúng có số từ giống nhau >= 2 từ
		nếu 2 câu có mối quan hệ với nhau thì biểu diễn là 1, ngược lại là 0		
	Sau khi có các đỉnh và mối quan hệ giữa các đỉnh, tiến hành tạo ma trận
Bước 5: Sau khi có ma trận, ta tính trọng số của các cạnh.
	Sử dụng thuật toán pagerank để tính trọng số của chúng.
Bước 6: Tiến hành sắp xếp các câu theo trọng số từ cao xuống thấp
Bước 7: thực hiện ghi kết quả trả về và in ra các câu chứa trọng số cao, in toàn bộ câu ban đầu của câu có trọng số cao
