# ⭐ QUALITY_RUBRIC — 6 Tiêu chí chấm điểm

Giải thích chi tiết từng tiêu chí mà giám khảo AI dùng để chấm kịch bản. Mục đích: team hiểu được "sao kịch bản này bị điểm thấp?" và "cách sửa?"

---

## 1️⃣ Hai hồi kết–mở (Vòng lặp logic)

**Định nghĩa**: Phần "Dẫn nhập" đặt ra một câu hỏi/vấn đề. Phần "Tổng kết" phải **trả lời DỨT ĐIỂM** câu hỏi đó.

### Ví dụ ✓ Tốt

**Dẫn nhập**: "Bạn đã bao giờ tự hỏi làm sao bộ lọc email có thể loại bỏ rác mà không vô tình xóa email quan trọng?"
↓
**Tổng kết**: "Định lý Bayes cho phép hệ thống cập nhật niềm tin từng bước. Mỗi từ khóa mới là bằng chứng → thay đổi xác suất → cuối cùng quyết định đúng. Bộ lọc giảm False Positive (xóa nhầm)."

✓ Câu hỏi "làm sao" được trả lời: **thông qua Bayes + update động**.

### Ví dụ ❌ Yếu

**Dẫn nhập**: "Làm sao quản lý danh mục đầu tư?"
↓
**Tổng kết**: "Ma trận hiệp phương sai giúp ta hiểu mối liên hệ giữa các cổ phiếu. Từ đó chọn trọng số tối ưu."

❌ Câu hỏi là "làm sao quản lý" → tổng kết chỉ giải thích "ma trận giúp hiểu mối liên hệ". **Không trả lời dứt điểm cách quản lý** (thiếu bước tối ưu hóa, không nói rõ output là gì).

### Điểm từng mức

| Điểm | Miêu tả |
|------|---------|
| 5 | Dẫn nhập đặt câu hỏi rõ → Tổng kết trả lời dứt điểm, logic khép kín |
| 4 | Dẫn nhập & tổng kết liên quan, nhưng trả lời không 100% dứt điểm (thiếu chi tiết nhỏ) |
| 3 | Dẫn nhập & tổng kết có quan hệ, nhưng logic còn lỏng, chưa khép kín rõ ràng |
| 2 | Dẫn nhập & tổng kết rời rạc, không rõ liên hệ |
| 1 | Dẫn nhập & tổng kết hoàn toàn không liên quan |

### Cách fix nếu thấp

Nếu điểm tiêu chí 1 < 3:
- Dẫn nhập: đặt **một** câu hỏi cụ thể → không multiple question
- Tổng kết: trước khi viết, tự hỏi "câu hỏi ở dẫn nhập được trả lời chưa?"
- Refine context: thêm ý "kịch bản phải có vòng lặp logic dẫn nhập ↔ tổng kết"

---

## 2️⃣ Neo lý thuyết (Có công thức & ngôn ngữ toán)

**Định nghĩa**: Phần "Diễn giải/Minh họa" **phải chứa** ít nhất một công thức/định lý/khái niệm toán tường minh. Và lời thoại phải dùng **ngôn ngữ toán chính xác** (không nói "trung bình" mà nói "kỳ vọng E[X]").

### Ví dụ ✓ Tốt

**Lời thoại**: "Định lý Bayes tính xác suất có điều kiện: P(Spam|W) = P(W|Spam)·P(Spam) / P(W). Từ công thức này, ta cập nhật xác suất Spam khi biết từ W xuất hiện. Nếu P(Spam|W) > 0.5 → gắn nhãn Spam."

**Công thức**: P(Spam|W) = ... rõ ràng
**Ngôn ngữ**: xác suất có điều kiện, từ khóa (W), Spam ✓

✓ **Điểm cao** — công thức & thuật ngữ toán đều có.

### Ví dụ ❌ Yếu

**Lời thoại**: "Bộ lọc Bayes là một hệ thống thông minh. Nó tính toán 'mức độ spam' của email. Nếu mức độ cao → xóa. Cách tính dựa trên các từ xuất hiện trước đây."

**Công thức**: không có (hoặc ngầm định)
**Ngôn ngữ**: "mức độ spam", "các từ" — không toán học, không tên biến ❌

❌ **Điểm thấp** — kịch bản kể chuyện ứng dụng nhưng thiếu công thức & thuật ngữ.

### Điểm từng mức

