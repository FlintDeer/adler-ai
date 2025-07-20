import argparse, numpy as np, random
import pickle
import os
import atexit
from collections import defaultdict      # keep this if it isn’t already imported
from sentence_transformers import SentenceTransformer

DB_FILE = "mem.pkl"                      # where we’ll save the state

# ---- Load existing memory (if any) ----
if os.path.exists(DB_FILE):
    vectors, edges = pickle.load(open(DB_FILE, "rb"))
else:
    vectors, edges = {}, defaultdict(dict)

# ---- Automatically save on program exit ----
def _save_on_exit():
    with open(DB_FILE, "wb") as f:
        pickle.dump((vectors, edges), f)

atexit.register(_save_on_exit)

MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DIM = MODEL.get_sentence_embedding_dimension()   # 384
ETA = 0.5
DECAY = 0.9
MAX_HOPS = 3

def random_vec():
    v = np.random.randn(DIM)
    return v / np.linalg.norm(v)

def store(mem_id, text):
    vec = MODEL.encode(text, normalize_embeddings=True)
    vectors[mem_id] = vec
    print(f"stored {mem_id}")

def associate(ids):
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            a, b = ids[i], ids[j]
            w = edges[a].get(b, 0.0) + ETA
            w = min(w, 1.0)
            edges[a][b] = edges[b][a] = w
    print(f"associated {ids}")

def recall(k, cue_id):
    cue_vec = vectors[cue_id]
    scores = {m: float(cue_vec @ v) for m, v in vectors.items()}
    frontier = dict(scores)          # start spread with cosine sims
    for _ in range(MAX_HOPS):
        nxt = {}
        for node, strength in frontier.items():
            for neigh, w in edges[node].items():
                prop = strength * w * DECAY
                if prop > scores.get(neigh, 0):
                    scores[neigh] = prop
                    nxt[neigh] = prop
        frontier = nxt
    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
    print("top recall:", best)

def repl():
    print("Interactive memory shell.  Ctrl-C or Ctrl-D to quit.")
    while True:
        try:
            line = input("mem> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0]
        if cmd == "add" and len(parts) >= 3:
            store(parts[1], " ".join(parts[2:]))
        elif cmd == "assoc":
            associate(parts[1:])
        elif cmd == "recall":
            k = int(parts[2]) if len(parts) > 3 and parts[1] == "-k" else 5
            cue = parts[-1]
            recall(k, cue)
        elif cmd == "graph": import show_graph 
        elif cmd == "batch" and len(parts) == 2:
            # syntax: batch FILENAME
            for line in open(parts[1], "r", encoding="utf-8"):
                line = line.strip()
                if not line: continue
                # first word becomes the ID, rest = sentence
                mem_id, *words = line.split()
                store(mem_id, " ".join(words))
            print("✓ batch loaded")
        else:
            print("command not found")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    add = sub.add_parser("add")
    add.add_argument("id")
    add.add_argument("text", nargs="+") # capture rest of line
    sub.add_parser("assoc").add_argument("ids", nargs="+")
    sub.add_parser("repl")
    sub.add_parser("graph")
    rec = sub.add_parser("recall")
    rec.add_argument("cue_id")
    rec.add_argument("-k", type=int, default=5)
    args = ap.parse_args()

    if args.cmd == "add": store(args.id, " ".join(args.text))
    elif args.cmd == "assoc": associate(args.ids)
    elif args.cmd == "recall": recall(args.k, args.cue_id)
    elif args.cmd == "repl": repl()

if __name__ == "__main__":
    main()

