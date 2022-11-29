import pandas as pd


# df = pd.read_csv("../recursos/senamhi/senamhiEMA.csv")
# df = pd.read_csv("../recursos/senamhi/SenamhiEMA_limpio.txt", sep="|")
# df = pd.read_csv("../recursos/senamhi/SenamhiEMA_limpio_2.txt", sep="|")
df = pd.read_csv("../recursos/senamhi/SenamhiEMA_SinEstandarizar.txt", sep="|")
print(type(df))
print(df.shape)
print(df.head())
print(df.describe())
print(df.describe(include='all'))
print(df.head(4))
print(df.columns)
df_var_cualitativas = ["Estación", "Ubigeo", "Departamento", "Provincia", "Distrito", "Latitud", "Longitud", "Altitud",
                       "Tipo", "Fecha", "Hora"]
df_var_cuantitativas = ["Código", "Temperatura(°C)", "Precipitacion(mm/hora)", "Humedad(%)", "DirecciónDelViento(°)",
                        "VelocidadDelViento(m/s)"]
print(df_var_cualitativas)
print(df_var_cuantitativas)
print(df['Estación'])
print(type(df['Estación']))
print(df[['Estación']])
print(type(df[['Estación']]))
print(df['Estación'].value_counts(normalize=True, dropna=False) * 100)
