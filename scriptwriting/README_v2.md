# Ngân hàng kịch bản — v2

Nâng cấp từ v1 (sinh hàng loạt, prompt khối, không kiểm chất lượng) sang quy trình:
**prompt module hoá → sinh từng kịch bản có tư liệu → chấm điểm → tự cải thiện theo nhận xét.**

Giữ nguyên schema JSON (6 phần + 2 sub-key) nên `json_to_excel.py` chạy không cần sửa.

## Cấu trúc thư mục
```
scriptwriting/
├── generate.py              # orchestrator v2 (thay cho aigenerate.py)
├── prompts/                 # prompt tách module — sửa từng phần độc lập
│   ├── 00_role.md           # vai trò: giảng viên XSTK, ưu tiên lý thuyết
│   ├── 01_structure.md      # 6 phần + yêu cầu "hai hồi kết–mở"
│   ├── 02_theory_anchor.md  # NEO LÝ THUYẾT — đòn bẩy chất lượng chính
│   ├── 03_visual_manim.md   # quy tắc mô tả hình ảnh Manim
│   ├── 04_length_budget.md  # ngân sách độ dài gắn với thời lượng phân cảnh
│   ├── 05_constraints.md    # điều cấm (lạc đề, lan man, thiên ứng dụng)
│   ├── 06_output_format.md  # hợp đồng JSON chặt
│   ├── judge.md             # rubric chấm điểm
│   └── revise.md            # hướng dẫn sửa theo nhận xét
├── context/                 # tư liệu tham khảo từng chủ đề (tùy chọn)
│   ├── _README.md
│   └── <slug>.md            # vd: bayes_spam_filter.md
├── topic.txt                # giữ nguyên
├── sample_script.txt        # giữ nguyên
└── raw_script/              # output: <slug>.json + reviews/<slug>_review.json
```

## Cài đặt
```bash
pip install google-genai openpyxl pandas
export GEMINI_API_KEY="..."     # bắt buộc
export GEN_MODEL="gemini-3.1-pro-preview"   # tùy chọn
export JUDGE_MODEL="..."         # tùy chọn — đặt model rẻ hơn để tiết kiệm token
```

## Dùng
```bash
python generate.py                       # sinh mọi chủ đề, bỏ qua file đã có
python generate.py --force               # sinh lại tất cả
python generate.py --only mtbf_estimation   # chỉ một chủ đề (workflow lặp từng cái)
python generate.py --rounds 3            # tối đa 3 vòng cải thiện
python generate.py --no-eval             # bản nháp nhanh, bỏ chấm điểm
python generate.py --pass 4.2            # nâng ngưỡng đạt
```
Sau đó vẫn chạy `python json_to_excel.py` như cũ để gom Excel.

## Quy trình mỗi chủ đề
1. **Sinh** — ghép `prompts/` + chủ đề + `context/<slug>` (nếu có) + mẫu → gọi model.
2. **Kiểm schema** — sai cấu trúc thì tự nhắc lỗi và sinh lại (tối đa 3 lần).
3. **Chấm điểm** — giám khảo cho điểm 6 tiêu chí (1–5) + lỗi cụ thể + gợi ý sửa.
   Đạt khi: điểm TB ≥ ngưỡng VÀ không tiêu chí nào < 3.
4. **Cải thiện** — chưa đạt thì sửa theo nhận xét rồi chấm lại, tới `--rounds` vòng.
   Cuối cùng lưu **bản điểm cao nhất**, kèm `<slug>_review.json` ghi lịch sử điểm.

## Tinh chỉnh chất lượng
- Kịch bản còn "kể ứng dụng", thiếu toán → sửa `prompts/02_theory_anchor.md`.
- Đổi tiêu chí/độ khắt khe khi chấm → sửa `prompts/judge.md`.
- Bơm kiến thức chuẩn cho một chủ đề → thêm `context/<slug>.md` (dán Gemini Deep Research).
- Tiết kiệm token: đặt `JUDGE_MODEL` rẻ hơn, hoặc `--rounds 1`, hoặc `--no-eval` cho bản nháp.

## Lưu ý: nên sửa luôn `json_to_excel.py`
File hiện đang **hard-code đường dẫn tuyệt đối** `/Users/doanvinhnhan/...` và sai hoa/thường
(`Scriptwriting` vs `scriptwriting`) → chỉ chạy được trên một máy. Nên đổi sang đường dẫn tương đối
giống `generate.py` (dùng `os.path.dirname(__file__)`) để cả nhóm chạy được.
File review giờ nằm ở `raw_script/reviews/` nên converter (chỉ quét `.json` trong `raw_script/`)
không gom nhầm.
