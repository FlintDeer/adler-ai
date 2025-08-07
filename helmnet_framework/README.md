## Concept Architechure

**Flowchart Diagram:**

[User Input] 
    ↓
[Lightweight Controller Transformer]
    ↓
[Prompt / Routing / Modulation Output]
    ↓
[Frozen Base LLM]
    ↓
[Final Output]

**Components:**

    * 1. Controller Transformer (small and dynamic)
        - Stores abstract vectors as functional 
          memory and conseptual knowledge.
        - Learns how to adapt to variably to 
          functions and contexts.
        - Can be trained locally.
        - Modules (undecided as of rn), ideas:
            - Memory bank. (vector store)
            - Meta-state encoder. (tracks internal context over time)
            - User model.

    * 2. Frozen Model (LLM)
        - Takes modified input. (promt or embeddings)
        - Never trained, just queried.

    * 3. Interpretative Modulation
        - Converts the controller's output into something the LLM can interpret:
            - Altered prompts.
            - Adapter masks.
            - Function selectors.
            - Token pre-conditioning.

