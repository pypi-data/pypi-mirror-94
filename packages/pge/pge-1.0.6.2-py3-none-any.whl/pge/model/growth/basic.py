import numpy as np
import networkx as nx


class BasicGrowth:
    def __init__(self, graph, schema, deg, model_param):
        self.gr = graph
        self.deg = deg
        self.schema = schema
        self.param = model_param

    def choice(self, gr, sz):
        return []

    def proceed(self, n, save, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, 0)

        for edge in nw_graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr, 0)

        count = self.gr.size()
        for _ in np.arange(n):
            new_node = np.random.choice([True, False], p=self.schema)
            if new_node:
                if self.deg[0] == "const":
                    nodes = self.choice(nw_graph, self.deg[1])
                else:
                    nodes = self.choice(nw_graph, self.deg[0](self.deg[1]))
                for node in nodes:
                    nw_graph.add_edge(str(count), node)
                    nw_graph.set_edge_data(str(count), node, attr, _+1)

                nw_graph.set_attr(str(count), attr, _+1)
                count += 1
            else:
                nodes = self.choice(nw_graph, 2)
                nw_graph.add_edge(nodes[0], nodes[1])
                nw_graph.set_edge_data(nodes[0], nodes[1], attr, _+1)
        nx.write_graphml(nw_graph.get_nx_graph(), save + ".graphml")
