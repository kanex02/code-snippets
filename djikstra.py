# Code for Dijkstra's Algorithm, as guided in COSC262 at the University of Canterbury.  
# Written by Kane Xie 2022. 

# USE:
# Sample format of graph. 
# On the first line, the first character denotes the type:
# D is for a directed graph, and U is for an undirected graph. 
# The second character is the number of nodes, and the third character indicates that the graph is weighted. 
# graph_string = """\
# D 3 W
# 1 0 3
# 2 0 1
# 1 2 1
# """
# 
# The call
# (dijkstra(adjacency_list(graph_string), start_node))
# returns a tuple (parents, distances)
# where 'parents' is a list of the parent nodes after the algorithm
# and 'distances' is a list of the shortest distance from each node to the root node. 

from math import inf

def dijkstra(adj_list, start):
    'Returns a tuple (parent_list, distance_list)'
    parent = [None for _ in range(len(adj_list))]
    distance = [inf for _ in range(len(adj_list))]
    in_tree = [False for _ in range(len(adj_list))]

    # set up the starting node
    in_tree[start] = True
    distance[start] = 0
    u = start

    # while not every node is in the tree
    while False in in_tree:

        # for every connection (other_node, weight) from node 'u', add the other node 'v' if it is not yet
        # in the tree or this connection is shorter than its previous one
        for v, weight in adj_list[u]:
            if (distance[v] == inf and not in_tree[v]) or distance[u] + weight < distance[v]:
                parent[v] = u
                distance[v]  = distance[u] + weight

        # grab the next vertex, add it to the tree, and start working on it
        w = next_vertex(in_tree, distance)
        in_tree[w] = True
        u = w

    return (parent, distance)


def next_vertex(in_tree, distance):
    'Returns the next closest node that is not yet in the tree.'
    next = in_tree.index(False)
    for v in range(len(in_tree)):
        if not in_tree[v] and distance[v] < distance[next]:
            next = v
    return next


def adjacency_list(graph_str):
    'Produces an adjacency list from a graph string. '
    lines = graph_str.splitlines()
    outarr = [[] for _ in range(int(lines[0].split()[1]))]

    # gets the type of the graph, where D is for a directed graph, and U is for an undirected graph
    typ = lines[0].split()[0]

    # for each line that follows, add a connection to the output array. If the graph is undirected, 
    # also add a connection in the opposite direction
    for line in lines[1:]:
        splitline = line.split()
        fromindex = int(splitline[0])
        toindex = int(splitline[1])
        weight = int(splitline[2]) if len(splitline) == 3 else None
        outarr[fromindex].append((toindex, weight))
        if typ == "U":
            outarr[toindex].append((fromindex, weight))


    return outarr