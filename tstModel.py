from model.model import Model

myModel = Model()
myModel.buildGraph(2007, 2008)
n, a = myModel.getDetails()
print(f"Nodi: {n}")
print(f"Archi: {a}")