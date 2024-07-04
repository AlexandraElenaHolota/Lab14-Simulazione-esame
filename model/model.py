import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._bestPathNode = []
        self._bestPathEdge = []
        self._bestScore = 0

    def getBestPath(self, soglia):
        self._bestPathNode = []
        self._bestPathEdge = []
        self._bestScore = 0

        for node in self.nodes:
            parziale = [node]
            visited = set(parziale)
            self.ricorsione(parziale, [], soglia, visited)

    def ricorsione(self, parziale, p_edges, soglia, visited):
        ultimo = parziale[-1]
        vicini = self.vicinoOk(ultimo, soglia)

        if not vicini:
            peso = self.getPeso(p_edges)
            if peso > self._bestScore:
                self._bestScore = peso
                self._bestPathNode = parziale[:]
                self._bestPathEdge = p_edges[:]
            return

        for v in vicini:
            if v not in visited:
                p_edges.append((ultimo, v, self._grafo[ultimo][v]['weight']))
                parziale.append(v)
                visited.add(v)

                self.ricorsione(parziale, p_edges, soglia, visited)

                visited.remove(v)
                parziale.pop()
                p_edges.pop()

    def getPeso(self, p_edges):
        peso = sum(p[2] for p in p_edges)
        return peso

    def vicinoOk(self, ultimo, soglia):
        vicini = self._grafo.edges(ultimo, data=True)
        result = [v for u, v, data in vicini if data["weight"] > soglia]
        return result



    def buildGrafo(self):
        self._grafo.clear()

        #aggiungi nodi
        self.nodes = DAO.getAllCromosomi()
        self._grafo.add_nodes_from(self.nodes)

        #aggiungi archi pesati

        self.edges = DAO.getAllWeightEdges()
        for e in self.edges:
            self._grafo.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def max_min(self):
        return DAO.getMaxMin()

    def filtraGrafo(self, soglia):
        archiMin = 0
        archiMax = 0
        for edges in self._grafo.edges(data=True):
            if edges[2]["weight"] < soglia:
                archiMin += 1
            if edges[2]["weight"] > soglia:
                archiMax += 1
        return archiMin, archiMax




