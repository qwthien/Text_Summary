# Text_Summary
 docid="AP880911-0016" num="10" wdcount="17"> The storm was approaching from the southeast with sustained winds of 75 mph gusting to 92 mph.<br>
docid: đoạn <br>
num: vị trí câu trong đoạn<br>
wdcount: tổng số lượng từ có trong câu<br>

Bước 1: đọc tệp văn bản có định dạng sau: <br>
	 docid="AP880911-0016" num="9" wdcount="28"> Hurricane Gilbert swept toward the Dominican Republic Sunday, and the Civil Defense alerted its heavily populated south coast to prepare for high winds, heavy rains and high seas.<br>
Bước 2: tiến hành xử lý văn bản vừa đọc bằng cách lọc danh sách tag chứa từ khóa tag ví dụ như sau:<br>
	def tienxuly(textfile):<br>
		filter_files = []<br>
		for text in textfiles:<br>
			if "P>" in text:<br>
				continue<br>
			if "TEXT>" in text:<br>
				continue<br>
			if "SUBJECT>" in text:<br>
Tạo 1 lớp đưa các thuộc tính như {docid, num, wdcount, textvalue} để dễ xử lý:<br>
	class TextClass:<br>
		def __init__(self,docid,num,wdcount,textvalue):<br>
			self.docid = docid<br>
			self.num = num<br>
			self.wdcount = wdcount<br>
			self.textvalue = textvalue<br>
Sau khi loại bỏ ký tự thừa trong từng câu: <br>
	+ Loại bỏ ký tự đặt biệt<br>
	+ Chuyển hoa thành thường<br>
	+ Loại bỏ Stopword<br>
	+ Đưa về từ nguyên mẫu<br>
Ta sẽ tổ hợp thành 1 danh sách các câu trong văn bản.<br>
Bước 3: Sau khi tổ hợp thành một danh sách bao gồm các câu, ta đi tách từ trong câu đó ra.<br>
Bước 4: Đồ thị hóa văn bản và tạo ra một ma trận<br>
	Để đồ thị hóa văn bản: <br>
		ta quy ước mỗi câu là một đỉnh<br>
		mối quan hệ giữa 2 câu là có nếu chúng có số từ giống nhau >= 2 từ<br>
		nếu 2 câu có mối quan hệ với nhau thì biểu diễn là 1, ngược lại là 0	<br>	
	Sau khi có các đỉnh và mối quan hệ giữa các đỉnh, tiến hành tạo ma trận<br>
Bước 5: Sau khi có ma trận, ta tính trọng số của các cạnh.<br>
	Sử dụng thuật toán pagerank để tính trọng số của chúng.<br>
Bước 6: Tiến hành sắp xếp các câu theo trọng số từ cao xuống thấp<br>
Bước 7: thực hiện ghi kết quả trả về và in ra các câu chứa trọng số cao, in toàn bộ câu ban đầu của câu có trọng số cao<br>

