import unittest
import numpy as np

from gauss_elimination import LinearSystem, Scheduler


class TestLinearSystem(unittest.TestCase):
	@staticmethod
	def generate_solvable_linear_system(size: int):
		while True:
			A = np.random.random((size, size))
			if np.linalg.det(A) != 0:
				break

		x = np.random.random(size)

		rhs = np.dot(A, x)

		return A, rhs

	class SynchronousScheduler:
		@staticmethod
		def execute(nodes):
			in_degree = {node: len(node.parents) for node in nodes}
			ready_nodes = [node for node, degree in in_degree.items() if degree == 0]

			while ready_nodes:
				node = ready_nodes.pop(0)
				node()
				for child in node.children:
					in_degree[child] -= 1
					if in_degree[child] == 0:
						ready_nodes.append(child)


	def test_nodes_execution(self):
		for N in range(2, 25):
			system = LinearSystem(N, scheduler=self.SynchronousScheduler)
			A, rhs = self.generate_solvable_linear_system(N)

			solution, matrix = system.solve(A, rhs)

			np.testing.assert_allclose(matrix, np.triu(matrix), atol=1e-10)  # matrix is upper triangular
			np.testing.assert_allclose(np.dot(A, solution), rhs)

	def test_concurrent_execution(self):
		for N in range(2, 25):
			system = LinearSystem(N, scheduler=Scheduler)
			A, rhs = self.generate_solvable_linear_system(N)

			solution, matrix = system.solve(A, rhs)

			np.testing.assert_allclose(np.dot(A, solution), rhs)

	def test_linear_system_reusability(self):
		system = LinearSystem(3, scheduler=Scheduler)

		for _ in range(10):
			A, rhs = self.generate_solvable_linear_system(3)
			solution, matrix = system.solve(A, rhs)
			np.testing.assert_allclose(np.dot(A, solution), rhs)


if __name__ == "__main__":
	unittest.main()
