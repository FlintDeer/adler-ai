import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT_FILE = BASE / "controller" / "dataset" / "controller_feedback.jsonl"
OUTPUT_FILE = BASE / "controller" / "dataset" / "controller_feedback_clean.jsonl"

def _try_parse_first_object(text: str):
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    end = 0
    while True:
        nxt = text.find("}", end)
        if nxt == -1:
            return None
        candidate = text[:nxt + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            end = nxt + 1

def _squash(val):
    return " ".join(str(val if val is not None else "").strip().split())

def clean_feedback_file():
    print(f"[Clean] CWD: {Path.cwd()}")
    print(f"[Clean] Input path:  {INPUT_FILE}")
    print(f"[Clean] Output path: {OUTPUT_FILE}")

    if not INPUT_FILE.exists():
        print("[Clean] Input file NOT found. Listing dataset dir:")
        ds_dir = INPUT_FILE.parent
        if ds_dir.exists():
            for p in ds_dir.glob("*"):
                print(" -", p)
        else:
            print(" (dataset dir does not exist)")
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fixed = 0
    kept = 0
    total = 0

    with INPUT_FILE.open("r", encoding="utf-8") as infile, \
         OUTPUT_FILE.open("w", encoding="utf-8") as outfile:

        for raw in infile:
            total += 1
            raw = raw.strip()
            if not raw:
                continue

            obj = None
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                obj = _try_parse_first_object(raw)
                if obj is not None:
                    fixed += 1
                else:
                    print(f"[Clean][SKIP] Unfixable line #{total}")
                    continue

            for k in list(obj.keys()):
                obj[k] = _squash(obj[k])

            outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")
            kept += 1

    print(f"[Clean] Done. Total: {total}, Kept: {kept}, Fixed: {fixed}")
    print(f"[Clean] Wrote: {OUTPUT_FILE}")
    print("[Clean] To replace original:")
    print(f'  copy /Y "{OUTPUT_FILE}" "{INPUT_FILE}"  (Windows)')
    print(f'  or: move "{OUTPUT_FILE}" "{INPUT_FILE}"')

if __name__ == "__main__":
    clean_feedback_file()
