"""A minimal weighted graph with an adjacency-list representation.

Nodes are any hashable values (strings, ints, tuples). Edges carry a
non-negative weight; negative weights are rejected at insertion time so
Dijkstra's precondition is enforced where the data enters, not deep
inside the algorithm.
"""

from __future__ import annotations

from collections import defaultdict


class Graph:
    """Directed-by-default weighted graph.

    Pass ``directed=False`` for an undirected graph, in which case every
    added edge is mirrored.
    """

    def __init__(self, directed: bool = True) -> None:
        self.directed = directed
        self._adj: dict[object, dict[object, float]] = defaultdict(dict)

    def add_node(self, node: object) -> None:
        self._adj.setdefault(node, {})

    def add_edge(self, source: object, target: object, weight: float = 1.0) -> None:
        if weight < 0:
            raise ValueError(f"negative edge weight {weight!r} is not supported")
        self._adj[source][target] = float(weight)
        self.add_node(target)
        if not self.directed:
            self._adj[target][source] = float(weight)

    def neighbors(self, node: object) -> dict[object, float]:
        """Return ``{neighbor: weight}`` for ``node`` (empty if unknown)."""
        return dict(self._adj.get(node, {}))

    def nodes(self) -> list[object]:
        return list(self._adj)

    def has_node(self, node: object) -> bool:
        return node in self._adj

    @classmethod
    def from_edges(cls, edges, directed: bool = True) -> "Graph":
        """Build a graph from ``(source, target)`` or ``(source, target, weight)`` tuples."""
        graph = cls(directed=directed)
        for edge in edges:
            if len(edge) == 2:
                graph.add_edge(edge[0], edge[1])
            elif len(edge) == 3:
                graph.add_edge(edge[0], edge[1], edge[2])
            else:
                raise ValueError(f"edge must have 2 or 3 items, got {edge!r}")
        return graph
