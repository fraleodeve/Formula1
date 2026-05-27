import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
        nodi, archi = self._model.getDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!\nIl grafo contiene {nodi} nodi"
                                                      f" e {archi} archi.", color = "red"))
        self._view.update_page()

    def handleDettagli(self, e):
        lista = self._model.getListaOutput()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:", color = "red"))
        for arco in lista:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} -> {arco[1]} (peso: {arco[2]["weight"]})"))

        lunghezza, maggiore, dettagli = self._model.getConnessa()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {lunghezza} componenti connesse.", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa maggiore ha dimensione pari a {len(maggiore)}.", color = "red"))
        for l in maggiore:
            self._view.txt_result.controls.append(ft.Text(l))

        self._view.txt_result.controls.append(ft.Text(f"Componente connessa in ordine decrescente di grado dei nodi.", color = "red"))
        for d in dettagli:
            self._view.txt_result.controls.append(ft.Text(f"{d[0]} - grado: {d[1]}"))

        self._view.update_page()

    def handleCerca(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(year))
            self._view._ddAnno2.options.append(ft.dropdown.Option(year))
        self._view.update_page()
