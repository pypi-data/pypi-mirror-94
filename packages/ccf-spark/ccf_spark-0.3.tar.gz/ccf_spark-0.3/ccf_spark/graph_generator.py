import networkx as nx


class GraphGenerator:
    def __init__(self, nodes: int, edges: int):
        self.graph = self._generate_random_graph(nodes, edges)

    def generate_new_random_graph(self, nodes: int, edges: int) -> None:
        self.graph = self._generate_random_graph(nodes, edges)

    def _generate_random_graph(self, nodes: int, edges: int) -> nx.Graph:
        return nx.gnm_random_graph(nodes, edges)

    def remove_null_degres_nodes(self) -> None:
        copy = self.graph.copy()
        self.graph = nx.subgraph_view(
            copy,
            filter_node=lambda node: bool(nx.degree(copy, node)),
        )

    def save(self, path: str) -> None:
        with open(path, 'wb') as f:
            nx.write_edgelist(self.graph, f)

    def draw(self):
        nx.draw(self.graph, with_labels=True)

    @staticmethod
    def generate_ccf_random_graph(nodes: int, edges: int):
        graph = GraphGenerator(nodes, edges)
        graph.remove_null_degres_nodes()
        return graph

    @property
    def number_connected_components(self) -> int:
        return nx.number_connected_components(self.graph)

    @property
    def edges(self) -> list:
        return self.graph.edges

    @property
    def nodes(self) -> list:
        return self.graph.nodes
