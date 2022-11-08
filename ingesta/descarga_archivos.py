import requests
from storage import Storage


def main():
    cloud = Storage()
    bucket = cloud.crear_bucket(cloud.client.project)
    url = "https://www.dge.gob.pe/portal/docs/vigilancia/cdistritos/2022/41/IRA%20-%20DEFUNCIONES.pdf"
    r = requests.get(url)
    nombre_archivo = "defunciones.pdf"
    archivo_destino = "../recursos/minsa/{}".format(nombre_archivo)
    with open(archivo_destino, 'wb') as f:
        f.write(r.content)
    cloud.subir_archivo(bucket, nombre_archivo, archivo_destino)


if __name__ == "__main__":
    main()
