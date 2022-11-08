import pandas as pd


# df = pd.read_csv("../recursos/minsa/defunciones.csv")
df = pd.read_csv("../recursos/senamhi/temperaturas.csv")
print(type(df))
print(df.shape)
print(df.head())
print(df.describe())
print(df.describe(include='all'))
print(df.head(4))
print(df.columns)
# df_var_cualitativas = ["Departamento", "Provincia", "Distrito"]
# df_var_cuantitativas = ["SemanaEpidemiologica01-40", "SemanaEpidemiologica41", "TotalGeneral", "Mortalidad", "PoblacionEnRiesgo"]
# print(df_var_cualitativas)
# print(df_var_cuantitativas)
# print(df['Departamento'])
# print(type(df['Departamento']))
# print(df[['Departamento']])
# print(type(df[['Departamento']]))
# print(df['Departamento'].value_counts(normalize = True, dropna = False)*100)
df_var_cualitativas = ["Estación", "Departamento", "Provincia", "Distrito", "Latitud", "Longitud", "Altitud", "Tipo", "Fecha"]
df_var_cuantitativas = ["Código", "TemperaturaMax(°C)", "TemperaturaMin(°C)", "HumedadRelativa(%)", "Precipitacion(mm/día)"]
print(df_var_cualitativas)
print(df_var_cuantitativas)
print(df['Estación'])
print(type(df['Estación']))
print(df[['Estación']])
print(type(df[['Estación']]))
print(df['Estación'].value_counts(normalize = True, dropna = False)*100)
