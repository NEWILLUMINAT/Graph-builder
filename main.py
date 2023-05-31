import copy

import networkx as nx
import matplotlib.pyplot as plt


def havel_hakimi_algorithm(sequence):
    sequence.sort(reverse=True)
    indexing_sequence = [[i, sequence[i]] for i in range(len(sequence))]
    edges = []
    first_elem = indexing_sequence[0][1]
    while first_elem > 0:
        if first_elem > len(indexing_sequence):
            return None
        if sum(sequence) % 2 != 0:
            return None
        if not is_graphical(sequence):
            return None
        k = first_elem
        for i in range(0, k):
            target = indexing_sequence[i + 1][0]
            source = indexing_sequence[0][0]
            edges.append((source, target))
            indexing_sequence[0][1] -= 1
            indexing_sequence[i + 1][1] -= 1
        indexing_sequence = indexing_sequence[1:]
        indexing_sequence.sort(key=lambda pair: pair[1], reverse=True)
        first_elem = indexing_sequence[0][1]

    return edges

def is_graphical(seq):
    for k in range(1, len(seq) - 1):
        s = sum(seq[:k])
        sum_of_min = sum([min(i, seq[i]) for i in range(k + 1, len(seq))])
        if s > k * (k - 1) + sum_of_min:
            return False
    return True


def construct_graphs(edges):
    g_nx = nx.Graph()
    g_nx.add_edges_from(edges)
    graphs = [g_nx]
    list_edges = get_list_edges(edges)
    stack = [list_edges]
    while stack:
        g = stack.pop()
        nodes = g.keys()
        for key in nodes:
            targets = g[key]
            if len(targets) == len(nodes) - 1:
                continue
            free_nodes = set(nodes).difference(set(targets).union({key}))
            for target in g[key]:
                for free_n in free_nodes:
                    new_targets = set(g[free_n]).difference(targets)
                    for n_target in new_targets:
                        if target in g[n_target]:
                            continue
                        new_g = try_switch_edges(key, target, free_n, n_target, g)
                        g2 = nx.Graph()
                        ed = get_edges(new_g)
                        g2.add_edges_from(ed)

                        for gr in graphs:
                            if nx.is_isomorphic(gr, g2):
                                break
                        else:
                            graphs.append(g2)
                            stack.append(new_g)

    return graphs


def try_switch_edges(x, y, u, v, list_edges) -> dict[int, list]:
    list_copy = copy.deepcopy(list_edges)
    list_copy[x].remove(y)
    list_copy[x].append(u)

    list_copy[y].remove(x)
    list_copy[y].append(v)

    list_copy[u].remove(v)
    list_copy[u].append(x)

    list_copy[v].remove(u)
    list_copy[v].append(y)
    return list_copy


def get_list_edges(g: list[(int, int)]) -> dict[int, list]:
    list_edges = dict()
    for u, v in g:
        if u in list_edges:
            list_edges[u].append(v)
        else:
            list_edges[u] = [v]
        if v in list_edges:
            list_edges[v].append(u)
        else:
            list_edges[v] = [u]
    return list_edges


def get_edges(g: dict[int, list]) -> list[(int, int)]:
    s = set()
    for key in g.keys():
        for t in g[key]:
            if (key, t) not in s and (t, key) not in s:
                s.add((key, t))
    return list(s)


def draw(g):
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True)
    edge_labels = {(u, v): f"{u}-{v}" for u, v in g.edges()}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    plt.show()


edges = havel_hakimi_algorithm([3, 3, 2, 2, 1, 1])
print(edges)
if edges:
    graphs = construct_graphs(edges)
    for g in graphs:
        draw(g)
