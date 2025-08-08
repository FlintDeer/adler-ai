import torch
from transformers import AutoTokenizer
from controller.controller_model import ControllerModel, MODULATION_TOKENS

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model once at import
model = ControllerModel(vocab_size=tokenizer.vocab_size).to(device)
model.load_state_dict(torch.load("controller_model.pt", map_location=device))
model.eval()

def get_controller_output(text: str) -> str:
    """Returns modulation tokens as a string for given user input."""
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    tokens = model.predict_tokens(input_ids, threshold=0.5)
    return " ".join(tokens)
