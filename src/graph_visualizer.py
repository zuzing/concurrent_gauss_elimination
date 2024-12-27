import matplotlib.pyplot as plt
import networkx as nx

from nodes import A, B, C


def draw_graph(nodes):
	G = nx.DiGraph()
	node_colors = {}
	color_mapping = {
		A: "red",
		B: "green",
		C: "blue"
	}

	for node in nodes:
		G.add_node(str(node))
		for child in node.children:
			G.add_edge(str(node), str(child))

		node_colors[str(node)] = color_mapping.get(type(node), "black")


	pos = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot")
	for node, (x, y) in pos.items():
		pos[node] = (x, y * 10)  # increase vertical spacing


	nx.draw(
		G, pos, with_labels=True, node_size=3000, node_color="white",
		edgecolors=[node_colors[node] for node in G.nodes()], font_size=10, font_weight="bold", linewidths=2
	)

	plt.show()