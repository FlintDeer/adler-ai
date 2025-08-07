**Description:**
* Inference yields a list of tokens, e.g. ["[clarify]", "[adjust]"].
* interpret_tokens turns that into: 
        
        "Ask for clarification or restate the question clearly. Adjust the focus to the most relevant concept."
* inject_hint creates the final prompt for the API:

        Ask for clarification or restate the question clearly. Adjust the focus to the most relevant concept.

        User: what’s your process?
        Adler: