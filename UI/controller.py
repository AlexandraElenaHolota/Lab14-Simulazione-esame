import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.max_min = None
        self.soglia = None

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()

        self._grafo = self._model.buildGrafo()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(
            f"Il grafo è costituito di {n} nodi e {a} archi."))

        self.max_min = self._model.max_min()
        self._view.txt_result.controls.append(ft.Text(
            f"Informazioni sui pesi degli archi - valore minimo: {self.max_min[0][0]} e valore massimo: {self.max_min[0][1]}."))


        self._view.update_page()

    def handle_countedges(self, e):
        if self._view.txt_name.value != "":
            try:
                self.soglia = int(self._view.txt_name.value)
            except ValueError:
                self._view.txt_result2.controls.append(ft.Text("Inseririe un numero"))
                self._view.update_page()
                return
        else:
            self._view.txt_result2.controls.append(ft.Text("Inseririe un numero soglia"))
            self._view.update_page()
            return
        if self.soglia > self.max_min[0][0] and self.soglia < self.max_min[0][1]:
            min, max = self._model.filtraGrafo(self.soglia)
            self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {max}"))
            self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {min}"))
        else:
            self._view.txt_result2.controls.append(ft.Text(f"Inserire un valore compreso tra {self.max_min[0][0]} e {self.max_min[0][1]}"))
        self._view.update_page()


    def handle_search(self, e):
        self._model.getBestPath(self.soglia)

        self._view.txt_result3.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model._bestScore)}"))

        for ii in self._model._bestPathEdge:
            self._view.txt_result3.controls.append(ft.Text(
                f"{ii[0]} --> {ii[1]}: weight {ii[2]}"))  # ii[2]

        self._view.update_page()