| Điểm | Miêu tả |
|------|---------|
| 5 | Công thức rõ (có biến, hệ số, dấu = ), ngôn ngữ 100% toán (biến ngẫu nhiên, phân phối, E, Var, P(A\|B), θ...) |
| 4 | Công thức có, ngôn ngữ 80% toán (một vài chỗ còn "kỳ vọng" thay vì E[X] nhưng chấp nhận được) |
| 3 | Công thức có nhưng hơi mờ, hoặc ngôn ngữ hỗn hợp 50%–50% toán & tiếng Việt thông thường |
| 2 | Công thức chỉ nhắc qua không rõ, ngôn ngữ chủ yếu là kịch bản (dưới 30% toán) |
| 1 | Không có công thức, chỉ kể ứng dụng |

### Cách fix nếu thấp

Nếu điểm tiêu chí 2 < 3:
- **Bước 1**: Dùng Gemini Deep Research → lấy công thức cốt lõi → thêm vào `context/<slug>.md`
  ```
  Công thức mục tiêu: P(Spam|W) = P(W|Spam)·P(Spam) / P(W)
  Tên biến: Spam, W (từ khóa), P(·)
  ```
- **Bước 2**: Sửa lời thoại dùng **tên biến**: "xác suất W cho trước Spam là P(W|Spam)" thay vì "khả năng từ xuất hiện trong spam"
- **Bước 3**: Chạy lại generate.py

---

## 3️⃣ Dễ hiểu (Clarity)

**Định nghĩa**: Mỗi câu có một ý rõ ràng, không rối, không nhảy bước.

### Ví dụ ✓ Tốt

"Phân phối Chuẩn N(μ, σ²) mô tả dữ liệu tập trung quanh μ (trung bình). Nếu σ nhỏ → dữ liệu chặt; nếu σ lớn → dữ liệu rộc. Quy tắc 68–95–99.7: 68% dữ liệu nằm trong [μ–σ, μ+σ]."

✓ Từng câu một bước, không nhảy, không rối.

### Ví dụ ❌ Yếu

"Phân phối Chuẩn là nền tảng của thống kê hiện đại, bắt nguồn từ định lý giới hạn trung tâm khi ta cộng nhiều biến độc lập. Nó gắn liền với ma trận hiệp phương sai, ma trận tương quan, và các tính chất của véc-tơ ngẫu nhiên. Khi có outlier, ta cần chuẩn hoá hoặc dùng phân phối robust khác."

❌ Nhảy từ "định nghĩa" → "CLT" → "ma trận" → "outlier" → quá nhanh, khó theo.

### Điểm từng mức

| Điểm | Miêu tả |
|------|---------|
| 5 | Mỗi câu một ý rõ. Câu sau nối tự nhiên từ câu trước. Không rối, không quá chuyên môn nhưng cũng không sơ sài |
| 4 | Rõ ràng, một vài chỗ hơi nhanh nhưng vẫn theo dõi được |
| 3 | Tạm được, nhưng có vài chỗ rối hoặc nhảy bước |
| 2 | Rối, nhảy bước nhiều, khó theo |
| 1 | Quá rối, không có cấu trúc logic |

### Cách fix nếu thấp

- Đọc lại lời thoại từng phần, tự hỏi "câu này có nối từ câu trước không?"
- Thêm từ nối: "Từ đó...", "Kết quả là...", "Tương tự..."
- Cắt bỏ những ý phụ không cần thiết (chi tiết quá → rối)

---

## 4️⃣ Mạch lạc (Coherence)

**Định nghĩa**: 6 phần liên kết với nhau một cách tự nhiên, từng phần là tiền đề cho phần sau.

### Ví dụ ✓ Tốt

```
1️⃣ Dẫn nhập: "Làm sao hệ thống quản lý hàng đợi xử lý request trong đêm Black Friday?"
↓ (Tại sao cần chủ đề này)
2️⃣ Mô tả: "Cách truyền thống: FIFO queue. Nhưng không biết thời gian phục vụ → không dự báo được độ dài hàng đợi"
↓ (Tại sao cách cũ thất bại)
3️⃣ Diễn giải: "Phân phối Exponential mô tả thời gian chờ: X ~ Exp(λ). Kỳ vọng = 1/λ"
↓ (Công cụ giải quyết)
4️⃣ Tổng kết: "Với mô hình Exponential, hệ thống dự báo được thời gian xử lý → tối ưu hàng đợi → khỏi bị sập"
↓ (Kết quả)
5️⃣ Từ khóa: Exponential, Thời gian chờ, FIFO
↓ (Khôi lại 3 khái niệm chính)
6️⃣ Gợi ý: "Ứng dụng tương tự: phân phối trong bệnh viện (thời gian khám), cửa hàng (thời gian kiểm tra)"
```

