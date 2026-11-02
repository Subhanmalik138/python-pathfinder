"""Shortest-path algorithms.

All three return ``(path, cost)`` where ``path`` is the list of nodes from
source to target inclusive, or ``(None, inf)`` when no path exists.
Unknown source/target nodes raise ``ValueError`` instead of silently
returning "no path" — a typo in a node name is a caller bug, not an
unreachable destination.
"""

from __future__ import annotations

import heapq
import math
from collections import deque

from .graph import Graph


def _check_nodes(graph: Graph, source: object, target: object) -> None:
    if not graph.has_node(source):
        raise ValueError(f"unknown source node {source!r}")
    if not graph.has_node(target):
        raise ValueError(f"unknown target node {target!r}")


def _reconstruct(previous: dict[object, object], source: object, target: object) -> list[object]:
    path = [target]
    while path[-1] != source:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def dijkstra(graph: Graph, source: object, target: object):
    """Dijkstra's algorithm: shortest path in a non-negatively weighted graph."""
    _check_nodes(graph, source, target)
    if source == target:
        return [source], 0.0
    dist = {source: 0.0}
    previous: dict[object, object] = {}
    heap = [(0.0, source)]
    visited: set[object] = set()
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            return _reconstruct(previous, source, target), cost
        for neighbor, weight in graph.neighbors(node).items():
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, math.inf):
                dist[neighbor] = new_cost
                previous[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))
    return None, math.inf


def bfs_shortest_path(graph: Graph, source: object, target: object):
    """Breadth-first search: fewest-edges path (edge weights ignored)."""
    _check_nodes(graph, source, target)
    if source == target:
        return [source], 0
    previous: dict[object, object] = {}
    seen = {source}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for neighbor in graph.neighbors(node):
            if neighbor in seen:
                continue
            seen.add(neighbor)
            previous[neighbor] = node
            if neighbor == target:
                path = _reconstruct(previous, source, target)
                return path, len(path) - 1
            queue.append(neighbor)
    return None, math.inf


def a_star(graph: Graph, source: object, target: object, heuristic=None):
    """A* search. ``heuristic(node, target)`` estimates remaining cost.

    With no heuristic (default) it behaves like Dijkstra. The heuristic
    must be admissible (never overestimate) for the result to stay optimal;
    the function trusts the caller's heuristic and does not validate it.
    """
    _check_nodes(graph, source, target)
    if source == target:
        return [source], 0.0
    estimate = heuristic or (lambda _node, _target: 0.0)
    g_score = {source: 0.0}
    previous: dict[object, object] = {}
    heap = [(estimate(source, target), 0.0, source)]
    visited: set[object] = set()
    while heap:
        _f, cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            return _reconstruct(previous, source, target), cost
        for neighbor, weight in graph.neighbors(node).items():
            new_cost = cost + weight
            if new_cost < g_score.get(neighbor, math.inf):
                g_score[neighbor] = new_cost
                previous[neighbor] = node
                heapq.heappush(heap, (new_cost + estimate(neighbor, target), new_cost, neighbor))
    return None, math.inf
