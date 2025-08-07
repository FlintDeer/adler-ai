import torch
import torch.nn as nn

MODULATION_TOKENS = [
    "[reflect]", "[clarify]", "[adjust]", "[reject]",
    "[expand]", "[confirm]", "[query]", "[halt]"
]

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class ControllerModel(nn.Module):
    def __init__(self, vocab_size, d_model=128, nhead=4, num_layers=4):
        super().__init__()
        self.token_map = {tok: idx for idx, tok in enumerate(MODULATION_TOKENS)}
        self.idx_map = {idx: tok for tok, idx in self.token_map.items()}

        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc_out = nn.Linear(d_model, len(self.token_map))

    def forward(self, src):
        embedded = self.embedding(src)
        encoded = self.pos_encoder(embedded)
        transformed = self.transformer_encoder(encoded)
        output = self.fc_out(transformed[:, -1, :])
        return output

    def predict_tokens(self, input_ids, threshold=0.5):
        with torch.no_grad():
            logits = self.forward(input_ids)
            probs = torch.sigmoid(logits).squeeze()
            selected = [self.idx_map[i] for i, p in enumerate(probs) if p > threshold]
            return selected or ["[unknown]"]