✓ 6 phần liên kết từng cái một, từng bước logic.

### Ví dụ ❌ Yếu

```
1️⃣ Dẫn nhập: "Phân phối Exponential là gì?"
↓
2️⃣ Mô tả: "Có 3 loại phân phối: Poisson, Exponential, Normal"
↓
3️⃣ Diễn giải: "Phân phối Normal là..."
```

❌ Dẫn nhập hỏi "Exponential là gì" nhưng phần 2 liệt kê 3 loại, phần 3 lại nói Normal → **không mạch lạc, rối**.

### Điểm từng mức

| Điểm | Miêu tả |
|------|---------|
| 5 | 6 phần dẫn dắt nhau một cách tự nhiên, từng phần làm nền tảng cho phần sau |
| 4 | Hầu hết liên kết tốt, một vài chỗ hơi gập gáp |
| 3 | Có liên kết nhưng chưa suôn sẻ, vài chỗ bị nhảy |
| 2 | Một vài phần liên kết, chủ yếu rời rạc |
| 1 | Gần như không liên kết, chỉ là danh sách 6 ý |

---

## 5️⃣ Chiều sâu đại cương (Trọng tâm XSTK)

**Định nghĩa**: Kịch bản lấy **kiến thức XSTK làm trọng tâm**, ứng dụng chỉ là ví dụ minh họa. Không thiên ứng dụng đến độ bỏ lý thuyết.

### Ví dụ ✓ Tốt

"Nhắc lại: xác suất có điều kiện P(A|B) = P(A∩B)/P(B). **Định lý Bayes suy ra từ công thức này**: P(A|B) = P(B|A)·P(A)/P(B). Ý tưởng **cốt lõi** là **cập nhật niềm tin từ dữ liệu mới**. Trong ứng dụng email, chữ 'spam' là **dữ liệu mới** → **cập nhật xác suất spam** → **quyết định**."

✓ Trọng tâm: định lý Bayes + công thức + ý tưởng cập nhật.
ứng dụng (email, từ 'spam') chỉ là ví dụ để minh họa ý tưởng.

### Ví dụ ❌ Yếu

"Google cần lọc spam để bảo vệ người dùng. Hàng triệu email đến mỗi ngày. Kỹ sư phải thiết kế hệ thống nhanh và chính xác. Google dùng bộ lọc Bayes: lên các từ khóa từ những email rác trước đó, rồi quét email mới. Nếu trùng từ khóa → gắn nhãn spam."

❌ 80% nội dung kể về **hệ thống Google, yêu cầu kỹ sư**. Chỉ đề cập "bộ lọc Bayes" một lần, không giải thích công thức hay ý tưởng **cập nhật xác suất**.

### Điểm từng mức

| Điểm | Miêu tả |
|------|---------|
| 5 | XSTK/toán là trọng tâm (70%+). Ứng dụng minh họa (30%) nhưng không lấn át |
| 4 | XSTK là trọng tâm (60%+), ứng dụng hợp lý (40%) |
| 3 | Cân bằng ~50%–50%, không thiên nặng một bên |
| 2 | Ứng dụng nhiều hơn XSTK (40% toán, 60% ứng dụng) |
| 1 | Chủ yếu ứng dụng (20% toán, 80% ứng dụng khi chi tiết) |

### Cách fix nếu thấp

- **Check**: Nếu xóa tên công ty/sản phẩm ra mà kịch bản vẫn đơn giản & đúng → **tốt** (lý thuyết là trụ)
- **Nếu**: Xóa tên công ty mà kịch bản "mất hết ý" → **sửa**: thêm công thức, ý tưởng toán vào
- **Phần lỗi nhất**: Phần "Diễn giải" → **phải có công thức + ý tưởng toán**, không phải chỉ kỹ thuật

---

## 6️⃣ Visual khả thi (Manim Implementation)

**Định nghĩa**: Mô tả hình ảnh (sub-key "Visuals") **cụ thể**, **dựng được** bằng Manim, và **bám đúng** lời thoại của cùng phần.

