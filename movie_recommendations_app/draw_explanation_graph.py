#!/usr/bin/env python
# coding: utf-8

import json
import os
# from graph_tool.all import *
import networkx as nx
import matplotlib.pyplot as plt 
from tqdm import tqdm
from graphviz import Digraph

# Extract data
# !unzip ../recommendation_jsons/new_recommendations_explanations.zip -d data/


print(os.listdir("./data/"))
print("Remove previous cache...")
os.system('rm cache/*')
print("CACHE --> ", os.listdir("./cache/"))

item_json = json.load(open("data/item_mapping.json"))
exp_json = json.load(open("data/attribute_explanation.json"))


def id2movie(i):
    return item_json[str(i)]['title']

def cache_exp(user, rec):
    # user = '1922'
    # rec = '110'
    exp = exp_json[user][rec]
    user = "user_" + user
    recI = rec
    if int(recI) in exp['matched_movies']:
        return
    rec = id2movie(rec)
    nodes = set([user, rec])

    #for m in exp['matched_movies']:
    #    nodes.append(id2movie(m))

    edges = []
    check = lambda V, E: (len(V) > 14) or (len(E) > 100)
    for a,v in exp['matched_attributes'].items():
        for attrib_value, movie_list in v.items():
            if len(attrib_value.strip()) > 0:
                A = f"[{a.upper()}]\n{attrib_value}"
                # A = attrib_value
                nodes.add(A)
                edges.append((A, rec))
                for m in movie_list[:5]: # rated movies
                    edges.append((user, id2movie(m)))
                    edges.append((id2movie(m), A))
                    nodes.add(id2movie(m))
                    if check(nodes, edges): break
            if check(nodes, edges): break
        if check(nodes, edges): break
    # print((user, rec))
    # print(f"Explanation Size: {len(nodes)} nodes, {len(edges)} edges")

    # ### GraphVIZ
    if len(exp['matched_movies']) > 0:
        f = Digraph('finite_state_machine', filename=f'cache/kgr_graph_user-{user}_item-{recI}.gv', format='png')
        # f = Digraph('finite_state_machine', filename='kgr_graph.gv')
        # f.attr(rankdir='LR', size='8,5')

        f.attr('node', shape='doublecircle')
        # f.attr('node', shape='circle')
        # for n in set(nodes):
        #    f.node(n.replace(":", " -"))

        for u,v in set(edges):
            f.edge(u.replace(":", " -"), v.replace(":", " -"))

        # f.render() # ooutput saved in pdf file in localdir
        # f.format = "png"
        f.render()
    else:
        pass
        # print(f"No entry found for {user, rec}")

    return

def cache_user(user):
    recs = list(exp_json[user].keys())
    for rec in recs:
        cache_exp(user, rec)
        
if __name__ == "__main__":
    
    users = list(exp_json.keys())
    # for user in tqdm(users):
    #     cache_user(user)
    
    from multiprocessing import Pool
    # pool = Pool(os.cpu_count()//2)
    pool = Pool(4)
    for _ in tqdm(pool.imap_unordered(cache_user, users), total=len(users)):
        pass