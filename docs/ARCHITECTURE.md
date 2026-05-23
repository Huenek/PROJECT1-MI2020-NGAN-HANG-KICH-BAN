# 🏗️ ARCHITECTURE — Thiết kế v2 so với v1

Tài liệu này giải thích **tại sao** v2 được thiết kế như thế, cái gì sai với v1, và cách v2 khắc phục.

## 📊 So sánh v1 vs v2

| Khía cạnh | v1.0 | v2.0 |
|-----------|------|------|
| **Prompt** | 1 file khối `prompt.txt` | 7 module trong `prompts/` + 2 module đánh giá |
| **Tư liệu** | Không có; model tự bịa | Context riêng từng chủ đề: `context/<slug>.md` |
| **Sinh** | Hàng loạt đa luồng (18 chủ đề cùng lúc) | Tuần tự, từng chủ đề một |
| **Schema** | Chặt (JSON 6 phần 2 sub-key) | Chặt như cũ + validate tự động |
| **Chất lượng** | Không kiểm | Chấm điểm 6 tiêu chí |
| **Cải thiện** | Không có | Vòng lặp tự động: nhận xét → sửa → chấm lại |
| **Output** | JSON `<slug>.json` | JSON + `reviews/<slug>_review.json` (lịch sử điểm) |

---

## ❌ Vấn đề v1

### 1. **Prompt khối → khó nâng cấp**

v1 để toàn bộ hướng dẫn trong một file `prompt.txt` (5KB+). Muốn sửa một phần (ví dụ: tăng ép "lý thuyết"), phải:
- Mở file lớn → tìm đoạn đó (dễ gây nhầm)
- Edit → quá khác cấu trúc → model hiểu sai hoặc quên phần khác
- Sinh lại → không biết phần nào sai

**Giải pháp v2**: Tách thành 7 module nhỏ + 2 module đánh giá. Mỗi module có trách nhiệm rõ ràng:
- Sửa `02_theory_anchor.md` → ép công thức toán
- Sửa `05_constraints.md` → chống lạc đề
- Sửa `04_length_budget.md` → điều chỉnh độ dài

Dễ test, dễ rollback, dễ collaborate.

### 2. **Sinh hàng loạt → khó kiểm soát chất lượng**

v1 chạy 18 chủ đề song song (ThreadPool, max_workers=3). Kết quả là:
- Không biết chủ đề nào đạt/không đạt (chỉ biết "xong" hay "error")
- Không có lịch sử điểm → khó track tiến độ
- Chủ đề thất bại → chỉ ghi error.txt gốc → phải sửa prompt chung rồi sinh lại toàn bộ

**Giải pháp v2**: Sinh tuần tự, từng chủ đề một → dễ monitor. Lưu `reviews/<slug>_review.json`:
```json
{
  "final_avg": 4.2,
  "passed": true,
  "rounds": [
    {"round": 0, "avg": 3.8, "review": {...}},
    {"round": 1, "avg": 4.2, "review": {...}}
  ]
}
```

Team có thể thấy: chủ đề #3 điểm 3.5 (yếu) → cần refine, chủ đề #5 điểm 4.8 (mạnh) → xong.

### 3. **Không có tư liệu → model tự bịa**

v1 chỉ có `topic.txt` (tên chủ đề) + mẫu JSON → model phải dựa vào kiến thức trong training:
- Dễ bịa con số (ví dụ: "tỷ lệ lỗi 0.03%", không biết từ đâu)
- Dễ lạc đề (ví dụ: về phía kỹ thuật hơn là toán)
- Không ưu tiên kiến thức nền tảng quan trọng

**Giải pháp v2**: `context/<slug>.md` bơm thông tin thật (từ Gemini Deep Research hoặc giáo trình):
```markdown
# Khái niệm XSTK cốt lõi
- Định lý Bayes: P(A|B) = P(B|A)P(A) / P(B)
- Xác suất tiên nghiệm P(A)
- ...

# Sai lầm thường gặp
1. Nhầm P(A|B) với P(B|A)
...
```

