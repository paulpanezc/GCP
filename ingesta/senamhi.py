import csv
import sys
from bs4 import BeautifulSoup
import requests
from storage import Storage


estaciones = {
    "CO": {
        "estado": "REAL",
        "cabecera": "Estación,Departamento,Provincia,Distrito,Latitud,Longitud,Altitud,Tipo,Código,Fecha,"
                    "TemperaturaMax(°C),TemperaturaMin(°C),HumedadRelativa(%),Precipitacion(mm/día)\n"
    },
    "EMA": {
        "estado": "AUTOMATICA",
        "cabecera": "Estación,Departamento,Provincia,Distrito,Latitud,Longitud,Altitud,Tipo,Código,Fecha,Hora,"
                    "Temperatura(°C),Precipitación(mm/hora),Humedad(%),DirecciónDelViento(°),VelocidadDelViento(m/s)\n"
    }
}


def parseo(tipo_estacion, codigo_estacion, periodo, altitud):
    url = "https://www.senamhi.gob.pe/mapas/mapa-estaciones-2/export.php?CBOFiltro={}&estaciones={}&t_e=M&estado={}&" \
          "cod_old=&cate_esta={}&soloAlt={}".format(periodo, codigo_estacion, estaciones[tipo_estacion]["estado"],
                                                    tipo_estacion, altitud)
    print(url)
    contenido = ""
    try:
        r = requests.get(url)
        web = r.text
        scraping = BeautifulSoup(web, "html.parser")
        tabla_datos = scraping("table")[0]
        tabla_mediciones = scraping("table")[1]
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
            if tipo_estacion == "CO":
                if i > 1:
                    fecha = fila("td")[0].text.strip()
                    temperatura_max = fila("td")[1].text.strip()
                    temperatura_min = fila("td")[2].text.strip()
                    humedad = fila("td")[3].text.strip()
                    precipitacion = fila("td")[4].text.strip()
                    contenido += "{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(estacion, departamento, provincia,
                                                                                      distrito, latitud, longitud, altitud,
                                                                                      tipo, codigo, fecha, temperatura_max,
                                                                                      temperatura_min, humedad,
                                                                                      precipitacion)
            elif tipo_estacion == "EMA":
                if i > 0:
                    fecha = fila("td")[0].text.strip()
                    hora = fila("td")[1].text.strip()
                    temperatura = fila("td")[2].text.strip()
                    precipitacion = fila("td")[3].text.strip()
                    humedad = fila("td")[4].text.strip()
                    direccion_viento = fila("td")[5].text.strip()
                    velocidad_viento = fila("td")[6].text.strip()
                    contenido += "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(estacion, departamento,
                                                                                            provincia, distrito, latitud,
                                                                                            longitud, altitud, tipo, codigo,
                                                                                            fecha, hora, temperatura,
                                                                                            precipitacion, humedad,
                                                                                            direccion_viento,
                                                                                            velocidad_viento)
            i += 1
    except requests.exceptions.ConnectionError:
        print("No se pudo obtener la data climatológica de la estación {} para el periodo {}.".format(codigo_estacion,
                                                                                                      periodo))
    return contenido


def main():
    tipo_estacion = sys.argv[1]
    if tipo_estacion in ["CO", "EMA"]:
        anio = sys.argv[2]
        mes_final = int(sys.argv[3])
        cloud = Storage()
        bucket = cloud.crear_bucket(cloud.client.project)
        archivo = "senamhi{}.csv".format(tipo_estacion)
        # Descomentar para usar en modo local
        # destino = "../recursos/senamhi/{}/{}".format(anio, archivo)
        # Uso en Dataproc / PySpark
        destino = "{}".format(archivo)
        contenido = estaciones[tipo_estacion]["cabecera"]
        # Descomentar para usar en modo local
        # with open("../recursos/senamhi/estaciones{}.csv".format(tipo_estacion)) as archivo_csv:
        # Uso en Dataproc / PySpark
        archivo_estaciones = "estaciones{}.csv".format(tipo_estacion)
        cloud.descargar_archivo(bucket, archivo_estaciones, archivo_estaciones)
        with open(archivo_estaciones) as archivo_csv:
            contenido_csv = csv.reader(archivo_csv, delimiter=',')
            for fila in contenido_csv:
                for mes in range(1, mes_final + 1):
                    periodo = "{}{}".format(anio, str(mes).zfill(2))
                    contenido += parseo(tipo_estacion, fila[0], periodo, fila[1])
        f = open(destino, 'wb')
        f.write(contenido.encode())
        f.close()
        cloud.subir_archivo(bucket, archivo, destino)
    else:
        print("Tipo de estación no admitido.")


if __name__ == "__main__":
    main()