### Ví dụ ✓ Tốt

**Lời thoại**: "Xác suất có điều kiện chia không gian thành hai vùng: sự kiện A xảy ra (xanh), không xảy ra (xám). Xác suất P(B|A) là tỷ lệ phần B trong vùng A."

**Visual**: "Manim: Vẽ hình vuông (không gian Ω). Phần xanh chiếm 40% (sự kiện A). Trong đó, phần xanh sẫm (A∩B) chiếm 25% toàn bộ. P(B|A) = 25/40 = 0.625. Camera zoom vào vùng xanh, highlight vùng xanh sẫm, hiển thị tỷ lệ."

✓ Cụ thể (hình vuông, %...), dựng được (Venn diagram trong Manim), bám lời (chia không gian = vùng xanh).

### Ví dụ ❌ Yếu

**Lời thoại**: "Xác suất là một khái niệm trừu tượng."

**Visual**: "Hình ảnh minh họa đẹp mắt về xác suất."

❌ "Hình ảnh minh họa" quá mơ hồ, không nói được lấy gì dựng, Camera như thế nào, hay nói chung là "dựng được không" cũng chưa biết.

### Điểm từng mức

| Điểm | Miêu tả |
|------|---------|
| 5 | Cụ thể (nêu kiểu đối tượng Manim: hình vuông, trục, mặt cong..., chuyển động, màu...). Dựng được rõ ràng. Bám lời thoại 100% |
| 4 | Cụ thể 80%, dựng được, bám lời ~90% |
| 3 | Hơi mơ hồ, nhưng vẫn tạm dựng được, bám lời ~80% |
| 2 | Mơ hồ, khó dựng, bám lời không rõ |
| 1 | Quá mơ hồ, không biết dựng gì |

### Cách fix nếu thấp

- **Ý tưởng**: Trước khi viết visual, **tự dựng mẫu Manim** nhỏ (hoặc vẽ sketch trên giấy)
- **Chi tiết**: Nêu rõ:
  - Loại đối tượng (lò xo hình elip, đồ thị hàm, vector, khối...)
  - Màu + ý nghĩa (xanh = dữ liệu tốt, đỏ = ngoại lệ, ...)
  - Chuyển động (rotate, zoom, fade in, ...)
  - Camera (zoom, pan, view 3D hay 2D)
- **Phần nguy hiểm**: Sub-key "Visuals" chỉ nên 1–2 câu **mô tả cụ thể**, không phải 5 câu rông hoa

---

## 📊 Bảng tóm tắt: cách fix từng tiêu chí

| Tiêu chí | Khi thấp (< 3) | Cách fix |
|----------|----------------|---------|
| 1 — Hai hồi | Dẫn nhập & tổng kết rời | Thêm câu hỏi rõ ở (1), trả lời dứt ở (4) |
| 2 — Neo lý | Thiếu công thức, quá ứng dụng | Thêm `context/<slug>` với công thức. Dùng tên biến (X, P(A\|B), E[X]...) |
| 3 — Dễ hiểu | Nhảy bước, rối | Sửa lời thoại: câu nào không có từ nối? Cắt chi tiết thừa |
| 4 — Mạch lạc | 6 phần rời rạc | Kiểm: phần N là nền tảng cho phần N+1 chưa? Thêm từ nối (Từ đó, Như vậy...) |
| 5 — Đại cương | Quá ứng dụng, thiếu XSTK | Sửa `02_theory_anchor.md` ép công thức hơn. Hoặc refine lời thoại: `P(Spam\|W) = ...` thay vì "tính mức độ" |
| 6 — Visual | Quá mơ hồ, không rõ dựng gì | Chi tiết: Manim object nào? Màu gì? Rotate hay fade? Camera zoom bao nhiêu? |

---

## 🎯 Golden rule

Khi chấm điểm, **tiêu chí 2 (Neo lý thuyết) và 5 (Đại cương)** nặng nhất. Nếu cả hai < 3 → kịch bản thất bại cơ bản (là ứng dụng, không phải XSTK). Khác:
- Tiêu chí 1, 3, 4, 6 yếu → dễ sửa (ở mức lời thoại / hình ảnh)
- Tiêu chí 2, 5 yếu → phải sửa deep (nội dung & chiến lược)

---

Xem [WORKFLOW.md](./WORKFLOW.md) để biết cách sửa khi điểm yếu.
