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
        k = self._view._txtInK.value # qui dovremmo fare i soliti controlli sulla validità di k prima di procedere
        kInt = int(k)

        listPilotiOttima, minDistEta = self._model.getListaPilotiOttima(kInt)

        if listPilotiOttima is None: # non possiamo trovare soluzioni
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non ci sono abbastanza componenti connesse per trovare {k} "
                                                          f"piloti che non siano stati compagni di squadra nel range selezionato."))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Lista di piloti con scarto di età minimo che non sono stati mai compagni di squadra nel range selezionato.", color="red"))

        for p in listPilotiOttima:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.txt_result.controls.append(
            ft.Text(f"Differenza di età fra pilota più giovane e quello più anziano: {minDistEta} giorni", color = "red"))

        youngest = min(listPilotiOttima, key=lambda x: x.dob)
        oldest = max(listPilotiOttima, key=lambda x: x.dob)

        self._view.txt_result.controls.append(ft.Text(f"Pilota più anziano: {oldest}"))
        self._view.txt_result.controls.append(ft.Text(f"Pilota più giovane: {youngest}"))

        self._view.update_page()

    def fillDDYear(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(year))
            self._view._ddAnno2.options.append(ft.dropdown.Option(year))
        self._view.update_page()