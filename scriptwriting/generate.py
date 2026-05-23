#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — Ngân hàng kịch bản v2

Khác với v1 (sinh hàng loạt, prompt khối, không kiểm chất lượng):
  - Prompt tách module trong prompts/, ghép động theo thứ tự PROMPT_MODULES.
  - Sinh TỪNG kịch bản, có chèn tư liệu tham khảo riêng từ context/<slug>.md (nếu có).
  - Sau khi sinh: kiểm schema -> chấm điểm bằng giám khảo -> nếu chưa đạt thì
    tự sửa theo nhận xét và chấm lại (vòng lặp cải thiện), tối đa --rounds vòng.
  - Giữ NGUYÊN schema JSON (6 key + 2 sub-key) để json_to_excel.py không phải đổi.

CLI:
  python generate.py                      # sinh mọi chủ đề, bỏ qua file đã có
  python generate.py --force              # sinh lại tất cả
  python generate.py --only mtbf_estimation   # chỉ một chủ đề (workflow lặp từng cái)
  python generate.py --rounds 3           # tối đa 3 vòng cải thiện
  python generate.py --no-eval            # bỏ chấm điểm (bản nháp nhanh)
  python generate.py --pass 4.0           # ngưỡng điểm đạt

Yêu cầu: biến môi trường GEMINI_API_KEY. Tùy chọn: GEN_MODEL, JUDGE_MODEL.
"""

import os
import re
import sys
import json
import time
import argparse

from google import genai
from google.genai import types

# --------------------------------------------------------------------------- #
# Đường dẫn (tương đối theo vị trí file này -> chạy được trên mọi máy)
# --------------------------------------------------------------------------- #
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CONTEXT_DIR = os.path.join(BASE_DIR, "context")
OUTPUT_DIR  = os.path.join(BASE_DIR, "raw_script")
TOPIC_FILE  = os.path.join(BASE_DIR, "topic.txt")
SAMPLE_FILE = os.path.join(BASE_DIR, "sample_script.txt")

# Thứ tự ghép module cho bước SINH. Muốn nâng cấp phần nào -> sửa đúng file đó.
PROMPT_MODULES = [
    "00_role.md",
    "01_structure.md",
    "02_theory_anchor.md",
    "03_visual_manim.md",
    "04_length_budget.md",
    "05_constraints.md",
    "06_output_format.md",
]
JUDGE_MODULE  = "judge.md"
REVISE_MODULE = "revise.md"

# Model (đổi qua biến môi trường nếu muốn giám khảo dùng model rẻ/nhanh hơn)
GEN_MODEL   = os.environ.get("GEN_MODEL",   "gemini-3.1-pro-preview")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", GEN_MODEL)

# --------------------------------------------------------------------------- #
# SCHEMA — nguồn chân lý duy nhất. Phải khớp y hệt key mà json_to_excel.py đọc.
# --------------------------------------------------------------------------- #
SECTION_KEYS = [
    "Tình huống dẫn nhập (5s)",
    "Mô tả bài toán/vấn đề (15s)",
    "Diễn giải/Minh họa (30s)",
    "Tổng kết kiến thức (30s)",
    "Tóm tắt từ khóa (10s)",
    "Gợi ý tiếp theo (10s)",
]
SUB_KEYS = [
    "Lời thoại (Voice-over)",
    "Đoạn video kết quả kèm câu hỏi (Visuals)",
]
JUDGE_CRITERIA = [
    "vong_lap_ket_mo", "neo_ly_thuyet", "de_hieu",
    "mach_lac", "chieu_sau_dai_cuong", "visual_kha_thi",
]

# Ngưỡng chất lượng (đổi qua CLI)
DEFAULT_PASS_THRESHOLD = 4.0   # điểm trung bình tối thiểu để đạt
MIN_PER_CRITERION      = 3      # không tiêu chí nào được dưới mức này
DEFAULT_ROUNDS         = 2      # số vòng cải thiện tối đa

# Ánh xạ thứ tự dòng trong topic.txt -> tên file (giữ từ v1)
TOPIC_FILENAMES = [
    "bayes_spam_filter", "ber_transmission", "system_reliability",
    "decision_tree_investment", "exponential_server_response", "normal_dist_machining",
    "gaussian_noise_signal", "covariance_portfolio", "3d_emission_diffusion",
    "robot_positioning_error", "linear_regression_housing", "regression_sensor_calibration",
    "confidence_interval_ab_test", "mtbf_estimation", "ttest_algorithm_speed",
    "qc_machine_deviation", "smart_elevator_queue", "bootstrap_resampling",
]

client = genai.Client()

# --------------------------------------------------------------------------- #
# Tiện ích
# --------------------------------------------------------------------------- #
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def load_modules(module_names):
    """Ghép các file module trong prompts/ thành một chuỗi prompt."""
    parts = []
    for name in module_names:
        path = os.path.join(PROMPTS_DIR, name)
        parts.append(read_file(path))
    return "\n\n".join(parts)


def load_context(slug):
    """Tìm context/<slug>.md rồi .txt. Trả về nội dung hoặc None."""
    for ext in (".md", ".txt"):
        path = os.path.join(CONTEXT_DIR, slug + ext)
        if os.path.exists(path):
            return read_file(path)
    return None


def extract_json(text):
    """Trích JSON từ phản hồi: bỏ rào markdown, lấy từ dấu mở đầu tới dấu đóng cuối."""
    if text is None:
        return None
    t = text.strip()
    t = re.sub(r"^```(?:json)?", "", t).strip()
    t = re.sub(r"```$", "", t).strip()
    # Ưu tiên mảng [...]; nếu không có thì thử object {...}
    for open_ch, close_ch in (("[", "]"), ("{", "}")):
        start = t.find(open_ch)
        end = t.rfind(close_ch)
        if start != -1 and end != -1 and end > start:
            candidate = t[start:end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return None


def validate_script(data):
    """Kiểm đúng schema. Trả về (ok, danh_sách_lỗi)."""
    errors = []
    if not isinstance(data, list) or len(data) != 1:
        return False, ["Đầu ra không phải mảng JSON chứa đúng 1 object."]
    obj = data[0]
    if not isinstance(obj, dict):
        return False, ["Phần tử của mảng không phải object."]

    for key in SECTION_KEYS:
        if key not in obj:
            errors.append(f"Thiếu key phần: '{key}'")
            continue
        section = obj[key]
        if not isinstance(section, dict):
            errors.append(f"Phần '{key}' không phải object.")
            continue
        for sub in SUB_KEYS:
            val = section.get(sub)
            if not isinstance(val, str) or not val.strip():
                errors.append(f"Phần '{key}' thiếu hoặc rỗng sub-key '{sub}'.")

    extra = [k for k in obj.keys() if k not in SECTION_KEYS]
    if extra:
        errors.append(f"Có key thừa không đúng schema: {extra}")

    return (len(errors) == 0), errors


def call_model(model, prompt, temperature):
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    return resp.text


# --------------------------------------------------------------------------- #
# Các bước của pipeline
# --------------------------------------------------------------------------- #
def build_generation_prompt(base_prompt, sample, topic, context):
    blocks = [base_prompt, "--- CHỦ ĐỀ ĐƯỢC GIAO ---\n" + topic]
    if context:
        blocks.append(
            "--- TƯ LIỆU THAM KHẢO (ưu tiên dùng thông tin ở đây khi có) ---\n" + context
        )
    blocks.append("--- KỊCH BẢN MẪU (chỉ tham khảo cấu trúc) ---\n" + sample)
    return "\n\n".join(blocks)


def generate_once(base_prompt, sample, topic, context, max_format_retries=3):
    """Sinh + ép đúng schema. Trả về (script_data | None)."""
    prompt = build_generation_prompt(base_prompt, sample, topic, context)
    for attempt in range(1, max_format_retries + 1):
        raw = call_model(GEN_MODEL, prompt, temperature=0.7)
        data = extract_json(raw)
        ok, errs = validate_script(data) if data is not None else (False, ["Không parse được JSON."])
        if ok:
            return data
        print(f"      [format retry {attempt}/{max_format_retries}] {errs[:2]}")
        prompt_fix = (
            prompt
            + "\n\n--- LỖI ĐỊNH DẠNG LẦN TRƯỚC, SỬA LẠI ---\n"
            + "\n".join(errs)
        )
        prompt = prompt_fix
        time.sleep(1)
    return None


def judge_script(judge_prompt, topic, script_data):
    """Chấm điểm. Trả về dict review hoặc None nếu lỗi."""
    prompt = (
        judge_prompt
        + "\n\n--- CHỦ ĐỀ ---\n" + topic
        + "\n\n--- KỊCH BẢN CẦN CHẤM ---\n"
        + json.dumps(script_data, ensure_ascii=False, indent=2)
    )
    raw = call_model(JUDGE_MODEL, prompt, temperature=0.2)
    review = extract_json(raw)
    if not isinstance(review, dict) or "scores" not in review:
        return None
    # Đảm bảo đủ tiêu chí
    scores = review.get("scores", {})
    if not all(c in scores for c in JUDGE_CRITERIA):
        return None
    return review


def evaluate(review, pass_threshold):
    """Tự tính đạt/chưa trong code (không tin tuyệt đối vào giám khảo)."""
    vals = [float(review["scores"][c]) for c in JUDGE_CRITERIA]
    avg = sum(vals) / len(vals)
    passed = (avg >= pass_threshold) and (min(vals) >= MIN_PER_CRITERION)
    return passed, round(avg, 2)


def revise_script(revise_prompt, base_prompt, topic, context, script_data, review):
    """Sửa kịch bản theo nhận xét. Trả về (script_data | None)."""
    prompt = (
        base_prompt  # nhắc lại toàn bộ quy tắc
        + "\n\n" + revise_prompt
        + "\n\n--- CHỦ ĐỀ ---\n" + topic
    )
    if context:
        prompt += "\n\n--- TƯ LIỆU THAM KHẢO ---\n" + context
    prompt += (
        "\n\n--- KỊCH BẢN HIỆN TẠI ---\n"
        + json.dumps(script_data, ensure_ascii=False, indent=2)
        + "\n\n--- NHẬN XÉT CỦA GIÁM KHẢO ---\n"
        + "Lỗi cần sửa: " + json.dumps(review.get("loi_can_sua", []), ensure_ascii=False)
        + "\nGợi ý: " + str(review.get("goi_y_cu_the", ""))
    )
    raw = call_model(GEN_MODEL, prompt, temperature=0.6)
    data = extract_json(raw)
    ok, _ = validate_script(data) if data is not None else (False, None)
    return data if ok else None


# --------------------------------------------------------------------------- #
# Xử lý một chủ đề: sinh -> chấm -> cải thiện
# --------------------------------------------------------------------------- #
def run_topic(slug, topic, base_prompt, judge_prompt, revise_prompt, sample, args):
    print(f"\n[*] {slug}")
    reviews_dir = os.path.join(OUTPUT_DIR, "reviews")
    out_path    = os.path.join(OUTPUT_DIR, slug + ".json")
    review_path = os.path.join(reviews_dir, slug + "_review.json")

    if os.path.exists(out_path) and not args.force:
        print("    đã tồn tại -> bỏ qua (dùng --force để sinh lại).")
        return

    context = load_context(slug)
    print(f"    context: {'có' if context else 'không'}")

    script = generate_once(base_prompt, sample, topic, context)
    if script is None:
        print("    [FAILED] không sinh được kịch bản đúng schema.")
        return

    if args.no_eval:
        save_outputs(out_path, review_path, script, history=None)
        print("    đã lưu (bỏ chấm điểm).")
        return

    history = []
    best_script, best_avg, best_review = script, -1.0, None

    for rnd in range(args.rounds + 1):  # vòng 0 = bản gốc, sau đó cải thiện
        review = judge_script(judge_prompt, topic, script)
        if review is None:
            print(f"    [round {rnd}] giám khảo trả về không hợp lệ -> dừng chấm.")
            break
        passed, avg = evaluate(review, args.pass_threshold)
        print(f"    [round {rnd}] điểm TB = {avg} | "
              + " ".join(f"{c}={review['scores'][c]}" for c in JUDGE_CRITERIA)
              + (" | ĐẠT" if passed else " | chưa đạt"))
        history.append({"round": rnd, "avg": avg, "review": review})

        if avg > best_avg:
            best_script, best_avg, best_review = script, avg, review

        if passed or rnd == args.rounds:
            break

        revised = revise_script(revise_prompt, base_prompt, topic, context, script, review)
        if revised is None:
            print("    [revise] sửa không đúng schema -> giữ bản tốt nhất.")
            break
        script = revised

    save_outputs(out_path, review_path, best_script,
                 history={"final_avg": best_avg, "passed": best_avg >= args.pass_threshold,
                          "rounds": history})
    print(f"    [DONE] lưu bản điểm cao nhất ({best_avg}) -> {os.path.basename(out_path)}")


def save_outputs(out_path, review_path, script, history):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    if history is not None:
        os.makedirs(os.path.dirname(review_path), exist_ok=True)
        with open(review_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
def parse_topics():
    text = read_file(TOPIC_FILE)
    topics = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            topics.append(re.sub(r"^\d+\.\s*", "", line))
    return topics


def main():
    ap = argparse.ArgumentParser(description="Sinh ngân hàng kịch bản v2 (context + đánh giá + cải thiện).")
    ap.add_argument("--only", help="chỉ sinh 1 chủ đề theo slug (vd: mtbf_estimation)")
    ap.add_argument("--force", action="store_true", help="sinh lại cả file đã có")
    ap.add_argument("--rounds", type=int, default=DEFAULT_ROUNDS, help="số vòng cải thiện tối đa")
    ap.add_argument("--no-eval", action="store_true", help="bỏ chấm điểm, chỉ sinh bản nháp")
    ap.add_argument("--pass", dest="pass_threshold", type=float,
                    default=DEFAULT_PASS_THRESHOLD, help="ngưỡng điểm TB để đạt")
    args = ap.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit("Lỗi: chưa thiết lập GEMINI_API_KEY.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base_prompt   = load_modules(PROMPT_MODULES)
    judge_prompt  = load_modules([JUDGE_MODULE])
    revise_prompt = load_modules([REVISE_MODULE])
    sample        = read_file(SAMPLE_FILE)
    topics        = parse_topics()

    pairs = []
    for i, topic in enumerate(topics):
        slug = TOPIC_FILENAMES[i] if i < len(TOPIC_FILENAMES) else f"topic_{i+1}"
        pairs.append((slug, topic))

    if args.only:
        pairs = [(s, t) for s, t in pairs if s == args.only]
        if not pairs:
            raise SystemExit(f"Không tìm thấy slug '{args.only}'. Slug hợp lệ: {TOPIC_FILENAMES}")

    print(f"Chế độ: {'1 chủ đề' if args.only else f'{len(pairs)} chủ đề'} | "
          f"rounds={args.rounds} | eval={'tắt' if args.no_eval else 'bật'} | "
          f"pass>={args.pass_threshold}")

    for slug, topic in pairs:
        try:
            run_topic(slug, topic, base_prompt, judge_prompt, revise_prompt, sample, args)
        except Exception as e:
            print(f"    [ERROR] {slug}: {e}")

    print("\n[HOÀN TẤT]")


if __name__ == "__main__":
    main()
