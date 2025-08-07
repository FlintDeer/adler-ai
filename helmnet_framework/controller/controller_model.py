# controller_stub.py
import torch
import torch.nn as nn

class ControllerTransformer(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, num_heads=8, num_layers=4, max_len=128):
        super(ControllerTransformer, self).__init__()

        # Token embedding layer
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embed_dim)

        # Positional encoding (learned)
        self.pos_embedding = nn.Embedding(max_len, embed_dim)

        # Transformer encoder layer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            activation="gelu",
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output projection layer (linear decoder)
        self.output_layer = nn.Linear(embed_dim, vocab_size)

    def forward(self, input_ids):
        """
        input_ids: [batch_size, seq_len]
        """
        batch_size, seq_len = input_ids.size()

        # Generate position indices
        position = torch.arange(0, seq_len, device=input_ids.device).unsqueeze(0).expand(batch_size, seq_len)

        # Combine token + position embeddings
        x = self.embedding(input_ids) + self.pos_embedding(position)

        self.dropout = nn.Dropout(0.1)
        x = self.dropout(x)

        # Permute for transformer input: [seq_len, batch_size, embed_dim]
        x = x.permute(1, 0, 2)

        # Pass through transformer encoder
        x = self.transformer_encoder(x)

        # Project output to vocab logits
        logits = self.output_layer(x)

        # Return to [batch_size, seq_len, vocab_size]
        return logits.permute(1, 0, 2)

    def resize_token_embeddings(self, new_vocab_size):
        old_weight = self.embedding.weight.data
        new_embedding = nn.Embedding(new_vocab_size, old_weight.size(1))
        new_embedding.weight.data[:old_weight.size(0)] = old_weight
        self.embedding = new_embedding
        self.output_layer = nn.Linear(old_weight.size(1), new_vocab_size)

def get_prompt_hint(user_input: str) -> str:
    input_lower = user_input.lower()

    dispatch = "dispatch mode: "
    mode = "'fallback null'. "
    message = "Respond clearly and contextually"

    if "memory" in input_lower:
        mode = "'memory'. "
        message = "Focus on how memory system work in this context."
    elif "learn" in input_lower:
        mode = "'learn'. ";
        message = "Emphasize learning mechanisms or reiforcement dynamics."
    elif "efficient" in input_lower:
        mode = "'efficient'. ";
        message = "Respond with optimization in mind."
    elif "you" in input_lower:
        mode = "'you'. "
        message = "Answer with self-reflective or model-based perspective"

    return dispatch + mode + message