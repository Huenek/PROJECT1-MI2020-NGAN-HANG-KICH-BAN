# 🔧 TROUBLESHOOTING — Gỡ lỗi thường gặp

Hướng dẫn fix những lỗi mà team sẽ gặp khi chạy v2.

---

## ❌ Setup & API

### "ModuleNotFoundError: No module named 'google'"

**Nguyên nhân**: Chưa cài package `google-genai`.

**Fix**:
```bash
pip install google-genai
# hoặc
pip install -r requirements.txt
```

---

### "GEMINI_API_KEY not set" hoặc "Please set GEMINI_API_KEY"

**Nguyên nhân**: Biến môi trường chưa được export.

**Fix** — kiểm tra:
```bash
echo $GEMINI_API_KEY   # nếu trống → không được set
```

**Đặt lại**:
```bash
# macOS / Linux
export GEMINI_API_KEY="your-actual-key"

# Windows PowerShell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-actual-key", "User")

# Windows CMD
setx GEMINI_API_KEY "your-actual-key"
```

Reload terminal / PowerShell rồi kiểm lại.

---

### "gRPC failed with status=UNAUTHENTICATED"

**Nguyên nhân**: API key sai hoặc hết quota.

**Fix**:
1. Kiểm tra API key (vào https://aistudio.google.com/u/0/app/apiDashboard)
   - Có đúng key không? Copy lại từ đó.
   - Quota còn không? (mặc định Google cho 60 calls/phút miễn phí)
2. Nếu quota hết → đợi 1 phút hoặc setup billing

---

### "socket timeout" khi gọi API

**Nguyên nhân**: Mạng chậm, bị block, hoặc server không phản hồi.

**Fix**:
```bash
# Kiểm tra kết nối
curl https://generativelanguage.googleapis.com/ -v

# Nếu timeout → mạng có issue (kiểm tra VPN, firewall)
# Hoặc thử dùng model khác:
export GEN_MODEL="gemini-3.1-sonnet-preview"
python generate.py --only bayes_spam_filter
```

---

## ❌ Schema & JSON

### "Không parse được JSON" hoặc "format retry 3/3"

**Nguyên nhân**: Model trả về lệch schema (thiếu key, sai cấu trúc).

**Fix**:
1. Xem raw response: thêm debug logging trong `generate.py` (ở hàm `extract_json`):
   ```python
   print("RAW:", raw[:200])  # xem 200 chữ đầu
   ```
2. Nếu model thường bị lệch → sửa prompt: `06_output_format.md` ép hơn (thêm ví dụ JSON)
3. Hoặc giảm temperature (từ 0.7 xuống 0.5) để model bảo thủ hơn:
   ```python
   # Trong generate.py, hàm call_model
   config=types.GenerateContentConfig(temperature=0.5)
   ```

---

### "Thiếu key phần 'Diễn giải/Minh họa'"

**Nguyên nhân**: Model quên hoặc bỏ một key trong schema.

**Fix**:
1. Kiểm tra `06_output_format.md` — có đầy đủ 6 key không?
2. Sửa lời nhắc: thêm "ĐÚNG XÁC 6 key" (Gemini thích chữ in hoa)
3. Chạy lại với `--force --rounds 3` (3 vòng cải thiện để model học)

---

## ❌ Chất lượng & Scoring

### "Điểm tiêu chí X thấp" (ví dụ: neo_ly_thuyet = 2)

**Nguyên nhân**: Model chưa nhận ra tiêu chí đó cần gì.

**Fix** — tùy tiêu chí:

**Nếu tiêu chí 2 "neo lý thuyết" thấp** (công thức, ngôn ngữ toán):
```
1. Sửa context/<slug>.md: thêm công thức cốt lõi rõ ràng
2. Sửa prompts/02_theory_anchor.md: ép hơn ("BẮT BUỘC có công thức")
3. Chạy: python generate.py --only <slug> --rounds 3
```

**Nếu tiêu chí 5 "chiều sâu đại cương" thấp** (quá ứng dụng):
```
1. Sửa context/<slug>.md: thêm mục "Mẹo chống lạc đề"
2. Sửa prompts/05_constraints.md: thêm "Ứng dụng chỉ minh họa, KHÔNG chi tiết kỹ thuật"
3. Chạy lại
```

**Nếu tiêu chí 1 "hai hồi kết–mở" thấp** (logic không khép):
```
1. Đọc lại dẫn nhập & tổng kết (file `.json`)
2. Sửa thủ công nếu cần (sửa trực tiếp `.json` trong `raw_script/`)
3. Hoặc chạy: python generate.py --only <slug> --force --rounds 2
```

---

### "Lặp lại 3 vòng nhưng vẫn không tăng điểm"

**Nguyên nhân**: Vấn đề sâu → cần sửa prompt/context, không phải model tự fix được.

**Fix**:
1. **Kiểm prompt**: Xem `prompts/02_theory_anchor.md` hay `05_constraints.md` có rõ không?
2. **Kiểm context**: `context/<slug>.md` có đầy đủ công thức & không gợi ý sai không?
3. **Sửa rồi sinh lại**:
   ```bash
   # Sửa file .md
   python generate.py --only <slug> --force --rounds 3
   ```
4. **Nếu vẫn không tăng** → hỏi team lead hoặc tạo issue GitHub

---

### "Điểm cao nhưng video team nói kịch bản sai"

**Nguyên nhân**: Tiêu chí chấm không khớp với yêu cầu thực tế.

**Fix**:
1. Hỏi video team: "Lỗi ở tiêu chí nào? (1–6)"
2. Sửa `judge.md`: ép tiêu chí đó hơn
3. Sinh lại bằng prompt mới:
   ```bash
   python generate.py --force --rounds 2
   ```

---

## ❌ Performance & Token

### "Chạy rất chậm" / "tốn nhiều token"

**Nguyên nhân**: Mỗi vòng chấm + sửa cần 2–3 gọi API (sinh + judge + revise).

**Fix**:
- **Giảm vòng**: `python generate.py --rounds 1` (nhanh hơn, chất lượng hơi thấp)
- **Bỏ chấm**: `python generate.py --no-eval` (nhanh gấp 3, chỉ dùng bản nháp)
- **Dùng model rẻ**: 
  ```bash
  export JUDGE_MODEL="gemini-3.1-sonnet-preview"  # rẻ hơn Pro
  python generate.py --rounds 2
  ```
- **Chạy tuần tự** (mặc định) thay vì song song → tiết kiệm quota

---

### "Hết quota giữa chừng"

**Nguyên nhân**: Gemini free tier giới hạn 60 request/phút hoặc có hạn mức.

**Fix**:
1. **Tạm dừng** 1 phút (chờ quota reset)
2. **Tiếp tục** từ chủ đề tiếp theo:
   ```bash
   python generate.py --only mtbf_estimation   # tiếp từ chủ đề này
   ```
3. **Setup billing** (Google Cloud) nếu cần nhiều request

---

## ❌ Output & Excel

### "json_to_excel.py báo lỗi đường dẫn"

**Nguyên nhân**: File hard-code đường dẫn `/Users/doanvinhnhan/...`.

**Fix**:
```python
# Mở json_to_excel.py, thay:
script_dir = '/Users/doanvinhnhan/doan1/scriptwriting/raw_script'

# Thành:
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(BASE_DIR, 'raw_script')
```

---

### "Excel trống hoặc thiếu chủ đề"

**Nguyên nhân**: JSON không hợp lệ hoặc converter bỏ qua (phải là mảng 1 object).

**Fix**:
1. Kiểm tra JSON:
   ```bash
   python3 -c "import json; json.load(open('raw_script/bayes_spam_filter.json'))"
   # Nếu không báo lỗi → JSON tốt
   ```
2. Kiểm tra converter: Có nạp hết file không?
   ```bash
   python json_to_excel.py  # xem output
   ```
3. Nếu vẫn thiếu → xem file `raw_script/*.json` có bị lỗi nào không

---

## ❌ GitHub & Teamwork

### "Conflict khi push (pull request có xung đột)"

**Nguyên nhân**: Hai người sửa cùng file `prompts/` rồi push cùng lúc.

**Fix**:
```bash
# Pull lại, fix conflict, rồi push
git pull origin main
# ... sửa file bị conflict (dấu <<<< >>>> ====)
git add .
git commit -m "fix conflict: prompt 02_theory_anchor"
git push origin main
```

**Tránh**: Phân công rõ — ai sửa file nào. Ví dụ:
- Nhân: `02_theory_anchor.md`, `context/`
- Anh: `04_length_budget.md`, `05_constraints.md`
- Hùng: `judge.md`, `revise.md`

---

### "Lịch sử của ai? Một đống commit lộn xộn"

**Nguyên nhân**: Mỗi lần chạy generate.py là có file `.json` & `.json_review` thay đổi → Git track hết → commit lộn xộn.

**Fix** — thêm `.gitignore`:
```
# .gitignore
scriptwriting/raw_script/*.json
scriptwriting/raw_script/reviews/*.json
```

Chỉ track `.md` (code/prompt) và `topic.txt`, chứ không track output JSON (auto-generate).

---

## ❌ Nâng cao

### "Model quên context dù có thêm vào"

**Nguyên nhân**: Context quá dài (>3000 chữ) → model quên ở phần cuối.

**Fix**:
- Giảm context: giữ lại chỉ **3–4 concept + công thức** (xóa chi tiết thừa)
- Hay dùng `context/<slug>.md` ngắn gọn + thêm prompt cụ thể vào topic tương ứng

---

### "Chấm điểm luôn cao (5.0) hoặc luôn thấp (2.0)"

**Nguyên nhân**: Judge module quá dễ/quá khắt.

**Fix** — sửa `judge.md`:
- **Quá dễ**: Thêm tiêu chí chi tiết hơn (ví dụ: "công thức phải viết dạng LaTeX rõ ràng")
- **Quá khắt**: Giảm đòi hỏi (ví dụ: "có công thức hoặc khái niệm, không bắt buộc cả hai")

---

## 📞 Khi nào cần hỏi team lead?

- Lỗi cơ bản (API key, setup): **trước tiên xem SETUP.md**
- Lỗi schema: cố gắng sửa prompt, nếu 3 vòng vẫn không được → hỏi
- Lỗi logic (điểm cao nhưng nội dung sai): hỏi lead để sửa rubric chung
- Lỗi GitHub (conflict, lịch sử): hỏi người quản lý repo

---

## 🎯 Checklist gỡ lỗi

Khi gặp lỗi, **lần lượt kiểm**:

- [ ] API key có đúng không? (`echo $GEMINI_API_KEY`)
- [ ] Module `.md` trong `prompts/` có đầy đủ không?
- [ ] Context `context/<slug>.md` có tồn tại không?
- [ ] Chạy lại lần 2 (model lần 2 đôi khi tốt hơn)?
- [ ] Xem `_review.json` → điểm tiêu chí nào thấp nhất?
- [ ] Sửa prompt / context tương ứng rồi chạy lại?
- [ ] Vẫn không được → tạo issue hoặc hỏi team lead

---

**Không tìm được lỗi của bạn?** → Tạo issue trên GitHub với:
- Lỗi gặp (error message đầy đủ)
- Lệnh chạy
- File đang dùng
- OS & Python version

Team sẽ giúp!
