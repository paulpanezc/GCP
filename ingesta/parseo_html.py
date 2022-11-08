from bs4 import BeautifulSoup
import requests
from storage import Storage


def parse(url, destino):
    r = requests.get(url)
    web = r.text
    scraping = BeautifulSoup(web, "html.parser")
    tabla_datos = scraping("table")[0]
    tabla_mediciones = scraping("table")[1]
    contenido = "Estación,Departamento,Provincia,Distrito,Latitud,Longitud,Altitud,Tipo,Código,Fecha,TemperaturaMax(°C),TemperaturaMin(°C),HumedadRelativa(%),Precipitacion(mm/día)\n"
    estacion = tabla_datos("tr")[0].text.strip().split(" : ")[1]
    departamento = tabla_datos("tr")[1]("td")[1].text
    provincia = tabla_datos("tr")[1]("td")[3].text
    distrito = tabla_datos("tr")[1]("td")[5].text
    latitud = tabla_datos("tr")[2]("td")[1].text
    longitud = tabla_datos("tr")[2]("td")[3].text
    altitud = tabla_datos("tr")[2]("td")[5].text
    tipo = tabla_datos("tr")[3]("td")[1].text
    codigo = tabla_datos("tr")[3]("td")[3].text
    i = 0
    for fila in tabla_mediciones("tr"):
        if (i > 1):
            fecha = fila("td")[0].text.strip()
            temperatura_max = fila("td")[1].text.strip()
            temperatura_min = fila("td")[2].text.strip()
            humedad = fila("td")[3].text.strip()
            precipitacion = fila("td")[4].text.strip()
            contenido += "{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(estacion, departamento, provincia, distrito, latitud, longitud, altitud, tipo, codigo, fecha, temperatura_max, temperatura_min, humedad, precipitacion)
        i += 1
    with open(destino, 'wb') as f:
        f.write(contenido.encode())


def main():
    cloud = Storage()
    bucket = cloud.crear_bucket(cloud.client.project)
    # url = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/export.php?CBOFiltro=202210&estaciones=116026&t_e=M&estado=REAL&cod_old=&cate_esta=CO&soloAlt=3980"
    url = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/export.php?CBOFiltro=202210&estaciones=115051&t_e=M&estado=REAL&cod_old=&cate_esta=CO&soloAlt=3931"
    archivo = "temperaturas.csv"
    destino = "../recursos/senamhi/{}".format(archivo)
    parse(url, destino)
    # cloud.subir_archivo(bucket, archivo, destino)


if __name__ == "__main__":
    main()
