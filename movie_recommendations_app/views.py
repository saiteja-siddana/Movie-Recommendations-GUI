from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
import pickle,json,requests,re
from django.template.defaultfilters import register
import networkx as nx
import matplotlib.pyplot as plt 
from tqdm import tqdm
from graphviz import Digraph,Source
import os,pydot
from json import dumps
os.environ["PATH"] += os.pathsep + r"C:\Users\Sai Teja\Anaconda3\Library\bin\graphviz" # To include graphviz in a systempath

# Create your views here. 

DIR = os.path.dirname(__file__)
 

file_path1 = os.path.join(DIR,'data', 'recommendations.json')
file_path2 = os.path.join(DIR,'data','item_mapping.json')
file_path3 = os.path.join(DIR,'data','attribute_explanation.json')

rec_json = json.load(open(file_path1))
users = rec_json.keys()

item_json = json.load(open(file_path2))

exp_json = json.load(open(file_path3))

def id2movie(i):
    return item_json[str(i)]['title']

def graph(user,rec):
    exp = exp_json[user][rec]
    user = "user_" + user
    recI = rec
    if int(recI) in exp['matched_movies']:
        return
    rec = id2movie(rec)
    nodes = set([user, rec])
    nodesDict = {
        user: 1, # user group: 1
        rec: 2 # rec movie group: 2
    }

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
                nodesDict[A] = 3
                edges.append((A, rec))
                for m in movie_list[:5]: # rated movies
                    edges.append((user, id2movie(m)))
                    edges.append((id2movie(m), A))
                    nodes.add(id2movie(m))
                    nodesDict[id2movie(m)] = 4
                    if check(nodes, edges): break
            if check(nodes, edges): break
        if check(nodes, edges): break
    # print((user, rec))
    # print(f"Explanation Size: {len(nodes)} nodes, {len(edges)} edges")

    # ### GraphVIZ
    if len(exp['matched_movies']) > 0:
        f = Digraph('finite_state_machine', filename=os.path.join('cache',f'kgr_graph_user-{user}_item-{recI}.gv'), format='png')
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
    newNodes = {n: { 'id': i, 'labelC': str(n), 'group': nodesDict[n]} 
                            for i, n in enumerate(nodesDict)}
    if len(exp['matched_movies']) > 0:
        with open(os.path.join('cache',f'kgr_graph_user-{user}_item-{recI}.json'), 'w') as fjson:
            json.dump({
                'nodes': [v for n,v in newNodes.items()],
                'edges': [{"from": newNodes[u]['id'], "to": newNodes[v]['id']} for u,v in set(edges)]
            }, fjson, indent=4)

    return

#kgr_graph_user-user_957_item-356.gv
#file_path = os.path.join(DIR,'../cache/kgr_graph_user-user_957_item-356.gv')
#graph = pydot.graph_from_dot_file(file_path)
fp1 = os.path.join(DIR,'..','cache', 'kgr_graph_user-user_957_item-356.gv')
s = Source.from_file(fp1).source
fp2 = os.path.join(DIR,'full_kg.json')
f = open(fp2,"r")
data = json.load(f)
dataJSON = dumps(data)  


def base(request):
    context = {
        'users_available' : users,
        's':s,
        'data' : data,
        'dataJSON' : dataJSON
    }
    return render(request,"base.html",context)


def home(request,user,id):
    DIR = os.path.dirname(__file__)
    data1 = []
    img1 = []
    data2 = []
    datajson = []
    recs = []

    for i in rec_json[user]:
        l = str(user) + "_item-" + str(i) + ".gv.png"
        check = os.path.join("cache", f"kgr_graph_user-user_{l}")
        filepath = os.path.join("cache", f"kgr_graph_user-user_{l}") 
        if os.path.exists(check)==False:
            graph(user,i)
        #fp = os.path.join(DIR,r'..\cache\kgr_graph_user-user_'+str(user)+'_item-'+str(i)+'.json')
        k = str(user) + "_item-" + str(i) + ".json"
        check = os.path.join("cache", f"kgr_graph_user-user_{k}")
        fp = os.path.join("..", "cache", f"kgr_graph_user-user_{k}")
        if os.path.exists(check)==False:
            datajson.append({})
        else:
            fp = os.path.join(DIR,fp)
            f = open(fp,"r")
            data = json.load(f)
            data2.append(data)
            dataJSON = dumps(data)
            datajson.append(dataJSON)
            data1.append(id2movie(i))
            recs.append(i)
        img1.append(filepath)
    
    #result1 = zip(data1,datajson)
    result1 = zip(data1,recs)

    context = {
        'users_available' : users,
        'user' : user,
        'id' : id,
        'result1' : result1, 
        'data2' : data2,
        'datajson' : datajson, 
        'recs' : recs,
        'data1' : data1 
    }
    return render(request, "home.html", context)

def graphs(request,user,rec):
    data1=[]
    recs=[]
    for i in rec_json[user]:
        k = str(user) + "_item-" + str(i) + ".json"
        check = os.path.join("cache", f"kgr_graph_user-user_{k}")
        fp = os.path.join("..", "cache", f"kgr_graph_user-user_{k}")
        if os.path.exists(check)==True:
            data1.append(id2movie(i))
            recs.append(i)
    result1 = zip(data1,recs)
    k = str(user) + "_item-" + str(rec) + ".json"
    check = os.path.join("cache", f"kgr_graph_user-user_{k}")
    fp = os.path.join("..", "cache", f"kgr_graph_user-user_{k}")
    if os.path.exists(check)==False:
        data = {}
    else:
        fp = os.path.join(DIR,fp)
        f = open(fp,"r")
        data = json.load(f)
        data = dumps(data)
        data1.append(id2movie(i))
    context={
        'data':data,
        'users_available' : users,
        'user' : user,
        'rec' : rec,
        'result1' : result1
    }
    return render(request,"graph.html",context)