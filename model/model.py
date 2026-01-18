import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.albums= []
        self.id_map = {}
        self.album_playlist_map= {}

        self.G= nx.Graph()

        self.soluzione_best= []


    def load_albums(self, durata):
        self.albums= DAO.get_all_album(durata)
        self.id_map= {a.id: a for a in self.albums} #dizionario con chiave: id album e valore: oggetto Album

    def load_album_playlists(self):
        self.album_playlist_map= DAO.get_album_playlist_map(self.albums) #mappa album -> playlist

    def build_graph(self):
        self.G.clear()

        self.G.add_nodes_from(self.albums)

        #creo gli archi
        for i, a1 in enumerate(self.albums): #prende l'album a1 in posizione i
            for a2 in self.albums[i+1:]: #prende gli album dopo a1
                if self.album_playlist_map[a1] & self.album_playlist_map[a2]:
                    '''
                    album_playlist_map[a1] → set di playlist dell’album a1
                    album_playlist_map[a2] → set di playlist dell’album a2
                    & = intersezione tra insiemi
                    QUINDI entra nell’if solo se i due album condividono almeno una playlist
                    '''
                    self.G.add_edge(a1, a2)

    def get_componenti(self, album):
        "restituisce la componente connessa di un album passato come parametro (trova tutti gli album collegati a album)"
        if album not in self.G: #verifico che l'album sia un nodo del grafo
            return []
        return list(nx.node_connected_component(self.G, album))
        '''
        nx.node_connected_component(self.G, album) restituisce un set, contiene tutti i nodi raggiungibili da album,
        include anche album stesso
        poi converto questo set in una lista
        '''


    def compute_best_set(self, start_album, max_durata):
        '''ricerca ricorsiva del set massimo di album nella componente connessa'''
        component= self.get_componenti(start_album)
        self.soluzione_best= []
        self._ricorsioe(component, [start_album], start_album.durata, max_durata)
        return self.soluzione_best

    def _ricorsioe(self, albums, current_set, current_durata, max_durata):

        #condizione di terminazione
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set[:]

        #ciclo di ricorsione
        for album in albums:
            if album in current_set:
                continue
            new_durata= current_durata + album.durata
            if new_durata <= max_durata:
                current_set.append(album)
                self._ricorsioe(albums, current_set, new_durata, max_durata)
                current_set.pop()