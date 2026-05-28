import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._drivers = []
        self._idMap = {}

        self._optListPiloti = None
        self._minDistGiorni = None

    def getListaPilotiOttima(self, k):
        self._optListPiloti = []
        self._minDistGiorni = 100*365 # metto distanza di giorni molto grande

        componenti = list(nx.connected_components(self._grafo))

        if len(componenti) < k:
            # allora non ho abbastanza componenti connesse da cui pescare -> non posso trovare soluzione
            return None, 0

        parziale = []
        self._ricorsione(componenti, k, parziale, 0)

        return self._optListPiloti, self._minDistGiorni

    def _ricorsione(self, componenti, k, parziale, indexComponente):
        # condizione di ottimalità
        if len(parziale) == k:
            dateDiNascita = [p.dob for p in parziale]
            diffEtaPiloti = (max(dateDiNascita) - min(dateDiNascita)).days
            if diffEtaPiloti < self._minDistGiorni:
                self._optListPiloti = copy.deepcopy(parziale)
                self._minDistGiorni = diffEtaPiloti

        # condizione di terminazione (quando esco)
        # 1) esco se l'indice che indica quale componente connessa sto considerando a questa iterazione è diventato maggiore o
        # uguale al numero di componenti connesse totali, perchè vuol dire che non ho altre componenti connesse da cui pescare
        # 2) l'altro motivo è se non ho abbastanza componenti rimanenti per arrivare a k piloti in parziale
        if indexComponente >= len(componenti) or (len(componenti) - indexComponente) < (k - len(parziale)):
            return

        # se non sono uscito, allora posso aggiungere ancora piloti. Per questa componente, di indice indexComponente,
        # provo a ingaggiare un pilota oppure a non ingaggiare nessuno.

        # caso 1, inserisco un pilota appartenente a questa comp connessa. In questo branch provo tutti i piloti che
        # fanno parte della componente connessa in esame.
        componente = componenti[indexComponente]
        for pilota in componente:
            parziale.append(pilota)
            self._ricorsione(componenti, k, parziale, indexComponente + 1)
            parziale.pop()

        # caso 2, mi tengo un branch di esplorazione in cui io non ho preso proprio nessuno da questa componente.
            self._ricorsione(componenti, k, parziale, indexComponente + 1)

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
