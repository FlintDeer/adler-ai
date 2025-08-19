import json
import re

# Accept "Suggested tokens:" with any spacing/case, tolerate odd punctuation
SUG_LINE_RE = re.compile(r"suggested\s*tokens\s*:\s*(.*)", re.IGNORECASE)

# Accept tokens in:
#  - square brackets  [clarify]
#  - parentheses      (clarify)
#  - bare words       clarify,respond
#  - mixed separators , ; / whitespace
TOKEN_RE = re.compile(
    r"""
    \[([^\[\]]+)\]            # [token]
    | \(([^()]+)\)            # (token)
    | \b([A-Za-z_]+)\b        # bare token (letters/underscore)
    """,
    re.VERBOSE,
)

# If you’ve added custom tokens, list them here so bare-word parsing is safe:
KNOWN = {
    "reflect", "clarify", "adjust", "reject",
    "expand", "confirm", "query", "halt",
    "respond"
}

def _normalize_tokens(raw: str) -> str:
    if not raw:
        return ""
    found = []
    for m in TOKEN_RE.finditer(raw):
        tok = (m.group(1) or m.group(2) or m.group(3) or "").strip()
        if not tok:
            continue
        # keep only known tokens for bare-word matches
        base = tok.strip().strip("[]() ").lower()
        if base in KNOWN:
            bracketed = f"[{base}]"
            if bracketed not in found:
                found.append(bracketed)
    return " ".join(found)

def extract_training_pairs(feedback_path: str, output_path: str) -> None:
    try:
        with open(feedback_path, "r", encoding="utf-8") as f:
            lines = [ln for ln in f if ln.strip()]
    except FileNotFoundError:
        print(f"[extract] No feedback file found at: {feedback_path}")
        return

    wrote = 0
    total = 0
    with open(output_path, "w", encoding="utf-8") as out:
        for ln in lines:
            total += 1
            ln = ln.strip()
            try:
                rec = json.loads(ln)
            except json.JSONDecodeError as e:
                print(f"[extract][SKIP] Bad JSON line len={len(ln)} ({e}); skipping.")
                continue

            user = (rec.get("input") or "").strip()
            evaluator = (rec.get("evaluator_result") or "").strip()
            if not user or not evaluator:
                print("[extract][SKIP] Missing input/evaluator_result.")
                continue

            m = SUG_LINE_RE.search(evaluator)
            if not m:
                print("[extract][INFO] No 'Suggested tokens:' present; likely [good].")
                continue

            norm = _normalize_tokens(m.group(1))
            if not norm:
                print("[extract][INFO] Suggested tokens empty/unrecognized; skipping training for this entry.")
                continue

            out.write(json.dumps({"input": user, "output": norm}, ensure_ascii=False) + "\n")
            wrote += 1

    print(f"[extract] Parsed {total} lines → wrote {wrote} training samples to {output_path}")
