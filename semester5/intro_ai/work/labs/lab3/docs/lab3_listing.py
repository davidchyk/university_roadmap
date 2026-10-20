import random
import sys
from math import inf
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

lab1_src = Path.cwd().parents[1] / 'lab1' / 'src'
sys.path.insert(0, str(lab1_src))
from lab1 import create_graph, remove_edges, validate_args

class KnowledgeBase:
    def __init__(self):
        self.graph = nx.Graph()
        self.announcements = []

    def tell(self, source, observations):
        self.graph.add_node(source)
        for u, v, weight in observations:
            self.graph.add_edge(u, v, weight=weight)
        self.announcements.append({
            'source': source,
            'observations': list(observations),
        })

    def ask_next_hop(self, current, target, blocked):
        if target not in self.graph or current not in self.graph:
            return None
        known = self.graph.copy()
        for node in blocked:
            if node not in (current, target) and node in known:
                known.remove_node(node)
        try:
            path = nx.shortest_path(known, current, target, weight='weight')
        except nx.NetworkXNoPath:
            return None
        return path[1] if len(path) > 1 else target

    def shortest_path(self, start, target):
        try:
            return nx.shortest_path(self.graph, start, target, weight='weight')
        except (nx.NodeNotFound, nx.NetworkXNoPath):
            return None

def edge_weight(graph, u, v):
    return float(graph[u][v].get('weight', 1))


def observe(graph, current):
    observations = set()
    local_nodes = {current, *graph.neighbors(current)}
    for node in local_nodes:
        for neighbor in graph.neighbors(node):
            u, v = sorted((node, neighbor))
            observations.add((u, v, edge_weight(graph, node, neighbor)))
    return list(observations)


def address(graph, node):
    return str(graph.nodes[node].get('address', node))


def path_delay(graph, path):
    if path is None:
        return inf
    return sum(edge_weight(graph, u, v) for u, v in zip(path, path[1:]))


def knowledge_based_agent(graph, start, target):
    knowledge = KnowledgeBase()
    path = [start]
    visited = {start}
    log = []
    installed_rules = 0
    revoked_rules = 0
    current = start

    while current != target:
        observations = observe(graph, current)
        knowledge.tell(current, observations)
        log.append(
            f'TELL: вузол {address(graph, current)}, '
            f'отримано анонсів: {len(observations)}'
        )

        next_node = knowledge.ask_next_hop(current, target, visited)
        if next_node is None:
            candidates = sorted(
                (
                    (neighbor, edge_weight(graph, current, neighbor))
                    for neighbor in graph.neighbors(current)
                    if neighbor not in visited
                ),
                key=lambda item: item[1],
            )
            next_node = candidates[0][0] if candidates else None

        if next_node is not None and next_node not in visited:
            installed_rules += 1
            visited.add(next_node)
            path.append(next_node)
            log.append(
                f'ASK: {address(graph, current)} -> '
                f'{address(graph, next_node)}'
            )
            current = next_node
            continue

        if len(path) == 1:
            return {
                'path': None, 'delay': inf,
                'installed': installed_rules, 'revoked': revoked_rules,
                'knowledge': knowledge, 'log': log,
            }

        previous = path.pop()
        current = path[-1]
        revoked_rules += 1
        log.append(
            f'RETRACT: відкликано правило до {address(graph, previous)}; '
            f'повернення до {address(graph, current)}'
        )

    return {
        'path': path,
        'delay': path_delay(graph, path),
        'installed': installed_rules,
        'revoked': revoked_rules,
        'knowledge': knowledge,
        'log': log,
    }

def greedy_agent(graph, start, target):
    visited = {start}
    path = [start]
    installed = 0
    revoked = 0

    def search(current):
        nonlocal installed, revoked
        if current == target:
            return True
        candidates = sorted(
            (
                (node, edge_weight(graph, current, node))
                for node in graph.neighbors(current)
                if node not in visited
            ),
            key=lambda item: item[1],
        )
        for node, _ in candidates:
            visited.add(node)
            path.append(node)
            installed += 1
            if search(node):
                return True
            path.pop()
            revoked += 1
        return False

    if not search(start):
        return {'path': None, 'delay': inf, 'installed': installed, 'revoked': revoked}
    return {'path': path, 'delay': path_delay(graph, path), 'installed': installed, 'revoked': revoked}


def dijkstra_path(graph, start, target):
    return nx.shortest_path(graph, start, target, weight='weight')


def draw_path(graph, path, title):
    positions = {node: (node[1], -node[0]) for node in graph.nodes}
    route_edges = {frozenset((u, v)) for u, v in zip(path or [], (path or [])[1:])}
    nx.draw(
        graph, positions,
        labels={node: address(graph, node) for node in graph.nodes},
        node_color=['tomato' if path and node in path else 'lightblue' for node in graph.nodes],
        edge_color=['crimson' if frozenset((u, v)) in route_edges else 'gray' for u, v in graph.edges],
        node_size=1500, font_size=8, width=2,
    )
    nx.draw_networkx_edge_labels(graph, positions, nx.get_edge_attributes(graph, 'weight'), font_size=8)
    plt.title(title)
    plt.axis('off')
    plt.show()

random.seed(42)
validate_args(25, 6, 1, 10)
graph = create_graph(25, 1, 10)
remove_edges(graph, 6)
start = (0, 0)
target = (4, 4)

knowledge_result = knowledge_based_agent(graph, start, target)
greedy_result = greedy_agent(graph, start, target)
optimal_path = dijkstra_path(graph, start, target)

print('Шлях агента ЛР2:', greedy_result['path'])
print('Затримка агента ЛР2:', greedy_result['delay'])
print('Шлях агента на основі знань:', knowledge_result['path'])
print('Затримка агента на основі знань:', knowledge_result['delay'])
print('Шлях Дейкстри:', optimal_path)
print('Затримка Дейкстри:', path_delay(graph, optimal_path))
print('Відкликано правил агентом на основі знань:', knowledge_result['revoked'])

plt.figure(figsize=(11, 8))
draw_path(graph, knowledge_result['path'], 'Маршрут агента на основі бази знань')

plt.figure(figsize=(11, 8))
draw_path(graph, optimal_path, 'Оптимальний маршрут за алгоритмом Дейкстри')

print('Фрагмент журналу TELL/ASK:')
for entry in knowledge_result['log'][:20]:
    print(entry)

print(f"{'№':>3} {'ЛР2':>10} {'KBA':>10} {'Дейкстра':>12} {'Вузли KBA':>12} {'Відклики KBA':>14}")
print('-' * 68)
for topology_number in range(1, 4):
    random.seed(100 + topology_number)
    test_graph = create_graph(25, 1, 10)
    remove_edges(test_graph, 6)
    old_result = greedy_agent(test_graph, start, target)
    new_result = knowledge_based_agent(test_graph, start, target)
    shortest = dijkstra_path(test_graph, start, target)
    print(
        f'{topology_number:>3} '
        f'{old_result["delay"]:>10g} '
        f'{new_result["delay"]:>10g} '
        f'{path_delay(test_graph, shortest):>12g} '
        f'{len(new_result["path"]):>12} '
        f'{new_result["revoked"]:>14}'
    )
