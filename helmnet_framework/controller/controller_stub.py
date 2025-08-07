# controller_stub.py

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