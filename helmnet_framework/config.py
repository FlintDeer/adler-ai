import os

# Get from env or use hardcoded fallback
ENV_API_KEY = os.getenv("XAI_API_KEY", "")
API_URL_CONFIG = "https://api.x.ai/v1"

ControllerTransformer(
    vocab_size,
    embed_dim=256,
    num_heads=8,
    num_layers=4,
    max_len=128
)