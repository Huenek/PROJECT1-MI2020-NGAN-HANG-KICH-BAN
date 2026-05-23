# 📋 WORKFLOW — Quy trình làm việc hàng tuần

Hướng dẫn chi tiết cách team vận hành pipeline v2 từ chọn chủ đề → sinh → kiểm → video.

## 📅 Quy trình hàng tuần (5 ngày làm)

```
Thứ 2         Thứ 3–4             Thứ 5               Thứ 6–7
└─ Planning   └─ Sinh & Refine    └─ Video Manim    └─ QA & Phát hành
```

---

## Thứ 2 — Planning & Tư liệu

### 1. Chọn 2–3 chủ đề tuần này
Ví dụ: chọn chủ đề #8, #14, #18 (covariance, MTBF, bootstrap).

### 2. Tạo `context/<slug>.md` cho từng chủ đề

**Bước 1.1**: Dùng Gemini để Deep Research chủ đề
```
Prompt: "Tôi cần soạn kịch bản 2 phút về [tên chủ đề] cho sinh viên XSTK. 
Cho tôi:
- 3 khái niệm XSTK nền tảng cần làm nổi bật (có công thức)
- Liên hệ với bộ môn nào (Xác suất, Thống kê, Đại số...)
- 2–3 sai lầm thường gặp khi dạy chủ đề này
- 1 ứng dụng thực tế đơn giản để làm ví dụ"
```

**Bước 1.2**: Copy kết quả → file `context/covariance_portfolio.md`

**Bước 1.3**: Format sạch, thêm phần nhận xét riêng:
```markdown
# Tư liệu — Ma trận hiệp phương sai trong Danh mục đầu tư

## Khái niệm XSTK cốt lõi
- Hiệp phương sai Cov(X,Y) = E[(X-μₓ)(Y-μᵧ)]
- Tương quan Cor(X,Y) = Cov(X,Y) / (σₓ σᵧ)
- [...]

## Liên hệ môn học
- Chương: Ma trận & Đại số tuyến tính (Đại cương)
- Chương: Phân phối đồng thời (XSTK)

## Sai lầm thường gặp
1. Nhầm hiệp phương sai âm = không liên quan (sai — âm = liên quan nghịch)
2. [...]

## Ứng dụng tối thiểu để dạy
- 2 cổ phiếu A, B; tìm danh mục (w₁A + w₂B) có variance nhỏ nhất
```

Lưu vào `scriptwriting/context/covariance_portfolio.md`.

---

## Thứ 3–4 — Sinh & Cải thiện kịch bản

### Quy trình cho TỪNG chủ đề

**Vòng 1: Sinh bản đầu + chấm lần 1**
```bash
cd scriptwriting
python generate.py --only covariance_portfolio --rounds 2
```

Kỳ vọng output:
```
[*] covariance_portfolio
    context: có
    [round 0] điểm TB = 3.8 | vong_lap_ket_mo=3 neo_ly_thuyet=4 ... | chưa đạt
    [round 1] điểm TB = 4.2 | ... | ĐẠT
    [DONE] lưu bản điểm cao nhất (4.2) -> covariance_portfolio.json
```

**Vòng 2: Kiểm điểm chi tiết (thủ công)**

Đọc `raw_script/reviews/covariance_portfolio_review.json`:
```json
{
  "scores": {
    "vong_lap_ket_mo": 4,
    "neo_ly_thuyet": 4,
    "de_hieu": 5,
    "mach_lac": 4,
    "chieu_sau_dai_cuong": 3,      // ← yếu nhất
    "visual_kha_thi": 4
  },
  "loi_can_sua": [
    "Phần Diễn giải dài dòng kể ứng dụng, nhưng công thức ma trận chưa nổi bật",
    "Tiêu chí 5 yếu: không đủ lý thuyết đại cương"
  ],
  "goi_y_cu_the": "..."
}
```

**Vòng 3: Decide — Đạt hay cần refine thêm?**

Ngưỡng xanh (pass): **TB ≥ 4.0 VÀ tất cả tiêu chí ≥ 3**
- Nếu đạt → lưu vào bảng "chủ đề sẵn sàng cho Manim", ✓ xong.
- Nếu chưa → **option A** (tự động): chạy lại với `--rounds 3`
- Nếu vẫn chưa → **option B** (thủ công): mở `prompts/` sửa module, chạy lại

**Option B** (sửa module):
Nếu lỗi lặp lại trên nhiều chủ đề (ví dụ: tiêu chí 5 "chiều sâu đại cương" luôn yếu),
sửa `prompts/02_theory_anchor.md` để ép hơn, rồi chạy lại:
```bash
python generate.py --force --rounds 2   # sinh lại tất cả với module mới
```

**Bảng tracking** (giữ trong Spreadsheet hoặc file):
```
Chủ đề                  Người      Trạng thái    Điểm TB   Ghi chú
─────────────────────────────────────────────────────────────────
1. Bayes spam filter    Nhân       ✓ Xong       4.5       Ready Manim
2. BER transmission     Anh        ⏳ Refine     3.8       –2 vòng
3. System reliability   Nhân       ✓ Xong       4.3       Ready
...
```

