import numpy as np
import networkx as nx

from dtg.tail.estimate.moment import MomentEstimator
from dtg.tail.mse import boot_estimate
from pge.model.growth.basic import BasicGrowth
from pge.model.growth.basic_fix import FixGrowth
from pge.model.growth.basic_lead import LeadFixGrowth


class PAGrowth(BasicGrowth):
    def choice(self, graph, sz):
        probs = np.array([graph.count_in_degree(node) for node in graph.get_ids()]) + self.param
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(), sz, replace=False, p=probs)


class PAFixGrowth(FixGrowth):
    def choice(self, graph, sz):
        probs = graph.get_attributes("dg") + self.param
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(stable=True), sz, replace=False, p=probs)

    def clean(self, graph):
        if self.param != 0:
            return []

        graph = self.prep(graph)
        sub = sorted(
            nx.connected_components(graph.get_nx_graph()), key=len, reverse=True
        )

        dels = []
        for sub_ in sub:
            if len(sub_) == 1:
                dels = np.append(dels, list(sub_))
        return dels

    def prep(self, graph):
        graph.set_attrs(
            "dg", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        return graph


class PALeadFixGrowth(LeadFixGrowth):
    def __init__(self, graph, deg, typ, arg):
        super().__init__(graph, deg, typ)
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
        probs = graph.get_attributes("dg", nodes)
        probs = probs / np.sum(probs)

        return np.random.choice(nodes, sz, replace=False, p=probs)

    def clean(self, graph):
        graph = self.prep(graph)

        sub = sorted(
            nx.connected_components(graph.get_nx_graph()), key=len, reverse=True
        )
        for sub_ in sub:
            if len(sub_) == 1:
                if np.sum(graph.get_attributes("dg", sub_) > 0) == 0:
                    graph.del_node(list(sub_)[0])
        return graph
