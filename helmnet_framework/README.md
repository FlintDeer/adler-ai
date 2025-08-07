**Description:**
    (A helm is the steering mechanism of a ship)
    The reason its called HelmNet is because this module, 
    as a framework, *"steers"*  the function of a LLM to 
    hopefully improve its memory and processing functionality 
    with a smaller (dynamic!!!) network to stand in as a sort 
    of way to learn by controlling the LLM's function.

## Concept Architechure

**Flowchart Diagram:**
    [User Input] 
    ↓
    [Controller (stub): interprets or modifies intent]
    ↓
    [Prompt Constructor: injects hint/context/etc]
    ↓
    [Wrapper sends full prompt to LLM]
    ↓
    [LLM Output]

**Components:**
    **1.**

        Controller Transformer (small and dynamic)
        - Stores abstract vectors as functional 
          memory and conseptual knowledge.
        - Learns how to adapt to variably to 
            functions and contexts.
        - Can be trained locally.
        - Modules (undecided as of rn), ideas:
            - Memory bank. (vector store)
            - Meta-state encoder. (tracks internal context over time)
            - User model.
**2.** 

    Frozen Model (LLM)
    - Takes modified input. (promt or embeddings)
    - Never trained, just queried.
**3.** 

    Interpretative Modulation
    - Converts the controller's output into something the LLM can interpret:
        - Altered prompts.
        - Adapter masks.
        - Function selectors.
        - Token pre-conditioning.

