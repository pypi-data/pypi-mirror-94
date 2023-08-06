import networkx as nx
import numpy as np

from dtg.tail.estimate.moment import MomentEstimator
from dtg.tail.mse import boot_estimate
from pge.model.growth.basic import BasicGrowth
from pge.model.growth.basic_fix import FixGrowth
from pge.model.growth.basic_lead import LeadFixGrowth


class CAGrowth(BasicGrowth):
    def choice(self, graph, sz):
        cs = {
            k: v ** self.param[0] + self.param[1]
            for k, v in nx.clustering(graph.get_nx_graph()).items()
            if v is not np.NaN
        }
        probs = list(cs.values())
        probs = probs / np.sum(probs)
        return np.random.choice(list(cs.keys()), sz, replace=False, p=probs)


class CAFixGrowth(FixGrowth):
    def prep(self, graph):
        rs = nx.clustering(graph.get_nx_graph())
        graph.set_attrs("clust", {k: 0 if v is np.NaN else v for k, v in rs.items()})
        return graph

    def choice(self, graph, sz):
        nodes = graph.get_ids(stable=True)
        probs = graph.get_attributes("clust") ** self.param[0] + self.param[1]

        nodes, probs = nodes[probs > 0], probs[probs > 0]
        if probs.size == 0:
            return None
        probs = probs / np.sum(probs)
        return np.random.choice(nodes, sz, replace=False, p=probs)

    def clean(self, graph):
        graph = self.prep(graph)

        sub = sorted(
            nx.connected_components(graph.get_nx_graph()), key=len, reverse=True
        )
        dls = []
        for sub_ in sub:
            if (
                np.sum(graph.get_attributes("clust", sub_) ** self.param[0] + self.param[1] > 0)
                == 0
            ):
                dls = np.append(dls, list(sub_))
        return dls


class CALeadFixGrowth(LeadFixGrowth):
    def __init__(self, graph, deg, typ, alpha, eps, arg):
        super().__init__(graph, deg, typ)
        self.alpha = alpha
        self.eps = eps
        self.arg = arg

    def choice(self, graph, sz):
        cms_nodes = graph.get_attributes("greedy")
        uns = np.unique(cms_nodes)
        nodes = graph.get_ids(stable=True)

        alp = []
        for un in uns:
            rs = boot_estimate(
                MomentEstimator,
                graph.get_attributes(self.arg, nodes[cms_nodes == un]),
                1 / 2,
                2 / 3,
                100,
                speed=False,
            )[0]
            if np.isnan(rs):
                alp.append(np.NaN)
                continue

            alp.append(1 / rs)

        nodes_ = []
        alp = np.array(alp)
        if np.sum(np.isnan(alp)) > 0:
            if np.sum(~np.isnan(alp)) > 0:
                alp[np.isnan(alp)] = np.max(alp[~np.isnan(alp)]) + 0.01
            else:
                alp[np.isnan(alp)] = 0.01
        mn = np.min(alp)

        for i in np.arange(len(alp)):
            if alp[i] == mn:
                nodes_ = np.append(nodes_, nodes[cms_nodes == uns[i]])

        nodes = nodes_
        cs = graph.get_attributes("clust", nodes)

        probs = np.power(cs, self.alpha) + self.eps
        probs = probs / np.sum(probs)
        if np.sum(probs > 0) >= sz:
            nodes, probs = nodes[probs > 0], probs[probs > 0]
            return np.random.choice(nodes, sz, replace=False, p=probs)
        else:
            print("renew")
            nodes = np.random.choice(nodes, sz, replace=False)
            for i in np.arange(sz - 1):
                if ~graph.get_nx_graph().has_edge(nodes[i], nodes[i + 1]):
                    graph.add_edge(nodes[i], nodes[i + 1])

            return nodes

    def clean(self, graph):
        graph = self.prep(graph)

        sub = sorted(
            nx.connected_components(graph.get_nx_graph()), key=len, reverse=True
        )
        for sub_ in sub:
            if (
                np.sum(
                    np.power(graph.get_attributes("clust", sub_), self.alpha) + self.eps
                    > 0
                )
                == 0
            ):
                for node in sub_:
                    graph.del_node(node)
        return graph
