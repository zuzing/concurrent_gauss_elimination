from __future__ import annotations


class Node:
	def __init__(self, system: LinearSystem):
		self.system = system
		self.children = []
		self.parents = []

	def add_child(self, child):
		if child in self.system.nodes:
			child = self.system.nodes[child]
		else:
			self.system.nodes[child] = child
			child.find_children()
		self.children.append(child)
		child.parents.append(self)

	def find_children(self):
		pass

	def __call__(self):
		pass

	def __hash__(self):
		pass

	def __eq__(self, other):
		pass

	def __str__(self):
		pass

	def __repr__(self):
		return str(self)


class A(Node):
	def __init__(self, system: LinearSystem, k: int, i: int):
		super().__init__(system)
		self.k = k
		self.i = i

	def find_children(self):
		for j in range(self.i, self.system.N+1):
			self.add_child(B(self.system, self.k, j, self.i))

	def __call__(self):
		self.system.m[self.k, self.i] = self.system.M[self.k, self.i] / self.system.M[self.i, self.i]

	def __hash__(self):
		return hash((self.k, self.i))

	def __eq__(self, other):
		return isinstance(other, A) and self.k == other.k and self.i == other.i

	def __str__(self):
		return f'A({self.k+1}, {self.i+1})'


class B(Node):
	def __init__(self, system: LinearSystem, k: int, j: int, i: int):
		super().__init__(system)
		self.k = k
		self.j = j
		self.i = i

	def find_children(self):
		self.add_child(C(self.system, self.k, self.j, self.i))

	def __call__(self):
		self.system.n[self.k, self.j, self.i] = self.system.M[self.i, self.j] * self.system.m[self.k, self.i]

	def __hash__(self):
		return hash((self.k, self.j, self.i))

	def __eq__(self, other):
		return isinstance(other, B) and self.k == other.k and self.j == other.j and self.i == other.i

	def __str__(self):
		return f'B({self.k+1}, {self.j+1}, {self.i+1})'


class C(Node):
	def __init__(self, system: LinearSystem, k: int, j: int, i: int):
		super().__init__(system)
		self.k = k
		self.j = j
		self.i = i

	def find_children(self):
		if self.k > self.i+1 and self.j > self.i+1:
			self.add_child(C(self.system, self.k, self.j, self.i+1))
		if self.k == self.i+1 and self.j != self.i+1:
			for r in range(self.i+2, self.system.N):
				if self.i < self.j:
					self.add_child(B(self.system, r, self.j, self.i+1))
		if self.j == self.i+1 and self.k > self.i+1:
			self.add_child(A(self.system, self.k, self.i+1))
		if self.k == self.i+1 and self.j == self.i+1:
			for r in range(self.i+2, self.system.N):
				self.add_child(A(self.system, r, self.i+1))

	def __call__(self):
		self.system.M[self.k, self.j] = self.system.M[self.k, self.j] - self.system.n[self.k, self.j, self.i]

	def __hash__(self):
		return hash((self.k, self.j, self.i))

	def __eq__(self, other):
		return isinstance(other, C) and self.k == other.k and self.j == other.j and self.i == other.i

	def __str__(self):
		return f'C({self.k+1}, {self.j+1}, {self.i+1})'
