import torch
from torch import nn, optim
from transformers import AutoTokenizer
from controller_model import ControllerModel, MODULATION_TOKENS

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ControllerModel(vocab_size=tokenizer.vocab_size).to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-4)
loss_fn = nn.BCEWithLogitsLoss()

import json
with open("controller/dataset/controller_training_reflect_boosted.jsonl", "r") as f:
    data = [json.loads(line) for line in f]

token_map = {tok: idx for idx, tok in enumerate(MODULATION_TOKENS)}

def encode_sample(sample):
    input_ids = tokenizer.encode(sample["input"], return_tensors="pt").to(device)
    label_vector = torch.zeros(len(MODULATION_TOKENS)).to(device)
    for tok in sample["output"].split():
        if tok in token_map:
            label_vector[token_map[tok]] = 1.0
    return input_ids, label_vector.unsqueeze(0)

loop_count = 15
for epoch in range(loop_count):
    total_loss = 0
    for sample in data:
        input_ids, label = encode_sample(sample)
        optimizer.zero_grad()
        logits = model(input_ids)
        loss = loss_fn(logits, label)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{loop_count}, Loss: {total_loss:.4f}")

torch.save(model.state_dict(), "controller_model.pt")
