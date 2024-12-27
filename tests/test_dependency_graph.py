import unittest
from unittest.mock import Mock

from gauss_elimination import LinearSystem
from nodes import *


class TestDependencyGraph(unittest.TestCase):
    def setUp(self):
        self.mock_system = Mock()

        self.expected_graph = {}

        a21 = A(self.mock_system, 1, 0)
        a31 = A(self.mock_system, 2, 0)
        a32 = A(self.mock_system, 2, 1)

        b211 = B(self.mock_system, 1, 0, 0)
        b231 = B(self.mock_system, 1, 2, 0)
        b221 = B(self.mock_system, 1, 1, 0)
        b241 = B(self.mock_system, 1, 3, 0)
        b311 = B(self.mock_system, 2, 0, 0)
        b321 = B(self.mock_system, 2, 1, 0)
        b322 = B(self.mock_system, 2, 1, 1)
        b331 = B(self.mock_system, 2, 2, 0)
        b332 = B(self.mock_system, 2, 2, 1)
        b341 = B(self.mock_system, 2, 3, 0)
        b342 = B(self.mock_system, 2, 3, 1)

        c211 = C(self.mock_system, 1, 0, 0)
        c221 = C(self.mock_system, 1, 1, 0)
        c231 = C(self.mock_system, 1, 2, 0)
        c241 = C(self.mock_system, 1, 3, 0)
        c311 = C(self.mock_system, 2, 0, 0)
        c321 = C(self.mock_system, 2, 1, 0)
        c322 = C(self.mock_system, 2, 1, 1)
        c331 = C(self.mock_system, 2, 2, 0)
        c332 = C(self.mock_system, 2, 2, 1)
        c341 = C(self.mock_system, 2, 3, 0)
        c342 = C(self.mock_system, 2, 3, 1)

        self.expected_graph[a21] = [b211, b221, b231, b241]
        self.expected_graph[b211] = [c211]
        self.expected_graph[c211] = []
        self.expected_graph[a31] = [b311, b321, b331, b341]
        self.expected_graph[b311] = [c311]
        self.expected_graph[c311] = []
        self.expected_graph[b231] = [c231]
        self.expected_graph[b221] = [c221]
        self.expected_graph[b241] = [c241]
        self.expected_graph[b321] = [c321]
        self.expected_graph[b331] = [c331]
        self.expected_graph[b341] = [c341]
        self.expected_graph[c321] = [a32]
        self.expected_graph[c221] = [a32]
        self.expected_graph[c231] = [b332]
        self.expected_graph[c241] = [b342]
        self.expected_graph[a32] = [b322, b332, b342]
        self.expected_graph[c341] = [c342]
        self.expected_graph[c331] = [c332]
        self.expected_graph[b322] = [c322]
        self.expected_graph[b332] = [c332]
        self.expected_graph[b342] = [c342]
        self.expected_graph[c322] = []
        self.expected_graph[c332] = []
        self.expected_graph[c342] = []

        self.system = LinearSystem(3)

    def test_graph_vertices(self):
        self.assertEqual(set(self.expected_graph.keys()), set(self.system.nodes.keys()))

    def test_graph_edges(self):
        for node, expected_children in self.expected_graph.items():
            actual_children = self.system.nodes[node].children
            self.assertEqual(expected_children, actual_children,
                             msg=f"Assertion failed for node {node}. "
                                 f"Expected children: {expected_children}, "
                                 f"Actual children: {actual_children}"
                             )


if __name__ == "__main__":
    unittest.main()
