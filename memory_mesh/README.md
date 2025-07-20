## roadmap (short-term)
    - Refactor prototype into a package
        * memory_mesh/__init__.py → MemoryStore class exposing store(), associate(), recall(), decay().
    - Swap pickle for SQLite (or faiss + sqlite):
        * Table vectors(id TEXT PRIMARY KEY, embedding BLOB)
        * Table edges(a TEXT, b TEXT, weight REAL).
    - Expose an internal API to the Core Orchestrator
        * memory_mesh_client.py with simple function calls (if running in-process) or HTTP endpoints (if run as a daemon).
    - Hook into the reasoning loop
        * Before each LLM step: recall(k, current_context_id) → inject returned IDs as scratch-pad cues.
        * After successful task completion: associate(active_ids).
    - Add decay scheduling in the Bootstrapper’s heartbeat (e.g., every 10 min multiply all edge weights by 0.99).

Move pickle → SQLite, write 10-line loader/saver                # Durable, inspectable storage.                                 
Wrap `MemoryStore` in a tiny Flask service                      # Lets Core Orchestrator call it asynchronously.                
Auto-associate IDs that appear together in one reasoning step   # Gives true *passive* memory formation like in the design doc. 
Metrics: log edge-strength histogram every hour                 # Data for Self-Update to trim or reinforce memories.           
