# prompt_constructor.py

def inject_hint(user_input: str, hint: str) -> str:
    """
    Prepend a system-style instruction (hint) to the user query,
    forming the full prompt for the LLM.
    """
    return f"{hint}\n\nUser: {user_input}\nAdler: idk"