---

## Thứ 5 — Manim & Video

Sau khi kịch bản đạt (4 tiêu chí ≥ 3, TB ≥ 4.0), gửi cho team **Manim**:

**Input cho team Manim:**
- File JSON: `raw_script/<slug>.json`
- Ảnh/icon cần: có `context/<slug>.md` nêu hint
- Thời lượng từng phần: viết cứng trong JSON mỗi key

**Output từ team Manim:**
- Video `.mp4` (1080x1920 dọc, 60fps, tiếng Việt + phụ đề)
- Lưu vào thư mục `videos/<slug>/`

**Team video kiểm:**
- Lời thoại khớp nhịp? (đọc từng section xem độ dài có ok)
- Hình ảnh minh họa sai lệch không?
- Phụ đề chính xác?

---

## Thứ 6–7 — QA & Phát hành

### QA Checklist

Mỗi chủ đề, tổng hợp một file `QA_<slug>.md`:
```markdown
# QA — Covariance Portfolio

## Kịch bản
- [x] Hai hồi kết–mở khớp
- [x] Có công thức ma trận
- [x] Không lạc đề
- [x] Điểm TB ≥ 4.0

## Video
- [x] Lời thoại rõ
- [x] Hình ảnh khớp nội dung
- [x] Phụ đề chính xác
- [x] Độ dài ≤ 2:10

## Excel
- [x] Tên file đúng
- [x] JSON hợp lệ
- [ ] Cập nhật aggregate.xlsx
```

### Phát hành

```bash
# 1. Gom Excel (nếu có >1 chủ đề)
cd scriptwriting
python json_to_excel.py
# → tạo aggregated_scripts.xlsx

# 2. Push lên GitHub
git add raw_script/*.json raw_script/reviews/*.json
git commit -m "v2.0: 3 chủ đề passed QA — covariance, MTBF, bootstrap"
git push origin main

# 3. Upload video lên các platform
# TikTok, YouTube, Facebook, Website (dùng Capcut hoặc OBS)
```

---

## 📊 Ví dụ: Sinh 1 chủ đề từ A–Z

```bash
# ===== Thứ 2: Tạo context =====
# (Dùng Gemini, tạo context/mtbf_estimation.md)

# ===== Thứ 3: Sinh & chấm =====
python generate.py --only mtbf_estimation --rounds 3
# Output: mtbf_estimation.json + review

# Xem điểm:
python3 -c "import json; d=json.load(open('raw_script/reviews/mtbf_estimation_review.json')); print(f\"Điểm TB: {d['final_avg']}\"; print('PASS' if d['passed'] else 'FAIL')"

# ===== Thứ 4: Kiểm thủ công =====
cat raw_script/mtbf_estimation.json | head -30   # xem 2–3 section đầu
# Nếu thiếu gì → chỉnh context, chạy lại: python generate.py --only mtbf_estimation --force

# ===== Thứ 5: Gửi Manim team =====
# Gửi file JSON + review (họ sẽ xem "Neo lý thuyết" để hiểu cái gì cần highlight)

# ===== Thứ 6: QA & Excel =====
python json_to_excel.py                  # nếu có >1 chủ đề
# Xem aggregated_scripts.xlsx

# ===== Thứ 7: Push & phát hành =====
git add raw_script/mtbf_estimation.json raw_script/reviews/mtbf_estimation_review.json
git commit -m "mtbf_estimation: passed v2 quality gate (4.3)"
git push
```

---

## 💡 Tips

- **Bơm context kỹ** — 70% chất lượng tốt đến từ context tốt, 30% tới từ model.
- **Nhanh track** — dùng file Spreadsheet (Google Sheets) để team thấy tiến độ realtime.
- **Tiết kiệm token** — tuần đầu dùng `--rounds 5`, sau đó tối ưu xuống `--rounds 2` khi ổn định.
- **Reuse context** — nếu 2 chủ đề liên quan (ví dụ: Linear Regression + Regression Sensor), copy–paste context rồi chỉnh.

---

## ❓ FAQ

**Q: Chủ đề không qua được vòng nào?**
→ A: Tăng `--rounds` (ví dụ --rounds 5). Hoặc sửa context chi tiết hơn, chạy lại.

**Q: Lỗi "điểm tiêu chí X quá thấp"?**
→ A: Sửa module tương ứng trong `prompts/`, tăng ép hơn. Ví dụ tiêu chí 2 "neo lý thuyết" yếu → sửa `02_theory_anchor.md`.

**Q: Sinh lại hết có mất tiền token không?**
→ A: Có — mỗi lần sinh + chấm tốn token. Cân nhắc số `--rounds`. Để tối thiểu: test 1–2 chủ đề full → nếu ổn thì batch còn lại với `--rounds 2`.

**Q: Có cách nào sinh nhanh để xem kịch bản trước video không?**
→ A: Có — chạy `python generate.py --only <slug> --no-eval`. Bỏ bước chấm → nhanh gấp 3 lần.

---

**Cần help?** → Xem [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) hoặc contact team lead.
