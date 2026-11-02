import math
import unittest

from pathfinder import Graph, a_star, bfs_shortest_path, dijkstra


def city_graph():
    # A -> B (1), A -> C (4), B -> C (2), B -> D (5), C -> D (1).
    # Shortest A -> D is A-B-C-D at cost 4, not the direct-looking A-C-D (5).
    return Graph.from_edges([
        ("A", "B", 1), ("A", "C", 4), ("B", "C", 2),
        ("B", "D", 5), ("C", "D", 1),
    ])


class TestDijkstra(unittest.TestCase):
    def test_prefers_cheaper_indirect_route(self):
        path, cost = dijkstra(city_graph(), "A", "D")
        self.assertEqual(path, ["A", "B", "C", "D"])
        self.assertEqual(cost, 4)

    def test_source_equals_target(self):
        self.assertEqual(dijkstra(city_graph(), "A", "A"), (["A"], 0.0))

    def test_unreachable_returns_none_and_inf(self):
        graph = Graph.from_edges([("A", "B", 1)])
        graph.add_node("Z")
        path, cost = dijkstra(graph, "A", "Z")
        self.assertIsNone(path)
        self.assertEqual(cost, math.inf)

    def test_unknown_node_raises(self):
        with self.assertRaises(ValueError):
            dijkstra(city_graph(), "A", "Nope")

    def test_undirected_graph_traverses_both_ways(self):
        graph = Graph.from_edges([("A", "B", 3)], directed=False)
        self.assertEqual(dijkstra(graph, "B", "A"), (["B", "A"], 3.0))


class TestBfs(unittest.TestCase):
    def test_fewest_edges_not_cheapest_weight(self):
        # Direct edge A -> D costs 10 but is one hop; BFS must pick it.
        graph = Graph.from_edges([
            ("A", "B", 1), ("B", "D", 1), ("A", "D", 10),
        ])
        path, cost = bfs_shortest_path(graph, "A", "D")
        self.assertEqual(path, ["A", "D"])
        self.assertEqual(cost, 1)

    def test_unreachable(self):
        graph = Graph.from_edges([("A", "B", 1)])
        graph.add_node("Z")
        path, cost = bfs_shortest_path(graph, "A", "Z")
        self.assertIsNone(path)
        self.assertEqual(cost, math.inf)


class TestAStar(unittest.TestCase):
    def test_matches_dijkstra_with_admissible_heuristic(self):
        graph = city_graph()
        positions = {"A": (0, 0), "B": (1, 0), "C": (2, 0), "D": (3, 0)}

        def heuristic(node, target):
            return abs(positions[node][0] - positions[target][0])

        path, cost = a_star(graph, "A", "D", heuristic)
        self.assertEqual(path, ["A", "B", "C", "D"])
        self.assertEqual(cost, 4)

    def test_no_heuristic_equals_dijkstra(self):
        graph = city_graph()
        self.assertEqual(a_star(graph, "A", "D"), dijkstra(graph, "A", "D"))


class TestGraph(unittest.TestCase):
    def test_negative_weight_rejected(self):
        graph = Graph()
        with self.assertRaises(ValueError):
            graph.add_edge("A", "B", -1)

    def test_two_item_edge_defaults_to_weight_one(self):
        graph = Graph.from_edges([("A", "B")])
        self.assertEqual(graph.neighbors("A"), {"B": 1.0})


if __name__ == "__main__":
    unittest.main()
