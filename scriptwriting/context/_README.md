# Thư mục context/

Mỗi chủ đề có thể có một file tư liệu tham khảo riêng để bơm vào prompt khi sinh kịch bản,
giúp nội dung bám kiến thức thật thay vì để model tự bịa.

## Quy ước
- Tên file = slug của chủ đề (giống tên file JSON output), đuôi `.md` hoặc `.txt`.
  Ví dụ: `bayes_spam_filter.md`, `mtbf_estimation.md`.
- Nội dung: dán kết quả Gemini Deep Research, trích đoạn giáo trình XSTK, công thức chuẩn,
  ví dụ số liệu đáng tin... — bất cứ thứ gì muốn model dựa vào.
- File là TÙY CHỌN. Nếu không có, pipeline vẫn chạy bình thường (chỉ thiếu phần tư liệu).

## Cách dùng
`generate.py` tự tìm `context/<slug>.md` (rồi `.txt`) và chèn vào prompt dưới mục
`--- TƯ LIỆU THAM KHẢO ---`. Model được dặn ưu tiên thông tin trong tư liệu này khi có mâu thuẫn.

Xem `bayes_spam_filter.md` làm mẫu.