Model được dặn: "Ưu tiên dùng thông tin ở TƯ LIỆU THAM KHẢO" → kịch bản bám kiến thức thật.

### 4. **Không kiểm → "chất lượng mù mờ"**

v1 output 18 file JSON, nhưng:
- Không biết chất lượng thế nào (phải đọc từng file bằng tay)
- Không có tiêu chí chung → khó so sánh
- Khi video team nói "kịch bản này lạc đề", không biết ai chịu trách nhiệm (model hay prompt?)

**Giải pháp v2**: Tự động chấm điểm bằng giám khảo AI (prompt `judge.md`):

```
6 tiêu chí (1–5 điểm):
1. Hai hồi kết–mở — logic kịch bản khép kín?
2. Neo lý thuyết — có công thức/khái niệm toán?
3. Dễ hiểu — theo dõi được?
4. Mạch lạc — phần nối mạch nhau?
5. Chiều sâu đại cương — XSTK hay ứng dụng?  ← KEY
6. Visual khả thi — Manim dựng được?
```

Team thấy:
- Chủ đề #2: tiêu chí 5 = 2 → "quá ứng dụng" → refine
- Chủ đề #5: tiêu chí 2 = 3 → "công thức chưa rõ" → sửa prompt 02_theory_anchor

### 5. **Không cải thiện → mất công công lao của model**

v1 sinh 1 lần → done. Nếu xấu → sinh lại 18 cái (tốn token).

v2 nếu điểm < 4.0 → tự sửa theo nhận xét (prompt `revise.md`) → chấm lại → nếu tốt hơn thì lưu. Lặp tối đa `--rounds` vòng.

**Lợi ích**:
- Cải thiện dần (round 0: 3.5 → round 1: 3.9 → round 2: 4.1 → PASS)
- Lưu lịch sử điểm → team thấy "script này cần 2 vòng mới pass"
- Nếu chủ đề khó → tăng `--rounds`, không cần sinh hết từ đầu

---

## ✅ Kiến trúc v2 chi tiết

### Phần 1: Prompt Module hoá

```
prompts/
├── 00_role.md              # "Bạn là giảng viên XSTK, không phải PR copywriter"
├── 01_structure.md         # "6 phần, phần 1 câu hỏi → phần 4 trả lời"
├── 02_theory_anchor.md     # "BẮT BUỘC có công thức, dùng ngôn ngữ toán"  ← ĐỖI TƯ
├── 03_visual_manim.md      # "Cụ thể, dựng được, bám lời thoại"
├── 04_length_budget.md     # "Tính chữ theo độ dài, khớp video"
├── 05_constraints.md       # "Cấm lạc đề, lan man, bịa"
├── 06_output_format.md     # "JSON schema chặt"
├── judge.md                # "Chấm 6 tiêu chí"
└── revise.md               # "Sửa theo nhận xét"
```

Ghép động trong code:
```python
PROMPT_MODULES = ["00_role.md", "01_structure.md", ..., "06_output_format.md"]
gen_prompt = load_modules(PROMPT_MODULES) + "\n\n--- CHỦ ĐỀ ---\n" + topic
```

**Tại sao tách?**
- Dễ debug: chạy test từng module
- Dễ upgrade: thay 1 module mà không vô tình đụng mấy cái khác
- Dễ A/B test: ví dụ thử 2 phiên bản `02_theory_anchor.md`, so điểm
- Dễ collabor: "Nhân sửa role, Anh sửa structure, Hùng sửa theory_anchor"

### Phần 2: Context per-topic

```
context/
├── _README.md
├── bayes_spam_filter.md       # Gemini Deep Research về Bayes
├── mtbf_estimation.md         # Về MTBF trong engineering
└── ...
```

