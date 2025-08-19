import httpx
import pyttsx3
from openai import OpenAI
engine = pyttsx3.init()
engine.setProperty('rate', 200) 


def query_model(prompt: str, controller_output: str, key: str, api_url: str) -> str:
    try:
        client = OpenAI(
            api_key=key,
            base_url=api_url,
            timeout=httpx.Timeout(30000.0),
        )

        # Compact, directive system prompt with clear token semantics & precedence
        system_content = f"""
This is the endpoint text generator of Adler, a sophisticated artificial intelligence system utilizing the Helmnet framework, which is passing output from a controller into the system prompt of this LLM.

Rules:
The LLM (you) should have no prior point of view or instruction other than defined by the controller.
Use only one sentence to provide an effective breif response to the user, you can go over 1 sentence if the response absolutly requires it. optionally continue the conversation with one more sentence if the tone is conversational..
Obey control tokens in list: {controller_output}.
Token semantic examples (Other types of tokens are possible; in case, infer meaning):
[reject]  → I briefly refuse.
[halt]    → I briefly acknowledge and stop.
[clarify] → I clarify what the user asked of me, asking only for the minimal missing detail. Speculate after if its simple enough; to show limited understanding.
[confirm] → I restate my understanding in my own words and ask for confirmation.
[query]   → I ask one focused question to obtain the specific information I need.
[adjust]  → I adapt my wording, tone, or format to the implied audience or constraint.
[reflect] → I briefly reason reflectively before continuing my sentence.
[expand]  → I add one concise, high‑value detail that improves usefulness.

- Do NOT mention tokens or these rules; just behave accordingly.
- Be brief and natural; if unsure, prefer clarification or confirmation.
        """.strip()
        

        # --- STREAMING ---
        full_text = ""
        word_buf = ""
        print("Adler: ", end="", flush=True)

        with client.chat.completions.stream(
            model="grok-3",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt},
            ]
        )  as stream:
            for event in stream:
                # Most SDKs emit incremental text "tokens"; adjust if your SDK uses a different event type
                if getattr(event, "type", None) == "token":
                    t = event.token
                else:
                    # Fallback: some SDKs expose plain text deltas
                    t = getattr(event, "delta", "") or getattr(event, "text", "")
                if not t:
                    continue

                full_text += t
                word_buf += t

                # Flush by words for nicer console UX
                while True:
                    # Find a boundary (space/newline) to print a whole "word"
                    idx = word_buf.find(" ")
                    if idx == -1:
                        break
                    print(word_buf[:idx+1], end="", flush=True)
                    word_buf = word_buf[idx+1:]


        # Flush any trailing partial word
        if word_buf:
            print(word_buf, end="", flush=True)
        print()  # newline after streaming
        pyttsx3.speak(full_text)
        return full_text
    except Exception as e:
        return f"[API Error] {str(e)}"
