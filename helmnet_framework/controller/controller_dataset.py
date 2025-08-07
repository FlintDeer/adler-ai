# controller_dataset.py
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer
import json

class ControllerDataset(Dataset):
    def __init__(self, data_path, tokenizer_name="distilbert-base-uncased", max_length=128):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.pad_token_id = self.tokenizer.pad_token_id
        self.samples = []

        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                input_text = entry["input"]
                target_text = entry["output"]

                # Encode input
                encoded = self.tokenizer(
                    input_text,
                    padding="max_length",
                    truncation=True,
                    max_length=max_length,
                    return_tensors="pt"
                )
                input_ids = encoded["input_ids"].squeeze()

                # Encode output
                encoded_target = self.tokenizer(
                    target_text,
                    padding="max_length",
                    truncation=True,
                    max_length=max_length,
                    return_tensors="pt"
                )
                target_ids = encoded_target["input_ids"].squeeze()

                # Optional: strip [CLS] from target
                if target_ids[0] == self.tokenizer.cls_token_id:
                    target_ids[0] = self.pad_token_id
                if self.tokenizer.sep_token_id in target_ids:
                    sep_index = (target_ids == self.tokenizer.sep_token_id).nonzero(as_tuple=True)[0]
                    if len(sep_index) > 0:
                        target_ids[sep_index[0]] = self.pad_token_id

                self.samples.append((input_ids, target_ids))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]
