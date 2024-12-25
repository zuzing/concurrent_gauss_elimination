import numpy as np
from concurrent.futures import ThreadPoolExecutor
from collections import deque
from typing import Tuple

from nodes import A


class Scheduler:
	def __init__(self, nodes):
		self.nodes = nodes

	def execute(self):
		in_degree = {node: len(node.parents) for node in self.nodes}
		ready_nodes = deque([node for node, degree in in_degree.items() if degree == 0])

		processed_count = 0

		with ThreadPoolExecutor() as executor:
			futures = {}

			while processed_count != len(self.nodes):
				if not ready_nodes:
					continue
				else:
					node = ready_nodes.popleft()
					futures[node] = executor.submit(node)
					processed_count += 1

					def on_complete(future, node=node):
						for child in node.children:
							in_degree[child] -= 1
							if in_degree[child] == 0:
								ready_nodes.append(child)

					futures[node].add_done_callback(on_complete)

			for future in futures.values():
				future.result()


class LinearSystem:
	def __init__(self, size: int):
		self.N = size
		self.nodes = {}

		self._build_tree()

		self.M = None
		self.m = None
		self.n = None

	def _build_tree(self):
		for r in range(1, self.N):
			a = A(self, r, 0)
			self.nodes[a] = a
			a.find_children()

	def solve(self, matrix: np.array, rhs: np.array) -> Tuple[np.ndarray, np.ndarray]:
		def backwards_substitution():
			for i in range(self.N-1, -1, -1):
				solution[i] = self.M[i, self.N]
				for j in range(i+1, self.N):
					solution[i] -= self.M[i, j] * solution[j]
				solution[i] /= self.M[i, i]

		self.M = np.array([np.append(np.copy(row),rhs[i]) for i, row in enumerate(matrix)])
		self.m = np.zeros((self.N, self.N))
		self.n = np.zeros((self.N, self.N, self.N))
		solution = np.zeros(self.N)

		scheduler = Scheduler(self.nodes)
		scheduler.execute()

		backwards_substitution()

		_M = self.M
		self.M = None
		self.m = None
		self.n = None

		return solution, _M
