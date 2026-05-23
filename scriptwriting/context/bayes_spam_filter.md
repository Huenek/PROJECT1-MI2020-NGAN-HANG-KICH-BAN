# Tư liệu tham khảo — Bộ lọc Spam bằng Định lý Bayes
# (File MẪU. Thay bằng nội dung deep-research thật của bạn.)

## Khái niệm XSTK cốt lõi cần làm nổi bật
- Xác suất có điều kiện: P(A|B) = P(A∩B) / P(B).
- Định lý Bayes: P(Spam | W) = P(W | Spam) · P(Spam) / P(W).
- Xác suất tiên nghiệm P(Spam) vs. hậu nghiệm P(Spam|W).
- Giả định "naive": độc lập có điều kiện giữa các từ → P(W₁,...,Wₙ|Spam) = Π P(Wᵢ|Spam).

## Liên hệ môn học (đại cương)
- Chương Xác suất có điều kiện & công thức Bayes (XSTK).
- Khái niệm độc lập / độc lập có điều kiện của các biến cố.

## Sự đánh đổi đáng nói
- False Positive (chặn nhầm thư thật) vs. False Negative (lọt spam).
- Bộ lọc tối thiểu hóa False Positive là chính.

## Lưu ý chống lạc đề
- Trọng tâm là CÔNG THỨC BAYES và xác suất có điều kiện, KHÔNG phải kiến trúc hệ thống email.
