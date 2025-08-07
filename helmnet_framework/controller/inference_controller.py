import torch
from transformers import AutoTokenizer
from controller_model import ControllerTransformer

# --- Config ---
model_path = "controller/controller_model.pt"
tokenizer_name = "distilbert-base-uncased"
embed_dim = 128
max_len = 128

# --- Load model and tokenizer ---
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
special_tokens = ["[reflect]", "[adjust]", "[clarify]", "[expand]", "[summarize]", "[ask]", "[reject]"]
tokenizer.add_tokens(special_tokens)
vocab_size = tokenizer.vocab_size + len(special_tokens)

model = ControllerTransformer(vocab_size, embed_dim=embed_dim, max_len=max_len)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# --- Inference loop ---
while True:
    user_input = input("Prompt: ").strip()
    if user_input.lower() in ("exit", "quit"):
        break

    tokens = tokenizer(
        user_input, 
        return_tensors="pt", 
        max_length=max_len, 
        truncation=True, 
        padding="max_length"
    )
    input_ids = tokens["input_ids"]

    with torch.no_grad():
        output_logits = model(input_ids)  # [1, seq, vocab]
        predicted_ids = output_logits.argmax(dim=-1)[0].tolist()  # [seq]

    # Convert token IDs to readable tokens
    decoded_tokens = tokenizer.convert_ids_to_tokens(predicted_ids)

    # Remove padding but keep special symbolic tokens
    filtered_tokens = [tok for tok in decoded_tokens if tok != "[PAD]"]

    print("Controller response:", " ".join(filtered_tokens), "\n")

