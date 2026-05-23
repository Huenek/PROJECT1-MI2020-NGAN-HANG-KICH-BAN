# ⚙️ SETUP — Cài đặt môi trường

Hướng dẫn từng bước để team có thể chạy pipeline v2 trên bất kỳ máy nào.

## 1️⃣ Yêu cầu hệ thống

- **Python**: 3.9 hoặc cao hơn
- **Git**: để clone repo
- **Gemini API key**: từ Google AI Studio
- **Hệ điều hành**: macOS, Linux, Windows (WSL2 khuyến nghị)

Kiểm tra Python:
```bash
python3 --version   # phải >= 3.9
```

## 2️⃣ Clone repo & vào thư mục

```bash
git clone https://github.com/[your-org]/MI2020VideoProject.git
cd MI2020VideoProject/scriptwriting
```

## 3️⃣ Tạo môi trường ảo (khuyến nghị)

```bash
# Tạo virtual env
python3 -m venv venv

# Kích hoạt
# macOS / Linux:
source venv/bin/activate
# Windows (CMD):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
```

## 4️⃣ Cài dependencies

Tạo file `requirements.txt` trong `scriptwriting/` với nội dung:

```
google-genai>=0.3.0
openpyxl>=3.1.0
pandas>=2.0.0
pillow>=9.0.0
pydub>=0.25.1
imageio>=2.14.0
scipy>=1.7.0
```

Cài:
```bash
pip install -r requirements.txt
```

## 5️⃣ Thiết lập Gemini API key

### a. Lấy API key
1. Vào https://aistudio.google.com/apikey
2. Click **Create API key**
3. Copy key vào một nơi an toàn

### b. Thiết lập biến môi trường

**macOS / Linux** — thêm vào `~/.bashrc` hoặc `~/.zshrc`:
```bash
export GEMINI_API_KEY="your-actual-key-here"
```

Rồi reload:
```bash
source ~/.bashrc
```

**Windows (PowerShell)**:
```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-actual-key-here", "User")
# Reload PowerShell sau đó
```

**Hoặc cách tạm thời (bất kỳ OS)**:
```bash
export GEMINI_API_KEY="your-key"
python generate.py --only bayes_spam_filter
```

### c. Kiểm tra
```bash
python3 -c "import os; print('✓ Key OK' if os.environ.get('GEMINI_API_KEY') else '✗ Key chưa set')"
```

## 6️⃣ Config tùy chọn (nâng cao)

Nếu muốn dùng model khác hoặc model riêng cho giám khảo:

```bash
# Model dùng để sinh kịch bản (mặc định: gemini-3.1-pro-preview)
export GEN_MODEL="gemini-3.1-pro-preview"

# Model dùng để chấm điểm (tùy chọn — để rẻ token, có thể dùng Sonnet)
export JUDGE_MODEL="gemini-3.1-pro-preview"
```

## 7️⃣ Test cài đặt

Chạy lệnh này để test (tạo 1 kịch bản test):

```bash
python generate.py --only bayes_spam_filter --rounds 1
```

Mong đợi đầu ra giống:
```
[*] bayes_spam_filter
    context: có
    [round 0] điểm TB = 4.2 | vong_lap_ket_mo=4 neo_ly_thuyet=5 ... | ĐẠT
    [DONE] lưu bản điểm cao nhất (4.2) -> bayes_spam_filter.json
```

Kiểm tra output:
```bash
ls -la raw_script/bayes_spam_filter.json                # phải có file
cat raw_script/reviews/bayes_spam_filter_review.json   # xem điểm
```

Nếu thấy JSON hợp lệ → ✓ **Setup xong!**

## 8️⃣ Troubleshooting cài đặt

### ❌ "ModuleNotFoundError: No module named 'google'"
→ Bạn chưa cài `google-genai`. Chạy:
```bash
pip install google-genai
```

### ❌ "GEMINI_API_KEY not set"
→ Biến môi trường chưa được export. Kiểm tra:
```bash
echo $GEMINI_API_KEY
```

Nếu trống → set lại theo bước 5b.

### ❌ "gRPC failed with status=UNAUTHENTICATED"
→ API key sai hoặc hết quota. Kiểm tra:
- API key có đúng không? (copy lại từ AI Studio)
- Quota còn không? (vào https://aistudio.google.com/u/0/app/apiDashboard)

### ❌ "socket timeout" khi gọi API
→ Mạng chậm hoặc bị block. Thử:
```bash
curl https://api.anthropic.com -v   # nếu timeout → mạng có issue
```

Nếu VPN cần → bật VPN trước khi chạy.

## 9️⃣ Chạy lần đầu (full workflow)

```bash
# Sinh 1 chủ đề (bayes) với 2 vòng cải thiện
python generate.py --only bayes_spam_filter --rounds 2

# Xem kịch bản
cat raw_script/bayes_spam_filter.json | head -50

# Xem điểm chi tiết
cat raw_script/reviews/bayes_spam_filter_review.json

# Gom tất cả JSON vào Excel (nếu có nhiều chủ đề)
# python json_to_excel.py
```

## 🔟 Cập nhật & duy trì

**Update code từ GitHub:**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

**Xóa cache & tạo lại:**
```bash
rm -rf raw_script/reviews/*.json     # xóa old reviews
python generate.py --force            # sinh lại tất cả
```

---

**Nếu vẫn gặp issue**: xem [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) hoặc tạo issue trên GitHub.
