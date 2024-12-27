import numpy as np
from concurrent.futures import ThreadPoolExecutor
from collections import deque

from collections.abc import Collection

from nodes import Node, A


class Scheduler:
	@staticmethod
	def execute(nodes: Collection[Node]):
		in_degree = {node: len(node.parents) for node in nodes}
		ready_nodes = deque([node for node, degree in in_degree.items() if degree == 0])

		processed_count = 0

		with ThreadPoolExecutor() as executor:
			futures = {}

			while processed_count != len(nodes):
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
	def __init__(self, size: int, scheduler=Scheduler):
		self.N = size
		self.scheduler = scheduler
		self.nodes = {}

		self._build_graph()

		self.M = None
		self.m = None
		self.n = None

	def _build_graph(self):
		for r in range(1, self.N):
			a = A(self, r, 0)
			self.nodes[a] = a
			a.find_children()

	def set_scheduler(self, scheduler):
		self.scheduler = scheduler

	def solve(self, matrix: np.array, rhs: np.array) -> tuple[np.ndarray, np.ndarray]:
		# def backwards_substitution():
		# 	for i in range(self.N - 1, -1, -1):
		# 		solution[i] = self.M[i, self.N]
		# 		for j in range(i + 1, self.N):
		# 			solution[i] -= self.M[i, j] * solution[j]
		# 		solution[i] /= self.M[i, i]

		def backwards_substitution():
			for i in range(self.N - 1, -1, -1):
				factor = self.M[i, i]
				self.M[i, :] /= factor
				for j in range(i):
					self.M[j, :] -= self.M[j, i] * self.M[i, :]
			solution = self.M[:, self.N]
			self.M = self.M[:, :-1]
			return solution


		if not self.scheduler:
			raise ValueError("Scheduler not set")
		if matrix.shape != (self.N, self.N):
			raise ValueError(f"This solver is for {self.N}x{self.N} matrices only")

		self.M = np.array([np.append(np.copy(row), rhs[i]) for i, row in enumerate(matrix)])
		self.m = np.zeros((self.N, self.N))
		self.n = np.zeros((self.N, self.N + 1, self.N))

		self.scheduler.execute(self.nodes.values())

		solution = backwards_substitution()

		_M = self.M
		self.M = None
		self.m = None
		self.n = None

		return solution, _M
