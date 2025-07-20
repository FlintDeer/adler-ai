Adler AI Memory Mesh Design

1. Purpose
    Create a passive, association-based memory layer that mimics brain-style
    replay without imposing
2. Memory Representation
    - Every significant thought is embedded as a high-dimensional
    vector (opaque activation pattern).
    - Representation granularity varies with inferred salience:
       - Highnsalience: full text + metadata.
       - Lownsalience: centroid vector + sparse keywords.
3. Association Edges
    - Edges seeded by temporal conoccurrence; similarity later strengthens/weakens them.
    - Optionally allow inhibitory links to dampen competing memories.
4. Strength Update & Reinforcement
    - Edge/node strength decays exponentially over time.
    - Any retrieval (‘read’) boosts strength (Hebbian reinforcement).
    - Strategy can be swapped later; start with simple exp-decay + +1 boost on read.
5. Forgetting & Cold Storage
    - When strength < threshold, item exits active index but vector stays in cold store.
    - If a future cue re-embeds near that vector, strength resets and edges rebuild.
6. Integration with Reasoning Loop
    - Retrieval is implicit: each new thought is embedded; nearest neighbours + 2-hop
    expansion form a
    - The reasoning LLM need not call a tool—memory activation occurs automatically
    before each reasoning generation.
    - Thinking about a memory reinforces it, aligning with biological replay.
7. Open Parameters
    - Decay constant λ.
    - Boost value on read.
    - Active-index capacity before cold-storage eviction.
    - Inhibitory edge rules.
