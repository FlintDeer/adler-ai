#inference_controller.py
import torch
from transformers import AutoTokenizer
from controller_model import ControllerTransformer

# --- Config ----------------------------------------------------------
model_path   = "controller/controller_model.pt"
tokenizer_name = "distilbert-base-uncased"

# THESE **must match** your training run:
embed_dim    = 256
num_heads    = 8
num_layers   = 4
max_len      = 128
MAX_SYMBOLS  = 5   # how many controller tokens to generate

# --- Load tokenizer & special tokens ---------------------------------
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
special_tokens = ["[reflect]", "[adjust]", "[clarify]", "[expand]",
                  "[summarize]", "[ask]", "[reject]"]
tokenizer.add_tokens(special_tokens)
vocab_size = len(tokenizer)

# --- Build & load controller model -----------------------------------
model = ControllerTransformer(
    vocab_size=vocab_size,
    embed_dim=embed_dim,
    num_heads=num_heads,
    num_layers=num_layers,
    max_len=max_len
)
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

pad_id = tokenizer.pad_token_id
sep_id = tokenizer.sep_token_id
cls_id = tokenizer.cls_token_id   # we’ll filter this too

# --- Inference REPL ---------------------------------------------------
while True:
    prompt = input("Prompt: ").strip()
    if prompt.lower() in {"exit", "quit"}:
        break

    # Encode user prompt
    enc = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,      # still keep truncation
        padding=False         # ←  no pad tokens added
    )
    input_ids = enc["input_ids"]          # shape [1, seq_len ≤ 128]
    
    # --- autoregressive generation loop ------------------------------
    generated = []
    cur_ids   = input_ids.clone()

    with torch.no_grad():
        for _ in range(MAX_SYMBOLS):
            logits = model(cur_ids)              # [1, seq, vocab]
            next_id = logits[0, -1].argmax().item()

            if next_id in {pad_id, sep_id, cls_id}:
                break

            generated.append(next_id)
            cur_ids = torch.cat(
                [cur_ids, torch.tensor([[next_id]])], dim=1
            )

    # Convert IDs → tokens
    tokens = tokenizer.convert_ids_to_tokens(generated)

    # Remove consecutive duplicates
    deduped = [tok for i, tok in enumerate(tokens) if i == 0 or tok != tokens[i-1]]

    print("Controller response:", " ".join(deduped) if deduped else "(no symbols)\n")
