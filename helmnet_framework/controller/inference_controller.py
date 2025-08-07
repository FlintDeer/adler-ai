import torch
from transformers import AutoTokenizer
from controller_model import ControllerModel

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ControllerModel(vocab_size=tokenizer.vocab_size).to(device)
model.load_state_dict(torch.load("controller_model.pt", map_location=device))
model.eval()

while True:
    text = input("User input: ")
    if text.strip().lower() == "exit":
        break
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    tokens = model.predict_tokens(input_ids, threshold=0.5)
    print("Modulation tokens:", " ".join(tokens))
