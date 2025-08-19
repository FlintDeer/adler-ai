import json
from pathlib import Path

FEEDBACK_LOG_PATH = Path(__file__).resolve().parents[1] / "controller" / "dataset" / "controller_feedback.jsonl"

def log_feedback_sample(user_input: str, controller_output: str, llm_response: str, evaluation_raw: str):
    def _s(x):
        return " ".join(str(x if x is not None else "").strip().split())

    FEEDBACK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "input": _s(user_input),
        "controller_output": _s(controller_output),
        "llm_response": _s(llm_response),
        "evaluator_result": _s(evaluation_raw),
    }

    try:
        line = json.dumps(record, ensure_ascii=False)
        with FEEDBACK_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"[FEEDBACK] Logged corrected sample to {FEEDBACK_LOG_PATH}")
    except Exception as e:
        print(f"[FEEDBACK][ERROR] Failed to log sample: {e}")
