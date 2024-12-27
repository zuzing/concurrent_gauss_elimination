import numpy as np
from gauss_elimination import LinearSystem
from graph_visualizer import draw_graph


def load_file(filename: str) -> tuple[int, list, list]:
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


def save_file(filename: str, n: int, x: np.ndarray, M: np.ndarray):
	with open(filename, 'w') as file:
		file.write(f"{n}\n")
		for row in M:
			file.write(" ".join(f"{elem:.2f}" for elem in row) + "\n")
		file.write(" ".join(f"{elem}" for elem in x) + "\n")



if __name__ == '__main__':
	n, matrix, rhs = load_file('../data/in15.txt')

	solver = LinearSystem(n)

	x, M = solver.solve(np.array(matrix), np.array(rhs))

	save_file('../data/out15.txt', n, x, M)


	solver = LinearSystem(3)
	draw_graph(solver.nodes.values())

	solver = LinearSystem(4)
	draw_graph(solver.nodes.values())




