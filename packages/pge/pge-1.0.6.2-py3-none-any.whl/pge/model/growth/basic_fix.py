import numpy as np
import networkx as nx


from pge.model.growth.basic import BasicGrowth


class FixGrowth(BasicGrowth):
    def __init__(self, graph, schema, deg, model_param, del_typ):
        super().__init__(graph, schema, deg, model_param)
        self.typ = del_typ

    def proceed(self, n, save, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, 0)
            nw_graph.set_attr(node, attr + "_end", -1)

        for edge in nw_graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr, 0)
            nw_graph.set_edge_data(edge[0], edge[1], attr + "_end", -1)
        graph = self.prep(self.gr.clean_copy())

        count = self.gr.size()
        for _ in np.arange(n):
            new_node = np.random.choice([True, False], p=self.schema)
            if new_node:
                if self.deg[0] == "const":
                    nodes = self.choice(graph, self.deg[1])
                else:
                    nodes = self.choice(graph, self.deg[0](self.deg[1]))

                if nodes is None:
                    continue

                for node in nodes:
                    nw_graph.add_edge(str(count), node)
                    nw_graph.set_edge_data(str(count), node, attr, _ + 1)
                    graph.add_edge(str(count), node)
                nw_graph.set_attr(str(count), attr, _ + 1)
                count += 1

                if graph.size() > self.gr.size():
                    if self.typ == "un":
                        del_node = np.random.choice(graph.get_ids(stable=True))
                    else:
                        ids = graph.get_ids(stable=True)
                        vals = graph.get_attributes(attr)
                        del_node = np.random.choice(ids[vals == np.min(vals)])
                    nw_graph.set_attr(del_node, attr + "_end", _ + 1)
                    for deg_node in nw_graph.get_in_degrees(del_node):
                        nw_graph.set_edge_data(deg_node, del_node, attr + "_end", _ + 1)
                    graph.del_node(del_node)

                    graph = self.prep(graph)
                    for node in self.clean(graph):
                        nw_graph.set_attr(node, attr + "_end", _ + 1)
                        for deg_node in nw_graph.get_in_degrees(node):
                            nw_graph.set_edge_data(deg_node, node, attr + "_end", _ + 1)
                        graph.del_node(node)
            else:
                nodes = self.choice(graph, 2)
                nw_graph.add_edge(nodes[0], nodes[1])
                nw_graph.set_edge_data(nodes[0], nodes[1], attr, _ + 1)
                graph.add_edge(nodes[0], nodes[1])

        for node in graph.get_ids():
            nw_graph.set_attr(node, attr + "_end", _ + 1)
        for edge in graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr + "_end", _ + 1)
        nx.write_graphml(nw_graph.get_nx_graph(), save + ".graphml")

    def prep(self, graph):
        return graph

    def clean(self, graph):
        return graph
