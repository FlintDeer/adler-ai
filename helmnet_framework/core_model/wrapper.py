# wrapper.py
import os
import httpx
from openai import OpenAI

def query_model(prompt: str, key: str, api_url: str) -> str:
    try:
        client = OpenAI(
            api_key=key,
            base_url=api_url,
            timeout=httpx.Timeout(30000.0),  # Override default timeout with longer timeout for reasoning models
        )

        completion = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": "You are Adler, a self aware reflective AI guide with an custom framework between the user and the prompts received to the LLM here."},
                {"role": "user", "content": prompt},
            ]
        )
        print(f"\n[HELMNET DEBUG] Prompt sent to LLM:\n---\n{prompt}\n---\n")
        return completion.choices[0].message.content
    except Exception as e:
        return f"[API Error] {str(e)}"