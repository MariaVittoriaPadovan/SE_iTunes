import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        durata_sec= int(self._view.txt_durata.value) * 60

        self._model.build_graph(durata_sec)

        n_nodes, n_edges = self._model.get_graph_details()

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo creato: {n_nodes} album, {n_edges} archi")
        )

        self.populate_dd_album(durata_sec)
        self._view.update()

    def populate_dd_album(self, durata):
        album = self._model.get_album(durata)

        # popolo dropdown di album
        for a in album:
            self._view.dd_album.options.append(ft.dropdown.Option(key=a.id, data=a))

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO
        # e.control è il DropDown
        selected_key = e.control.value  # salvo la chiave dell'opzione scelta

        for option in e.control.options:  # ciclo su tutte le opzioni del DropDown
            if option.key == selected_key:  # quando trovo la chiave dell'opzione selezionata
                self._view.dd_album_value = option.data  # salvo il valore reale associato all'opzione del dd
                break

    def handle_analisi_comp(self, e): #?
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        album_scelto= self._view.dd_album.value
        self._model.get_num_componente_connessa()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO