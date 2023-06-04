import json

with open("data/item_mapping.json") as f:
    mapping = json.load(f)

with open("data/history.json") as f:
    history = json.load(f)
    print("H",len(history))

with open("data/recommendations.json") as f:
    rec = json.load(f)
    print("R", len(rec))

users = list(rec.keys())

nodes = []
edges_rated = []
edges_rcvd = []
for user in users[:10]:    
    rated = history[user]
    rcvd = list(rec[user].keys())

    # graph creation
    user = int(user)
    nodes.append(-user)
    for m in rated[:10]:
        m = int(m)
        nodes.append(m)
        edges_rated.append((-user, m))
    
    for m in rcvd[:10]:
        m = int(m)
        nodes.append(m)
        edges_rcvd.append((-user, m))

nodes = set(nodes)
edges_rated = set(edges_rated)
edges_rcvd = set(edges_rcvd)

D = {
    "nodes": [],
    "edges": []
}
entities = {}
id = 0
for n in nodes:
    item = {
        'id': id,
        'labelC': f'user_{-n}' if n < 0 else mapping[str(n)]['title'],
        'group': 1 if n < 0 else 2,
    }
    entities[n] = id
    id += 1
    D['nodes'].append(item)

for e in edges_rated:
    item = {
        "from": entities[e[0]],
        "to": entities[e[1]],
        "group": 1
    }
    D['edges'].append(item)
    

for e in edges_rcvd:
    item = {
        "from": entities[e[0]],
        "to": entities[e[1]],
        "group": 2
    }
    D['edges'].append(item)

with open("full_kg.json", "w") as f:
    json.dump(D, f, indent=4)
