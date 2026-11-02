import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestCli(unittest.TestCase):
    def run_cli(self, graph_data, *extra):
        with tempfile.TemporaryDirectory() as tmp:
            graph_file = Path(tmp) / "graph.json"
            graph_file.write_text(json.dumps(graph_data), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "pathfinder.cli", str(graph_file), *extra],
                cwd=ROOT / "src", capture_output=True, text=True, check=False,
            )
            return result

    def test_dijkstra_output(self):
        result = self.run_cli(
            [["A", "B", 1], ["B", "D", 1], ["A", "D", 10]],
            "--from", "A", "--to", "D",
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("A -> B -> D", result.stdout)
        self.assertIn("cost: 2", result.stdout)

    def test_no_path_exits_nonzero(self):
        result = self.run_cli([["A", "B", 1]], "--from", "A", "--to", "Z")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