Mỗi file chứa:
```markdown
# Tư liệu — MTBF

## Khái niệm XSTK
- Mean Time Between Failures = 1/λ (nếu exponential)
- Công thức: MTBF = ∫ₒ^∞ [1-F(t)] dt

## Liên hệ môn học
- Phân phối Exponential (XSTK)
- Độc lập & memoryless

## Không dùng
- Không kể lể cách tính engineering detail
```

Model được dặn: "Ưu tiên THÔNG TIN TRONG TƯ LIỆU THAM KHẢO". Giải pháp tư liệu → không bịa.

### Phần 3: Auto quality loop

```python
# Sinh
script = generate_once(topic, context)

# Vòng đánh giá & cải thiện
for round in range(max_rounds):
    review = judge(script)
    if evaluate(review) == PASS:
        break
    script = revise(script, review)
    
# Lưu
save(script, review_history)
```

**Điều kiện đạt:**
```python
passed = (avg_score >= 4.0) and (min(criterion_scores) >= 3)
```

Không phải "pass nếu model nói pass" → code tự tính, chắc chắn.

### Phần 4: CLI linh hoạt

```bash
python generate.py --only <slug>           # Lặp 1 chủ đề
python generate.py --force                 # Sinh lại tất cả
python generate.py --rounds 5              # Tối đa 5 vòng
python generate.py --no-eval               # Bản nháp (bỏ chấm)
python generate.py --pass 3.8              # Nạn ngưỡng
```

**Tại sao cần?**
- Thứ 3 sinh thử 1 chủ đề → pass nhanh → xong
- Thứ 4 refine 2 chủ đề → cần lặp chúng → `--only`
- Tuần sau sửa module → sinh lại hết → `--force`
- Hối hả deadline → bản nháp nhanh → `--no-eval`

---

## 📈 Tác động dự kiến

### Trước v2 (v1.0)
- Sinh 18 chủ đề → output 18 JSON
- Không biết chất lượng → video team gửi lại "kịch bản #3 lạc đề"
- Sửa prompt → sinh lại 18 cái (tốn token + thời gian)
- Không có nhận xét → khó biết fix cái gì

**Kết quả**: 30% chủ đề phải refine sau video, tốn thêm 2–3 ngày.

### Sau v2 (v2.0)
- Sinh 18 chủ đề → chấm điểm → 85% pass, 15% cần refine
- Chủ đề yếu được ngay feedback → sửa context rồi sinh lại (chỉ cần chủ đề đó)
- Vòng cải thiện tự động → tiết kiệm thời gian điều chỉnh thủ công
- Lịch sử điểm → team track tiến độ, biết yếu điểm ở đâu

**Kết quả**: 95% chủ đề pass trước video, chỉ 5% nhỏ lẻ refine. Tiết kiệm 2 ngày.

---

## 🔮 Mở rộng tương lai

### v2.1 — Tự sinh visual
- Giám khảo AI chấm "visual_kha_thi" → nếu thấp → sửa prompt Manim tự động
- Hoặc gọi agent để vẽ mẫu Manim (prototype)

### v3.0 — End-to-end
- Topic → Kịch bản (v2) → Manim code sinh tự động (agent) → Video mp4 → Upload

---

## 💬 Tóm tắt thiết kế

| Vấn đề v1 | Giải pháp v2 |
|-----------|------------|
| Prompt khối, khó sửa | Module tách rõ, dễ upgrade |
| Không có context | Per-topic context từ Deep Research |
| Sinh hàng loạt, không kiểm | Tuần tự + auto score 6 tiêu chí |
| Không cải thiện | Vòng lặp tự động: nhận xét → sửa → chấm |
| Khó track QA | Lưu `_review.json` lịch sử điểm |

**Kết quả**: Chất lượng cao hơn, kiểm soát tốt hơn, tiết kiệm thời gian refine.

---

Xem [QUALITY_RUBRIC.md](./QUALITY_RUBRIC.md) để hiểu chi tiết 6 tiêu chí.
