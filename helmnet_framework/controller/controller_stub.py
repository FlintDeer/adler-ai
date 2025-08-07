"""
controller_stub.py
===================

A lightweight, rule‑based controller for the HelmNet framework.

This module provides a simple heuristic function to determine which
modulation tokens apply to a given user input and converts those
tokens into a human‑readable hint string. It is meant to stand in
place of a trainable controller model when machine learning
dependencies (e.g. PyTorch or Transformers) are not available. You
can extend or replace the heuristics here with a learned model in the
future.
"""

from typing import List

# Mapping from modulation tokens to natural language descriptions
TOKEN_HINTS = {
    "[clarify]": "Ask for clarification or restate the question clearly.",
    "[adjust]": "Adjust the focus to the most relevant concept.",
    "[reflect]": "Encourage thoughtful reflection on the question.",
    "[reject]": "Politely reject incorrect assumptions or premises.",
    "[expand]": "Request more details or expand the explanation.",
    "[confirm]": "Confirm understanding or agreement.",
    "[query]": "Ask a follow‑up question for more information.",
    "[halt]": "Stop or conclude when the answer seems sufficient.",
}


def detect_tokens(user_input: str) -> List[str]:
    """
    Heuristically map patterns in ``user_input`` to one or more
    modulation tokens.

    The rules defined here are intentionally simple so that they can
    operate without any external ML libraries. They are based on
    common phrases that might imply a need for clarification, adjustment,
    reflection, etc.

    Parameters
    ----------
    user_input : str
        The raw text entered by the user.

    Returns
    -------
    List[str]
        A list of modulation tokens relevant to the input. If no
        patterns match, ``[clarify]`` is returned by default.
    """
    text = user_input.lower()
    tokens: List[str] = []

    # Clarify: the user signals they didn't understand or ask what something means
    if any(phrase in text for phrase in ["don't understand", "explain again", "what does", "what do you mean"]):
        tokens.append("[clarify]")

    # Adjust: the user asks for a simpler or different phrasing
    if any(phrase in text for phrase in ["rephrase", "simpler", "adjust"]):
        tokens.append("[adjust]")

    # Reflect: the user wants to pause and think or reflect on the content
    if any(phrase in text for phrase in ["think", "moment to think", "reflect", "review", "let's review"]):
        tokens.append("[reflect]")

    # Reject: the user asserts something is incorrect or seems off
    if any(phrase in text for phrase in ["doesn't seem right", "doesn't seem correct", "wrong", "incorrect", "that's not right"]):
        tokens.append("[reject]")

    # Expand: the user asks for more detail or to expand on an idea
    if any(phrase in text for phrase in ["tell me more", "more about", "expand on", "go deeper"]):
        tokens.append("[expand]")

    # Query: the user seeks confirmation or further questions
    if any(phrase in text for phrase in ["are you sure", "really?", "query", "can you?", "could you?"]):
        tokens.append("[query]")

    # Confirm: the user indicates agreement or confirmation
    if any(phrase in text for phrase in ["yes", "that makes sense", "i agree", "correct"]):
        tokens.append("[confirm]")

    # Halt: the user suggests stopping or that a part is sufficient
    if any(phrase in text for phrase in ["stop", "enough", "halt", "that's enough"]):
        tokens.append("[halt]")

    # Default fallback
    if not tokens:
        tokens.append("[clarify]")

    return tokens


def interpret_tokens(tokens: List[str]) -> str:
    """
    Convert a list of modulation tokens into a single natural language
    hint string.

    Parameters
    ----------
    tokens : List[str]
        Modulation tokens detected by :func:`detect_tokens` or a
        controller model.

    Returns
    -------
    str
        A concatenated string of human‑readable instructions. Unknown
        tokens are ignored.
    """
    hints = [TOKEN_HINTS.get(tok) for tok in tokens if tok in TOKEN_HINTS]
    # Filter out any None values and join
    hints = [h for h in hints if h]
    return " ".join(hints) if hints else ""


def get_prompt_hint(user_input: str) -> str:
    """
    Public API expected by ``main.py``.

    It detects modulation tokens relevant to the user's input and
    converts them into a descriptive hint that can be prepended to
    the prompt sent to the LLM.

    Parameters
    ----------
    user_input : str
        Raw text input from the user.

    Returns
    -------
    str
        A human‑readable hint string derived from one or more
        modulation tokens.
    """
    tokens = detect_tokens(user_input)
    return interpret_tokens(tokens)


__all__ = ["get_prompt_hint", "detect_tokens", "interpret_tokens", "TOKEN_HINTS"]