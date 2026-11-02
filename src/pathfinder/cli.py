"""Command-line interface.

Graph input is JSON: either a list of edges
``[["A", "B", 2.5], ["B", "C"]]`` or an object
``{"directed": false, "edges": [["A", "B", 1]]}``.
Coordinates for an A* heuristic can be supplied as a second JSON file
mapping node names to ``[x, y]`` pairs (Euclidean distance is used).

Example:
    python -m pathfinder.cli graph.json --from A --to D --algorithm dijkstra
"""

from __future__ import annotations

import argparse
import json
import math
import sys

from .algorithms import a_star, bfs_shortest_path, dijkstra
from .graph import Graph

ALGORITHMS = {"dijkstra": dijkstra, "bfs": bfs_shortest_path}


def load_graph(path: str) -> Graph:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        edges, directed = data["edges"], data.get("directed", True)
    else:
        edges, directed = data, True
    return Graph.from_edges(edges, directed=directed)


def load_positions(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return {node: tuple(coords) for node, coords in json.load(handle).items()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Find the shortest path in a graph.")
    parser.add_argument("graph", help="JSON file with edges")
    parser.add_argument("--from", dest="source", required=True, help="source node")
    parser.add_argument("--to", dest="target", required=True, help="target node")
    parser.add_argument("--algorithm", choices=["dijkstra", "bfs", "astar"], default="dijkstra")
    parser.add_argument("--positions", help="JSON file of node coordinates for A*")
    args = parser.parse_args(argv)

    try:
        graph = load_graph(args.graph)
        if args.algorithm == "astar":
            positions = load_positions(args.positions) if args.positions else {}

            def heuristic(node, target):
                if node not in positions or target not in positions:
                    return 0.0
                x1, y1 = positions[node]
                x2, y2 = positions[target]
                return math.hypot(x2 - x1, y2 - y1)

            path, cost = a_star(graph, args.source, args.target, heuristic)
        else:
            path, cost = ALGORITHMS[args.algorithm](graph, args.source, args.target)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if path is None:
        print(f"no path from {args.source} to {args.target}")
        return 1
    print(" -> ".join(str(node) for node in path))
    print(f"cost: {cost:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
