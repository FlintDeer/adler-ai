import os

"""
Configuration variables for the HelmNet framework.

This module defines simple environment-based configuration values that
other modules can import. The previous version attempted to instantiate a
``ControllerTransformer`` here, but that class is undefined in this
repository and instantiating it at import time violates separation of concerns.
"""

# Allow the API key to be provided via an environment variable; default to empty.
ENV_API_KEY: str = os.getenv("XAI_API_KEY", "")

# Allow overriding the base API URL via an environment variable; default to the
# x.ai endpoint used by the OpenAI-compatible API wrapper.
API_URL_CONFIG: str = os.getenv("XAI_API_URL", "https://api.x.ai/v1")

__all__ = ["ENV_API_KEY", "API_URL_CONFIG"]