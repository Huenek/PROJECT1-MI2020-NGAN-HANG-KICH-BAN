ĐỊNH DẠNG ĐẦU RA — bắt buộc tuyệt đối (downstream sẽ parse JSON tự động, sai format là hỏng):

- Trả về DUY NHẤT một mảng JSON hợp lệ. KHÔNG thêm lời giải thích, KHÔNG bọc trong ```json ... ```.
- Mảng chứa ĐÚNG 1 object.
- Object chứa CHÍNX XÁC 6 key, đúng tên, đúng thứ tự:
  "Tình huống dẫn nhập (5s)"
  "Mô tả bài toán/vấn đề (15s)"
  "Diễn giải/Minh họa (30s)"
  "Tổng kết kiến thức (30s)"
  "Tóm tắt từ khóa (10s)"
  "Gợi ý tiếp theo (10s)"
- Mỗi key chứa ĐÚNG 2 sub-key, đúng tên:
  "Lời thoại (Voice-over)"
  "Đoạn video kết quả kèm câu hỏi (Visuals)"
- Mọi giá trị là chuỗi (string) không rỗng. Không thêm/bớt key nào khác.

Ví dụ khung (chỉ minh họa cấu trúc, KHÔNG sao chép nội dung):
[
  {
    "Tình huống dẫn nhập (5s)": {
      "Lời thoại (Voice-over)": "...",
      "Đoạn video kết quả kèm câu hỏi (Visuals)": "**Mở đầu:** [...]"
    },
    "Mô tả bài toán/vấn đề (15s)": { "Lời thoại (Voice-over)": "...", "Đoạn video kết quả kèm câu hỏi (Visuals)": "**Vấn đề:** [...]" },
    "Diễn giải/Minh họa (30s)": { "Lời thoại (Voice-over)": "...", "Đoạn video kết quả kèm câu hỏi (Visuals)": "**Giải pháp:** [...]" },
    "Tổng kết kiến thức (30s)": { "Lời thoại (Voice-over)": "...", "Đoạn video kết quả kèm câu hỏi (Visuals)": "**Tổng kết:** [...]" },
    "Tóm tắt từ khóa (10s)": { "Lời thoại (Voice-over)": "...", "Đoạn video kết quả kèm câu hỏi (Visuals)": "**Từ khóa:** [...]" },
    "Gợi ý tiếp theo (10s)": { "Lời thoại (Voice-over)": "...", "Đoạn video kết quả kèm câu hỏi (Visuals)": "**Gợi ý:** [...]" }
  }
]
