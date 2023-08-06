import numpy as np
import networkx as nx

from pge.init.classes.graph import SGraph


class CustomCreator:
    @staticmethod
    def partitioned_grow(types, prt):
        graph = nx.Graph()
        count = 0
        for tp in types:
            nw_graph = tp[0](*tp[1])
            nw_graph.set_attrs("prt", count)
            graph = nx.union(graph, nw_graph.get_nx_graph(), rename=(None, tp[2]))
            count += 1

        graph = SGraph(graph)
        nodes = graph.get_ids(stable=True)
        dg = np.array(
            [
                np.random.choice(
                    max(int(prt * graph.count_out_degree(node)), 1) + 1, 1
                )[0]
                for node in nodes
            ]
        )
        if np.sum(dg) % 2 != 0:
            dg[0] += 1
        prts = graph.get_attributes("prt")
        print(np.unique(prts))
        print(np.sum(dg[prts == 0]), np.sum(dg[prts == 1]), np.sum(dg[prts == 2]))

        for i in np.arange(nodes.size):
            if dg[i] == 0:
                continue

            indx = np.arange(nodes.size)[(prts != prts[i]) & (dg > 0)]
            if indx.size == 0:
                continue
            adds = np.random.choice(indx, dg[i])

            for add in adds:
                if dg[add] > 0:
                    graph.add_edge(nodes[i], nodes[add])
                    dg[add] -= 1
            dg[i] = 0

        print(np.sum(dg) / 2)
        return graph
