# 📄 context_TEMPLATE.md — Mẫu tạo tư liệu tham khảo cho chủ đề mới

Dùng file này làm template khi tạo `context/<slug>.md` cho một chủ đề mới.

---

## Cách dùng

1. **Copy file này** → đặt tên `context/<slug>.md` (ví dụ `context/linear_regression_housing.md`)
2. **Điền nội dung** theo từng section:
   - Title & giới thiệu
   - Khái niệm XSTK cốt lõi (có công thức)
   - Liên hệ môn học
   - Sai lầm thường gặp
   - Ứng dụng tối thiểu
   - Mẹo chống lạc đề
3. **Lưu** → pipeline sẽ tự tìm & dùng

---

## Template

```markdown
# Tư liệu tham khảo — [Tên chủ đề đầy đủ]

*Điền dòng này: Nguồn (ví dụ: Gemini Deep Research ngày X, Giáo trình XSTK chương Y, Bài báo Z)*

## 1. Khái niệm XSTK cốt lõi — CẦN NỀU RÕ CÔNG THỨC

Nêu **3–4 khái niệm chính** của chủ đề, mỗi cái **kèm công thức toán**:

### Khái niệm 1: [Tên]
- **Định nghĩa**: ...
- **Công thức**: ...
- **Ý tưởng**: Cái gì là quan trọng về khái niệm này?

### Khái niệm 2: [Tên]
...

### Khái niệm 3: [Tên]
...

**Ghi chú**: Model sẽ ưu tiên các khái niệm này khi viết kịch bản.

---

## 2. Liên hệ môn học — NỀU RÕ ĐÂY LÀ ĐẠI CƯƠNG

Nêu rõ chủ đề này thuộc **phần nào của XSTK / Toán đại cương**:

- **Chương XSTK**: (ví dụ: Chương 3 "Xác suất có điều kiện & Định lý Bayes")
- **Chương Toán đại cương**: (ví dụ: Đại số tuyến tính, Giải tích, ...)
- **Kỹ năng tiên quyết**: (ví dụ: Phải hiểu biến ngẫu nhiên liên tục, tích phân, ...)
- **Mở rộng**: Chủ đề nào ở những bài sau dùng khái niệm này? (ví dụ: Hồi quy tuyến tính dùng định lý "bình phương nhỏ nhất")

---

## 3. Sai lầm thường gặp khi dạy — CHỐNG LẠC ĐỀ

Nêu **2–3 sai lầm** mà sinh viên hoặc người nói dễ mắc phải. Mỗi cái nêu **lý do tại sao sai**:

### Sai lầm 1
- **Nội dung sai**: [Miêu tả sai lầm]
- **Tại sao sai**: [Giải thích]
- **Đúng là gì**: [Cách nói đúng]

### Sai lầm 2
...

**Ghi chú**: Model sẽ tránh các cách nói sai này.

---

## 4. Ứng dụng tối thiểu — ĐỂ MINH HỌA, KHÔNG SAO CHÉP

Nêu **một bối cảnh thực tế đơn giản** để làm ví dụ:

- **Bối cảnh**: [Ngành / vấn đề]
- **Bài toán cụ thể**: [Nêu con số / dữ liệu cụ thể nếu có]
- **Cách dùng XSTK**: [Nêu tên khái niệm + công thức]
- **Kết quả mong đợi**: [Output của model là gì?]

**Ví dụ**:
```
Bối cảnh: Kiểm soát chất lượng trong xưởng cơ khí

Bài toán: Đục lỗ trục động cơ, đường kính tiêu chuẩn 10mm ± 0.5mm.
Máy có sai số là N(μ, σ²). Cần tìm μ, σ² từ 100 lỗ được đục.

Cách dùng: Ước lượng MLE: μ̂ = (1/n)Σxᵢ, σ̂² = (1/n)Σ(xᵢ - μ̂)²

