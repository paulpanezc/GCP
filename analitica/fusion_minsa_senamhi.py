import pandas as pd


defunciones = pd.read_csv("../recursos/minsa/minsa.csv")
climatologica = pd.read_csv("../recursos/senamhi/SenamhiCO_limpio_2.txt", sep="|")
print(defunciones.columns)
print(climatologica.columns)
mortalidad_clima = pd.merge(left=defunciones, right=climatologica, left_on="Ubigeo", right_on="Ubigeo")
print(mortalidad_clima.shape)
print(mortalidad_clima)
