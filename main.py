import numpy as np
from typing import Tuple
from gauss_elimination import LinearSystem


def load_file(filename: str) -> Tuple[int, list, list]:
	"""
	File format:
		matrix size
		matrix
		constant terms
	"""
	with open(filename, 'r') as file:
		n = int(file.readline())
		matrix = []
		for _ in range(n):
			line = file.readline()
			matrix.append(list(map(float, line.split())))
		rhs = list(map(float, file.readline().split()))

	return n, matrix, rhs


if __name__ == '__main__':
	# n, matrix = load_file('matrix.txt')


	def generate_nonsingular_matrix(size):
		while True:
			matrix = np.random.rand(size, size)
			if np.linalg.det(matrix) != 0:
				return matrix


	n = 3
	mat = generate_nonsingular_matrix(n)
	terms = [1, 2, 3]

	ls = LinearSystem(n)
	solution, _ = ls.solve(mat, terms)

	np_solution = np.linalg.solve(mat, terms)
	print(solution)
	print(np_solution)
