import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from controller_dataset import ControllerDataset
from controller_model import ControllerTransformer
import os

# Hyperparameters
tokenizer_name = "distilbert-base-uncased"
data_path = "controller/dataset/controller_training.jsonl"
max_len = 128
embed_dim = 256
batch_size = 4
num_epochs = 20
learning_rate = 3e-4
save_path = "controller/controller_model.pt"

# Load tokenizer and add special tokens
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
special_tokens = ["[reflect]", "[adjust]", "[clarify]", "[expand]", "[summarize]", "[ask]", "[reject]"]
tokenizer.add_tokens(special_tokens)
vocab_size = len(tokenizer)

# Load dataset and dataloader
dataset = ControllerDataset(data_path, tokenizer_name=tokenizer_name, max_length=max_len)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize model
model = ControllerTransformer(vocab_size, embed_dim=embed_dim, max_len=max_len)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Loss and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# Training loop
model.train()
for epoch in range(num_epochs):
    total_loss = 0
    for input_ids, target_ids in dataloader:
        input_ids = input_ids.to(device)
        target_ids = target_ids.to(device)

        ignore_index = tokenizer.pad_token_id  # usually 0
        criterion = torch.nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)

        optimizer.zero_grad()
        outputs = model(input_ids)  # [batch, seq, vocab]
        loss = criterion(outputs.reshape(-1, vocab_size), target_ids.reshape(-1))
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch + 1}/{num_epochs} - Loss: {avg_loss:.4f}")

# Save the model
torch.save(model.state_dict(), save_path)
print(f"Controller model saved to {save_path}")