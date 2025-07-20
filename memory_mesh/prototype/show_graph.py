import pickle, os, math
import networkx as nx
import matplotlib.pyplot as plt

DB_FILE = "mem.pkl"
THRESH  = 0.05        # only draw edges stronger than this

if not os.path.exists(DB_FILE):
    raise SystemExit("➡  No mem.pkl to visualise yet")

vectors, edges = pickle.load(open(DB_FILE, "rb"))

G = nx.Graph()
G.add_nodes_from(vectors.keys())

for a, nbrs in edges.items():
    for b, w in nbrs.items():
        if a < b and w >= THRESH:      # a<b avoids duplicating undirected edges
            G.add_edge(a, b, weight=w)

# simple spring layout
pos = nx.spring_layout(G, k=0.8/ math.sqrt(len(G.nodes())), seed=42)

weights = [G[u][v]['weight'] for u,v in G.edges()]
max_w = max(weights) if weights else 1
colors = [w / max_w for w in weights] 

plt.figure(figsize=(8, 6))
nx.draw_networkx_edges(
    G, pos, 
    alpha=0.9, 
    width=[3*w for w in weights],
    edge_color = colors,
    edge_vmin=0.0, edge_vmax=1.0,
    edge_cmap=plt.cm.Blues, 
)
nx.draw_networkx_nodes(G, pos, node_size=700)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Memory Association Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig("memory_graph.png", dpi=300)
print("✅  Saved memory_graph.png")
