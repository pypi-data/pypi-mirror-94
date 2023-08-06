import networkx as nx
import numpy as np

from pge.model.growth.basic_fix import FixGrowth
from pge.ranks.rank import estimate_rank


class LeadFixGrowth(FixGrowth):
    def prep(self, graph):
        rs = nx.clustering(graph.get_nx_graph())
        graph.set_attrs("clust", {k: 0 if v is np.NaN else v for k, v in rs.items()})
        rs = nx.closeness_centrality(graph.get_nx_graph())
        graph.set_attrs("cls", {k: 0 if v is np.NaN else v for k, v in rs.items()})
        graph.set_attrs(
            "dg", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )

        estimate_rank(graph, "one", pers=None)
        comp = nx.algorithms.community.greedy_modularity_communities(
            graph.get_nx_graph()
        )
        ind = 0
        for c in comp:
            ind += 1
            for node in c:
                graph.set_attr(node, "greedy", ind)
        return graph
