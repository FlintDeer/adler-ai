import os

# Get from env or use hardcoded fallback
ENV_API_KEY = os.getenv("XAI_API_KEY", "")
API_URL_CONFIG = "https://api.x.ai/v1"