Kết quả: Nếu μ̂ ≈ 10.02, σ̂ ≈ 0.48 → máy hiệu chỉnh tốt, nằm trong dung sai.
```

**Ghi chú**: Ứng dụng chỉ để **minh họa ý tưởng toán**, KHÔNG phải để kể lể kỹ thuật.

---

## 5. Mẹo chống lạc đề — ĐỌC TRƯỚC KHI SINH

Liệt kê **những cách nói hay xu hướng** mà model dễ rơi vào (rồi bỏ toán):

- ❌ Đừng nói quá nhiều về [chi tiết kỹ thuật nào]
- ❌ Tránh xu hướng [gì] vì nó lấn át lý thuyết
- ✓ Hãy ưu tiên [cái gì] vì đó là trụ cột

**Ví dụ**:
```
❌ Đừng nói quá nhiều về "hệ thống bộ lọc của Gmail" vì nó sẽ len lỏi
❌ Tránh xu hướng "kỹ sư phải optimize tốc độ" vì nó lấn át ý tưởng Bayes
✓ Hãy ưu tiên "cập nhật xác suất từ dữ liệu" vì đó là essence của Bayes
```

---

## Template hoàn chỉnh (ví dụ)

---

# Tư liệu tham khảo — Ước lượng Maximum Likelihood (MLE)

*Nguồn: Gemini Deep Research, Giáo trình XSTK Bách Khoa chương 8*

## 1. Khái niệm XSTK cốt lõi

### Khái niệm 1: Hàm Likelihood L(θ)
- **Định nghĩa**: Hàm mật độ xác suất chung của dữ liệu quan sát, xem như hàm của tham số θ.
- **Công thức**: L(θ | x₁,...,xₙ) = Πᵢ₌₁ⁿ f(xᵢ | θ)
- **Ý tưởng**: Tham số nào làm cho dữ liệu này **có khả năng xảy ra nhất**?

### Khái niệm 2: MLE θ̂ = argmax L(θ)
- **Định nghĩa**: Giá trị θ tối đa hóa likelihood.
- **Công thức**: θ̂ = argmax Πᵢ₌₁ⁿ f(xᵢ | θ), tương đương với argmax ln L(θ)
- **Ý tưởng**: Tìm tham số "hợp lý" nhất từ dữ liệu.

### Khái niệm 3: Bất biến của MLE
- **Tính chất**: Nếu θ̂ là MLE của θ, thì g(θ̂) là MLE của g(θ).
- **Ứng dụng**: Không cần tính lại, chỉ chuyển đổi kết quả.

## 2. Liên hệ môn học

- **Chương XSTK**: Chương 7–8 "Ước lượng điểm & MLE"
- **Chương Toán**: Giải tích (đạo hàm, tìm cực trị), Đại số (ma trận Hessian cho MLE đa biến)
- **Tiên quyết**: Biết biến ngẫu nhiên liên tục, hàm mật độ, logarit
- **Mở rộng**: Hồi quy logistic dùng MLE. Mạng nơ-ron dùng MLE/cross-entropy. Kiểm định giả thuyết dùng likelihood ratio test.

## 3. Sai lầm thường gặp

### Sai lầm 1: Nhầm likelihood với xác suất
- **Nội dung sai**: "Likelihood là xác suất dữ liệu xảy ra khi cho trước θ" (giống định nghĩa xác suất)
- **Tại sao sai**: Likelihood không phải xác suất (L(θ) có thể > 1, không tích phân thành 1)
- **Đúng**: Likelihood là **thước đo mức độ "hợp lý" của tham số θ cho dữ liệu**

### Sai lầm 2: Tìm MLE bằng cách bình phương dữ liệu
- **Nội dung sai**: "Để tối đa hóa L, bình phương từng xᵢ lên"
- **Tại sao sai**: MLE giải qua đạo hàm ∂ln L / ∂θ = 0, không bình phương dữ liệu
- **Đúng**: Logarit likelihood, rồi đạo hàm theo θ, cho bằng 0, giải θ̂

### Sai lầm 3: MLE luôn tốt hơn ước lượng khác
- **Nội dung sai**: "MLE là tốt nhất, luôn dùng MLE"
- **Tại sao sai**: MLE không luôn không chệch, không luôn MVUE
- **Đúng**: MLE có tính chất tiệm cận tốt (consistent, asymptotic normality) nhưng hữu hạn có thể chệch

## 4. Ứng dụng tối thiểu

**Bối cảnh**: Nhà máy ô tô kiểm tra thời gian bảo hành động cơ

- **Bài toán**: Thời gian hỏng hóc tuân theo Exponential(λ). Quan sát 50 cái động cơ, thời gian hỏng: 1200h, 1150h, ..., 1300h. Ước lượng λ.

- **Cách dùng XSTK**: Hàm likelihood L(λ | x₁,...,x₅₀) = λ⁵⁰ e^(-λ Σxᵢ). MLE: λ̂ = 1/x̄

- **Kết quả**: Nếu x̄ = 1250h → λ̂ = 1/1250 = 0.0008 lỗi/giờ → MTBF = 1/λ̂ = 1250h

## 5. Mẹo chống lạc đề

- ❌ Đừng kể quá nhiều về "vòng đời bảo hành" hay "lợi nhuận công ty"
- ❌ Tránh xu hướng "kỹ sư phải quyết định hành động gì" (đó là quyết định, không phải ước lượng)
- ✓ Hãy ưu tiên "tham số λ là gì, MLE là cách tìm λ̂ từ dữ liệu"

---

## Hết template. Bạn có sẵn sàng để sinh!

Lưu file này và chạy:
```bash
python generate.py --only <slug>
```

Pipeline sẽ tự tìm tư liệu của bạn và bơm vào prompt.

---

**Tips**:
- **Càng chi tiết context, càng tốt**: Model sẽ có tư liệu để dựa vào, ít bịa.
- **Vừa phải**: Đừng dài quá (>2KB). Model sẽ quên ở phần cuối.
- **Tập trung vào toán**: Công thức, khái niệm, liên hệ môn học là trụ cột.
- **Reuse**: Nếu 2 chủ đề gần giống (ví dụ: Regression vs Logistic Regression), copy–paste context rồi chỉnh ký 20%.

Xem [WORKFLOW.md](./WORKFLOW.md#thứ-2--planning--tư-liệu) để biết quy trình tạo context hàng tuần.
```
