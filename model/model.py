import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._drivers = []
        self._idMap = {}

    def getListaPilotiOttima(self, k):
        pass
        # 1:09:10

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, annoI, annoF):
        self._grafo.clear()
        self._drivers = DAO.getAllNodes(annoI, annoF)
        self._grafo.add_nodes_from(self._drivers)

        for nodo in self._drivers:
            self._idMap[nodo.driverId] = nodo

        edges = DAO.getAllArchi(annoI, annoF, self._idMap)
        for e in edges:
            self._grafo.add_edge(e.d1, e.d2, weight = e.peso)

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getListaOutput(self):
        lista = sorted(self._grafo.edges(data=True), key = lambda x: x[2]["weight"], reverse = True)
        return lista[:3]

    def getConnessa(self):
        componenti = list(nx.connected_components(self._grafo))
        maggiore = max(componenti, key = len)
        subgraph = self._grafo.subgraph(maggiore).copy() # creo copia di un sotto grafo
        nodiOrdinati = sorted(subgraph.nodes(), key = lambda x: self._grafo.degree(x), reverse = True)
        dettagli = [(n, self._grafo.degree(n)) for n in nodiOrdinati]
        return len(componenti), maggiore, dettagli
