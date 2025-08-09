import json
import os

LOG_PATH = "controller/dataset/controller_feedback.jsonl"

def log_feedback_sample(user_input, controller_output, llm_response, evaluation_raw):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    sample = {
        "input": user_input,
        "controller_output": controller_output,
        "llm_response": llm_response,
        "evaluator_result": evaluation_raw.strip()
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(sample) + "\n")

    print("[FEEDBACK] Logged corrected sample to controller_feedback.jsonl")