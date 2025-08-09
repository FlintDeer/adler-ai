import json
import re

SUGGESTED_RE = re.compile(r"Suggested\s+tokens\s*:\s*(.*)", re.IGNORECASE)

def _clean_token_block(text: str) -> str:
    """
    Accepts messy strings like:
      "[reflect] [expand]"
      "[reflect][expand]"
      "[ reflect ]   [ expand ]"
      "[reflect], [expand]"
    and returns a normalized string: "[reflect] [expand]"

    Returns "" if nothing valid is found.
    """
    # Grab all bracketed tokens like [reflect]
    tokens = re.findall(r"\[[^\[\]]+\]", text)
    tokens = [t.strip() for t in tokens if t.strip()]
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return " ".join(deduped)

def extract_training_pairs(feedback_path: str, output_path: str) -> None:
    """
    Reads controller/dataset/controller_feedback.jsonl and writes a clean
    controller/dataset/controller_feedback_training.jsonl with {"input","output"} pairs.

    Skips blank/malformed lines, logs why, and only exports samples that contain a
    recognizable "Suggested tokens:" line with bracketed tokens.
    """
    try:
        with open(feedback_path, "r", encoding="utf-8") as f:
            lines = [ln for ln in f if ln.strip()]  # skip blanks early
    except FileNotFoundError:
        print(f"[extract] No feedback file found at: {feedback_path}")
        return

    new_samples = 0
    total = 0

    with open(output_path, "w", encoding="utf-8") as out:
        for raw in lines:
            total += 1
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"[extract][SKIP] Bad JSON: {e}")
                continue

            # Basic fields sanity
            user = rec.get("input", "").strip()
            evaluator = rec.get("evaluator_result", "").strip()
            if not user or not evaluator:
                print("[extract][SKIP] Missing 'input' or 'evaluator_result'.")
                continue

            # Find the 'Suggested tokens:' line (case-insensitive)
            match = SUGGESTED_RE.search(evaluator)
            if not match:
                print("[extract][SKIP] No 'Suggested tokens:' line found.")
                continue

            token_block = _clean_token_block(match.group(1))
            if not token_block:
                print("[extract][SKIP] Suggested tokens had no [token] blocks.")
                continue

            out.write(json.dumps({"input": user, "output": token_block}) + "\n")
            new_samples += 1

    print(f"[extract] Parsed {total} feedback lines → wrote {new_samples} training samples to {output_path}")
