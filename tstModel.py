from model.model import Model

mymodel = Model()

mymodel.buildGrafo()

lista = mymodel.filtraGrafo(3)


mymodel.getBestPath(3)
print(f"{mymodel._bestScore}")
