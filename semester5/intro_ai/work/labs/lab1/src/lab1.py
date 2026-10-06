import math
import random

import matplotlib.pyplot as plt
import networkx as nx


def validate_args(nodes_num, edges_to_delete, min_weight, max_weight):
    k = math.isqrt(nodes_num)
    if k * k != nodes_num:
        raise ValueError("nodes_num має бути повним квадратом")

    max_edges_to_delete = (k - 1) ** 2
    if edges_to_delete < 0 or edges_to_delete > max_edges_to_delete:
        raise ValueError(
            f"edges_to_delete має бути від 0 до {max_edges_to_delete}"
        )

    if min_weight <= 0 or min_weight > max_weight:
        raise ValueError("Некоректний діапазон ваг ребер")


def create_graph(nodes_num=25, min_weight=1, max_weight=10):
    k = math.isqrt(nodes_num)
    nodes = []
    edges = []

    for row in range(k):
        for column in range(k):
            nodes.append((row, column))

    for node in nodes:
        row, column = node

        if row + 1 < k:
            edges.append(
                (
                    node,
                    (row + 1, column),
                    random.randint(min_weight, max_weight),
                )
            )

        if column + 1 < k:
            edges.append(
                (
                    node,
                    (row, column + 1),
                    random.randint(min_weight, max_weight),
                )
            )

    graph = nx.Graph()

    for node in nodes:
        graph.add_node(
            node,
            address=f"10.0.{node[0]}.{node[1]}",
        )

    for u, v, weight in edges:
        graph.add_edge(u, v, weight=weight)

    return graph


def show_graph(graph, highlighted_path=None, title="Топологія мережі"):
    positions = {
        node: (node[1], -node[0])
        for node in graph.nodes
    }

    highlighted_edges = set()
    if highlighted_path:
        highlighted_edges = {
            frozenset((u, v))
            for u, v in zip(highlighted_path, highlighted_path[1:])
        }

    node_colors = [
        "tomato" if highlighted_path and node in highlighted_path else "lightblue"
        for node in graph.nodes
    ]
    edge_colors = [
        "crimson"
        if frozenset((u, v)) in highlighted_edges
        else "gray"
        for u, v in graph.edges
    ]

    plt.figure(figsize=(10, 8))
    nx.draw(
        graph,
        positions,
        labels={
            node: graph.nodes[node].get("address", str(node))
            for node in graph.nodes
        },
        node_color=node_colors,
        edge_color=edge_colors,
        with_labels=True,
        node_size=1600,
        font_size=8,
        width=2,
    )
    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=nx.get_edge_attributes(graph, "weight"),
        font_size=8,
    )
    plt.title(title)
    plt.axis("off")
    plt.show()


def remove_edges(graph, edges_to_delete):
    edges = list(graph.edges())
    random.shuffle(edges)
    removed = 0

    while removed < edges_to_delete and edges:
        u, v = edges.pop()
        edge_weight = graph[u][v]["weight"]
        graph.remove_edge(u, v)

        if nx.is_connected(graph):
            removed += 1
        else:
            graph.add_edge(u, v, weight=edge_weight)

    if removed != edges_to_delete:
        raise ValueError("Не вдалося видалити задану кількість ребер")
