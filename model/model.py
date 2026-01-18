import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.album= []

        self.G= nx.Graph()
        self._nodes = []
        self._edges = []

    def get_album(self, durata):
        return DAO.get_all_album(durata)

    def build_graph(self, durata):
        self.G.clear()

        self._nodes=[]
        self._edges=[]

        #creo i nodi
        self.album= self.get_album(durata)
        for a in self.album:
            self._nodes.append(a)
        self.G.add_nodes_from(self._nodes)

        #creo gli archi
        all_edges= DAO.get_album_connessi()
        for e in all_edges:
            self.G.add_edge(e[0], e[1])

    def get_graph_details(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def get_num_componente_connessa(self): #?
        return nx.number_connected_components(self.G)