import json
import torch
from torch import nn, optim
from transformers import AutoTokenizer
from controller.controller_model import ControllerModel, MODULATION_TOKENS

# Training hyperparams (feel free to tweak)
LR = 1e-5
EPOCHS = 2
THRESH_WARN_EMPTY = True

def _encode_sample(tokenizer, device, sample, token_map):
    text = sample.get("input", "")
    outputs = sample.get("output", "").split()
    if not text or not outputs:
        return None, None

    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)

    # Multi-hot target vector over modulation tokens
    label_vec = torch.zeros(len(MODULATION_TOKENS), device=device)
    for tok in outputs:
        if tok in token_map:
            label_vec[token_map[tok]] = 1.0
        # else: ignore unknown tokens silently (keeps it robust)

    return input_ids, label_vec.unsqueeze(0)

def train_on_feedback(path="controller/dataset/controller_feedback_training.jsonl"):
    """
    Fine-tunes the controller on the corrected feedback dataset.
    - Safely aborts if dataset is missing/empty.
    - Uses BCEWithLogitsLoss for multi-label targets.
    - Loads/saves controller_model.pt in-place.
    """
    # Load corrected samples
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[AutoTrain] No training file found at: {path}")
        return

    if not data:
        print("[AutoTrain] No training samples found — skipping.")
        return

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = ControllerModel(vocab_size=tokenizer.vocab_size).to(device)
    try:
        model.load_state_dict(torch.load("controller_model.pt", map_location=device))
        print("[AutoTrain] Loaded existing controller_model.pt")
    except Exception as e:
        print(f"[AutoTrain] Could not load existing model (starting fresh): {e}")

    model.train()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()
    token_map = {tok: idx for idx, tok in enumerate(MODULATION_TOKENS)}

    # Quick pass: drop samples that fail encoding
    encoded = []
    for s in data:
        ids, y = _encode_sample(tokenizer, device, s, token_map)
        if ids is not None and y is not None:
            encoded.append((ids, y))

    if not encoded:
        print("[AutoTrain] Encoded dataset is empty — nothing to train.")
        return

    for epoch in range(EPOCHS):
        total_loss = 0.0
        for input_ids, label in encoded:
            optimizer.zero_grad()
            logits = model(input_ids)
            loss = loss_fn(logits, label)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[AutoTrain] Epoch {epoch+1}/{EPOCHS} — Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "controller_model.pt")
    print("[AutoTrain] Saved updated controller_model.pt")
