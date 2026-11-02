# Pathfinder

Shortest-path algorithms over weighted graphs, with a small CLI — no
dependencies, standard library only.

Finding a route through a network shows up everywhere: road navigation,
network routing, game AI, dependency resolution. This package implements
the three algorithms that answer "what's the best route?" for the three
different meanings of "best": cheapest by weight (Dijkstra), fewest hops
(BFS), and cheapest with a guide towards the goal (A*).

## Algorithms

| Algorithm | Best for | Guarantee |
| --- | --- | --- |
| Dijkstra | Weighted graphs, no heuristic available | Optimal, non-negative weights only |
| BFS | Unweighted graphs / fewest edges | Optimal in hop count |
| A* | Grids and maps with coordinates | Optimal if the heuristic never overestimates |

All three return `(path, cost)`, or `(None, inf)` when no path exists.

## Design decisions

1. **Negative weights are rejected at insertion, not in the algorithm.**
   Dijkstra silently returns wrong answers on negative edges, so `Graph.add_edge`
   raises `ValueError` immediately — the bug surfaces where the bad data enters.
2. **Unknown nodes raise instead of returning "no path".** A misspelled node
   name is a caller bug, not an unreachable destination, so it gets an error
   rather than a misleading empty result.
3. **Heuristics are plain callables.** A* takes any `heuristic(node, target)`
   function, so callers can plug in Manhattan distance, Euclidean distance,
   or a domain-specific estimate without touching the algorithm.

## Usage

```python
from pathfinder import Graph, dijkstra, a_star

graph = Graph.from_edges([
    ("A", "B", 1), ("A", "C", 4), ("B", "C", 2), ("C", "D", 1),
])
path, cost = dijkstra(graph, "A", "D")
print(path, cost)  # ['A', 'B', 'C', 'D'] 4.0
```

Undirected graphs: `Graph(directed=False)` mirrors every edge.

## CLI

```bash
PYTHONPATH=src python -m pathfinder.cli examples/cities.json --from A --to D
PYTHONPATH=src python -m pathfinder.cli examples/cities.json --from A --to D --algorithm bfs
PYTHONPATH=src python -m pathfinder.cli examples/cities.json --from A --to D --algorithm astar --positions examples/positions.json
```

Graph JSON is a list of edges (`["A", "B", 2.5]`, weight optional) or an
object `{"directed": false, "edges": [...]}`.

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Tech stack

Python 3.10+ standard library only. No third-party dependencies.
