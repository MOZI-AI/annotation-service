__author__ = 'Abdulrahman Semrie<hsamireh@gmail.com>'

import json
import uuid
import time
import networkx as nx
import logging

logger = logging.getLogger("annotation-service")
col = {}
edges = {}
_attrs = dict(name='name', ident='id')


def multi_level_layout(path):
    t0 = time.time()
    with open(path) as fp:
        graph_dict = json.load(fp)

    graph = nx.Graph()

    # Add the nodes
    for node in graph_dict["nodes"]:
        data = node["data"]
        graph.add_node(data["id"])

    # Add edges
    for edge in graph_dict["edges"]:
        data = edge["data"]
        graph.add_edge(data["source"], data["target"])

    graph_size = len(graph)
    if graph_size >= 600:
        graph_scale = 6000
        node_space = 380
    else:
        graph_scale = 4000
        node_space = 300

    G, level = generate_coarser_graph(graph, 0)
    pos = nx.spring_layout(G, scale=graph_scale, k=node_space)

    FG, position = generate_finer_graph(G, level - 1, pos, graph_scale, node_space)
    position = nx.spring_layout(FG, scale=graph_scale, pos=position, k=node_space)
    for k, v in position.items():
        position[k] = {"x": v[0], "y": v[1]}

    nx.set_node_attributes(graph, position, "position")

    for node in graph_dict["nodes"]:
        node["position"] = graph.nodes[node["data"]["id"]]["position"]

    for edge in graph_dict["edges"]:
        edge["data"]["id"] = str(uuid.uuid4())

    t1 = time.time()
    logger.info("Total time: {0} seconds".format(t1 - t0))

    return graph_dict


def cytoscape_data(G, OG, attrs=None):
    """Returns data in Cytoscape JSON format (cyjs).

    Parameters
    ----------
    G : NetworkX Graph


    Returns
    -------
    data: dict
        A dictionary with cyjs formatted data.
    Raises
    ------
    NetworkXError
        If values in attrs are not unique.
    """
    if not attrs:
        attrs = _attrs
    else:
        attrs.update({k: v for (k, v) in _attrs.items() if k not in attrs})

    name = attrs["name"]
    ident = attrs["ident"]

    if len(set([name, ident])) < 2:
        raise nx.NetworkXError('Attribute names are not unique.')

    jsondata = {"data": list(G.graph.items()), 'directed': G.is_directed(), 'multigraph': G.is_multigraph(),
                "elements": {"nodes": [], "edges": []}}
    nodes = jsondata["elements"]["nodes"]
    edges = jsondata["elements"]["edges"]

    for i, j in G.nodes.items():
        n = OG["nodes"][str(i)]
        n["position"] = j["position"]
        nodes.append(n)

    if G.is_multigraph():
        for e in G.edges(keys=True):
            n = {"data": G.adj[e[0]][e[1]][e[2]].copy()}
            n["data"]["source"] = e[0]
            n["data"]["target"] = e[1]
            n["data"]["key"] = e[2]
            edges.append(n)
    else:
        for e, j in G.edges().items():
            n = dict(data={})
            n["data"]["id"] = str(uuid.uuid4())
            n["position"] = {"x": 0, "y": 0}
            n["data"]["source"] = e[0]
            n["data"]["target"] = e[1]
            for k, v in j.items():
                n[k] = v
            edges.append(n)
    return jsondata


def generate_coarser_graph(G, level):
    if G.number_of_nodes() <= 2: return G, level

    # sort the edges

    col[level] = {}
    edges[level] = {}

    mie = nx.maximal_matching(G)
    if (len(mie)) == 0:
        return G, level
    for i in mie:
        new_node = "{0}-{1}".format(i[0], i[1])
        G.add_node(new_node)
        col[level][new_node] = list(i)
        c1, c2 = i[0], i[1]
        cn1, cn2 = list(G.adj[c1]), list(G.adj[c2])
        G.remove_node(c1)
        G.remove_node(c2)
        edges[level][new_node] = []
        for i in cn1:
            if i == c1 or i == c2: continue
            G.add_edge(i, new_node)
            edges[level][new_node].append((i, c1))

        for i in cn2:
            if i == c1 or i == c2: continue
            G.add_edge(i, new_node)
            edges[level][new_node].append((i, c2))
    return generate_coarser_graph(G, level + 1)


def generate_finer_graph(G, level, position, scale, k):
    if level < 0: return G, position
    for n in col[level]:
        cn1, cn2 = col[level][n][0], col[level][n][1]
        # set the node positions
        G.add_node(cn1, group="nodes")
        G.add_node(cn2, group="nodes")
        G.add_edge(cn1, cn2, group="edges")
        for c1, c2 in edges[level][n]:
            G.add_edge(c1, c2, group="edges")

    G.remove_nodes_from(col[level].keys())
    nPos = nx.spring_layout(G, scale=scale, pos=position, k=k)
    return generate_finer_graph(G, level - 1, nPos, scale, k)
