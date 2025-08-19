import httpx
from openai import OpenAI

def evaluate_controller_decision(user_input: str, controller_tokens: str, llm_response: str, key: str, api_url: str) -> dict:
    client = OpenAI(
        api_key=key,
        base_url=api_url,
        timeout=httpx.Timeout(30.0)
    )

    system_msg = (
        "You an evaluator AI helping another AI learn to modulate its behaviour in its 'controller' system."
        "The controller system generates one or more tokens, which serve as personal instructions for the LLM to use to formulate its own response."
        "Using control tokens like [reflect], [clarify], [expand], or whatever else suits, 2 max but less is more"
        "You will evaluate whether all the tokens chosen matched the intent and output precisely, as .\n\n"
        "Respond in this format once, keep the reason short with one sentence for each token max:\n"
        "- Evaluation: [good] / [wrong_tokens] / [overmodulated] / [undermodulated]\n"
        "- Suggested tokens: [...]\n"
        "- Reason: ..."
    )

    user_prompt = f"""In the context:

user:
{user_input}

controller:
{controller_tokens}

llm response:
{llm_response}

Did the controller chose the right tokens?"""

    completion = client.chat.completions.create(
        model="grok-3-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt}
        ],
    )

    reply = completion.choices[0].message.content

    # after getting `reply`
    if "Suggested tokens:" not in reply:
        # fall back to controller tokens so good cases reinforce
        reply += f"\n- Suggested tokens: {controller_tokens}"
        
    print("\n[FEEDBACK] Evaluation Result:\n" + reply + "\n")

    return {"raw": reply}
