# Print boot BEFORE heavy imports for instant feedback
import os
import config
import time
import threading
import itertools
import sys

os.system('cls')

boot_complete = False

def booting():
    for c in itertools.cycle(['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']):
        if boot_complete:
            break
        sys.stdout.write(f"\r{c} [HELMNET] Booting integrated feedback-training loop.")
        sys.stdout.flush()
        time.sleep(0.1)
    

t = threading.Thread(target=booting)
t.start()

from controller.controller_stub import get_controller_output
from core_model.wrapper import query_model
from feedback.evaluator import evaluate_controller_decision
from feedback.logger import log_feedback_sample
from feedback.extract_training_data import extract_training_pairs
from controller.auto_trainer import train_on_feedback

from config import ENV_API_KEY, API_URL_CONFIG

boot_complete = True
sys.stdout.write(f"\r[HELMNET] Ready. Type 'exit' to stop.\033[K\n\n")

FEEDBACK_PATH = "controller/dataset/controller_feedback.jsonl"
TRAINING_OUTPUT_PATH = "controller/dataset/controller_feedback_training.jsonl"
SEED_PROMPTS_PATH = "controller/seed_prompts.txt"

def _count_lines(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0

def _generate_self_prompt() -> str:
    # Use a seed file if you’ve saved one; fall back to a small builtin list
    try:
        with open(SEED_PROMPTS_PATH, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
        if lines:
            return lines[0 if len(lines) == 1 else (int(time.time()) % len(lines))]
    except FileNotFoundError:
        pass
    seeds = [
        "What am I optimizing for when I respond?",
        "When should I prefer [expand] over [clarify]?",
        "Design a new modulation token to handle uncertainty.",
        "How should I merge modulation with long-term memory?"
        ]
    return seeds[int(time.time()) % len(seeds)]

def main():
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        if user_input == "":
            user_input = _generate_self_prompt()
            print(f"[AutoPrompt] → {user_input}")

        # 1) Controller
        controller_output = get_controller_output(user_input)
        print(f"\n[Controller Output] → {controller_output}")

        # 2) LLM
        response = query_model(user_input, controller_output, ENV_API_KEY, API_URL_CONFIG)
        # the stream is printed as its generated in wrapper.py

        # 3) Evaluator
        feedback = evaluate_controller_decision(user_input, controller_output, response, ENV_API_KEY, API_URL_CONFIG)
        raw_eval = (feedback or {}).get("raw", "").strip()
        if "Suggested tokens:" not in raw_eval:
            print("[Evaluator] → No 'Suggested tokens:' found; will still log for review.")

        # 4) Log full record
        log_feedback_sample(user_input, controller_output, response, raw_eval)

        # 5) Extract → train only if new samples appeared
        before = _count_lines(TRAINING_OUTPUT_PATH)
        extract_training_pairs(FEEDBACK_PATH, TRAINING_OUTPUT_PATH)
        after = _count_lines(TRAINING_OUTPUT_PATH)
        added = max(0, after - before)

        if added > 0:
            print(f"[Train] New samples: {added} → training…")
            train_on_feedback(TRAINING_OUTPUT_PATH)
        else:
            print("[Train] No new clean samples; skipping training.")

if __name__ == "__main__":
    main()
