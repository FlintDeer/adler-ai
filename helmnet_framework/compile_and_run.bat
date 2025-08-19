@echo off
python fix_feedback_json.py
copy /Y controller\dataset\controller_feedback_clean.jsonl controller\dataset\controller_feedback.jsonl
python main.py