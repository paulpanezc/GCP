import pandas as pd


df = pd.read_csv("../recursos/minsa/minsa.csv")
print(type(df))
print(df.shape)
print(df.head())
print(df.describe())
print(df.describe(include='all'))
print(df.head(4))
print(df.columns)
df_var_cualitativas = ["Departamento", "Provincia", "Distrito", "FechaInicio", "FechaFin"]
df_var_cuantitativas = ["Ubigeo", "SemanasEpidemologicasAnteriores", "SemanaEpidemiologicaActual", "TotalGeneral",
                        "Mortalidad", "PoblacionEnRiesgo"]
print(df_var_cualitativas)
print(df_var_cuantitativas)
print(df['Departamento'])
print(type(df['Departamento']))
print(df[['Departamento']])
print(type(df[['Departamento']]))
print(df['Departamento'].value_counts(normalize = True, dropna = False)*100)
