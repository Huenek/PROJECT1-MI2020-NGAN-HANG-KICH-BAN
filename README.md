# 📺 Ngân hàng kịch bản video — Ứng dụng XSTK vào công nghệ thông tin

Dự án Đại học Bách Khoa Hà Nội (FaMI team) — sinh ra kịch bản, video hoá, phân phối nội dung giáo dục
về **Xác suất Thống kê (XSTK) và các ứng dụng thực tế** trong lĩnh vực CNTT, điện tử, cơ khí...

## 🎯 Mục tiêu

- **Xây dựng kho** kịch bản video 18 chủ đề, mỗi chủ đề ~2 phút, độ sâu kiến thức đại cương.
- **Tự động hoá** sinh kịch bản từ chủ đề → JSON → Excel → video (dùng Manim 3D).
- **Đảm bảo chất lượng**: không lạc đề, neo lý thuyết, không thiên ứng dụng.
- **Workflow linh hoạt**: sinh từng chủ đề, bơm tư liệu riêng, tự cải thiện theo nhận xét AI.

## 📦 Phiên bản

- **v1.0** — Sinh hàng loạt, prompt khối, không kiểm chất lượng.
- **v2.0** ⭐ — Prompt module hoá, sinh từng kịch bản có context, chấm điểm + vòng lặp cải thiện tự động.

## 🚀 Nhanh start

```bash
# 1. Clone repo
git clone https://github.com/[your-org]/MI2020VideoProject.git
cd MI2020VideoProject/scriptwriting

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Thiết lập API key
export GEMINI_API_KEY="your-key-here"

# 4. Sinh 1 chủ đề test (ví dụ: Bayes)
python generate.py --only bayes_spam_filter --rounds 2

# 5. Xem kết quả
cat raw_script/bayes_spam_filter.json
cat raw_script/reviews/bayes_spam_filter_review.json

# 6. Gom toàn bộ vào Excel
python json_to_excel.py
```

Chi tiết xem [SETUP.md](./docs/SETUP.md).

## 📂 Cấu trúc thư mục

```
MI2020VideoProject/
├── docs/                          # Tài liệu dự án (README này)
│   ├── SETUP.md                   # Cài đặt & config
│   ├── WORKFLOW.md                # Quy trình làm việc
│   ├── ARCHITECTURE.md            # Thiết kế v2
│   ├── QUALITY_RUBRIC.md          # Tiêu chí chấm điểm
│   ├── context_TEMPLATE.md        # Mẫu thêm context
│   └── TROUBLESHOOTING.md         # Gỡ lỗi
├── scriptwriting/                 # Pipeline v2
│   ├── generate.py                # Orchestrator chính
│   ├── prompts/                   # Prompt module (7 sinh + 2 đánh giá)
│   ├── context/                   # Tư liệu tham khảo từng chủ đề
│   ├── raw_script/                # Output JSON + reviews/
│   ├── topic.txt
│   ├── sample_script.txt
│   ├── json_to_excel.py
│   └── README_v2.md               # Hướng dẫn scriptwriting riêng
└── README.md                      # (file này)
```

## 📋 Quy trình hàng tuần

1. **Thứ 2**: Chọn 2–3 chủ đề tuần này → tạo `context/<slug>.md` (Deep Research).
2. **Thứ 3–4**: Chạy `generate.py --only <slug> --rounds 3`, kiểm điểm, lặp lại.
3. **Thứ 5**: Video team dựng Manim, QA team chấp thuận.
4. **Thứ 6**: Phân phối (TikTok, YouTube, Facebook, Website).

Chi tiết: [WORKFLOW.md](./docs/WORKFLOW.md).

## 🔑 Tính năng v2

### ✅ Prompt module hoá
- 7 module sinh + 2 module đánh giá → sửa chỉ 1 phần, không phá cái khác.
- `02_theory_anchor.md` ép công thức + ngôn ngữ toán → giải quyết bài toán "kịch bản thiên ứng dụng".

### ✅ Per-topic context injection
- Mỗi chủ đề có `context/<slug>.md` riêng → bơm Gemini Deep Research → model dựa vào thay vì bịa.

### ✅ Auto quality loop
- Sinh → Kiểm schema → Chấm điểm (6 tiêu chí) → Chưa đạt? → Sửa theo nhận xét → Chấm lại.
- Lưu `reviews/<slug>_review.json` ghi lịch sử điểm, giúp team thấy chủ đề nào còn yếu.

### ✅ CLI linh hoạt
```bash
python generate.py --only <slug>      # Lặp 1 chủ đề
python generate.py --force            # Sinh lại toàn bộ
python generate.py --rounds 5         # Tối đa 5 vòng cải thiện
python generate.py --no-eval          # Bản nháp nhanh (bỏ chấm)
```

## 📊 Tiêu chí chấm điểm (6 tiêu chí)

1. **Hai hồi kết–mở** — câu hỏi ở Dẫn nhập được trả lời ở Tổng kết?
2. **Neo lý thuyết** — Có công thức/định lý/khái niệm XSTK tường minh?
3. **Dễ hiểu** — Giải thích rõ ràng, dễ theo dõi?
4. **Mạch lạc** — Các phần nối mạch, dẫn dắt tự nhiên?
5. **Chiều sâu đại cương** — Lấy kiến thức XSTK làm trọng tâm hay thiên ứng dụng?
6. **Visual khả thi** — Mô tả Manim cụ thể, dựng được?

Chi tiết: [QUALITY_RUBRIC.md](./docs/QUALITY_RUBRIC.md).

## 📝 Để bắt đầu

1. Đọc [SETUP.md](./docs/SETUP.md) để cài đặt.
2. Đọc [WORKFLOW.md](./docs/WORKFLOW.md) để hiểu quy trình hàng tuần.
3. Đọc [ARCHITECTURE.md](./docs/ARCHITECTURE.md) để hiểu tại sao v2 thiết kế như vậy.
4. Chạy `python generate.py --only bayes_spam_filter` để test.
5. Xem lỗi? → [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md).

## 🛠️ Công cụ & thư viện

- **Sinh kịch bản**: Gemini 3.1 Pro (API)
- **Xử lý JSON**: Python 3.9+
- **Video**: Manim 0.18.0, Manim-voiceover, gTTS
- **Excel**: openpyxl, pandas
- **Khác**: google-genai, Jupyter Notebook, MikTeX (LaTeX)

## 📈 Tiến độ

- [x] v1.0 — sinh hàng loạt
- [x] v2.0 — prompt module + context + auto-eval + improvement loop
- [ ] v2.1 — tự động sinh visual (agent Manim)
- [ ] v3.0 — full end-to-end (topic → video → publish)


---

**Last updated**: May 2026 | **Maintain by**: FaMI team, HUST
