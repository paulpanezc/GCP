import os
import sys
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import requests
from storage import Storage


filas_no_permitidas = ["RIESGOCasos,Notificados,de,DEFUNCIONES,notificadas,por,neumonías,(Intra,y,Extra,Hospitalarias)"
                       ",,en,menores,de,5,años", "DEPARTAMENTO,PROVINCIAS,DISTRITOSSEM.,EPIDEMIOLOGICAS,TOTAL,",
                       "GENERALMORTALIDAD", "SEMANA,EPIDEMILOGICA", "DEPARTAMENTO,PROVINCIAS,DISTRITOSTOTAL,",
                       "Elaborado:,Area,de,Gestión,de,Desarrollo,de,Sistemas,de,la,Información,-,CDC",
                       "IMPORTADO,IMPORTADO,IMPORTADO,0,0,0,0,99999999",
                       "1POBLACION,EN,", "1", "DISTRITOS,-,AÑO,,2022,SE.,1",
                       "01,-,1,2POBLACION,EN,", "01,-,1,2", "DISTRITOS,-,AÑO,,2022,SE.,2",
                       "01,-,2,3POBLACION,EN,", "01,-,2,3", "DISTRITOS,-,AÑO,,2022,SE.,3",
                       "01,-,3,4POBLACION,EN,", "01,-,3,4", "DISTRITOS,-,AÑO,,2022,SE.,4",
                       "01,-,4,5POBLACION,EN,", "01,-,4,5", "DISTRITOS,-,AÑO,,2022,SE.,5",
                       "01,-,5,6POBLACION,EN,", "01,-,5,6", "DISTRITOS,-,AÑO,,2022,SE.,6",
                       "01,-,6,7POBLACION,EN,", "01,-,6,7", "DISTRITOS,-,AÑO,,2022,SE.,7",
                       "01,-,7,8POBLACION,EN,", "01,-,7,8", "DISTRITOS,-,AÑO,,2022,SE.,8",
                       "01,-,8,9POBLACION,EN,", "01,-,8,9", "DISTRITOS,-,AÑO,,2022,SE.,9",
                       "01,-,9,10POBLACION,EN,", "01,-,9,10", "DISTRITOS,-,AÑO,,2022,SE.,10",
                       "01,-,10,11POBLACION,EN,", "01,-,10,11", "DISTRITOS,-,AÑO,,2022,SE.,11",
                       "01,-,11,12POBLACION,EN,", "01,-,11,12", "DISTRITOS,-,AÑO,,2022,SE.,12",
                       "01,-,12,13POBLACION,EN,", "01,-,12,13", "DISTRITOS,-,AÑO,,2022,SE.,13",
                       "01,-,13,14POBLACION,EN,", "01,-,13,14", "DISTRITOS,-,AÑO,,2022,SE.,14",
                       "01,-,14,15POBLACION,EN,", "01,-,14,15", "DISTRITOS,-,AÑO,,2022,SE.,15",
                       "01,-,15,16POBLACION,EN,", "01,-,15,16", "DISTRITOS,-,AÑO,,2022,SE.,16",
                       "01,-,16,17POBLACION,EN,", "01,-,16,17", "DISTRITOS,-,AÑO,,2022,SE.,17",
                       "01,-,17,18POBLACION,EN,", "01,-,17,18", "DISTRITOS,-,AÑO,,2022,SE.,18",
                       "01,-,18,19POBLACION,EN,", "01,-,18,19", "DISTRITOS,-,AÑO,,2022,SE.,19",
                       "01,-,19,20POBLACION,EN,", "01,-,19,20", "DISTRITOS,-,AÑO,,2022,SE.,20",
                       "01,-,20,21POBLACION,EN,", "01,-,20,21", "DISTRITOS,-,AÑO,,2022,SE.,21",
                       "01,-,21,22POBLACION,EN,", "01,-,21,22", "DISTRITOS,-,AÑO,,2022,SE.,22",
                       "01,-,22,23POBLACION,EN,", "01,-,22,23", "DISTRITOS,-,AÑO,,2022,SE.,23",
                       "01,-,23,24POBLACION,EN,", "01,-,23,24", "DISTRITOS,-,AÑO,,2022,SE.,24",
                       "01,-,24,25POBLACION,EN,", "01,-,24,25", "DISTRITOS,-,AÑO,,2022,SE.,25",
                       "01,-,25,26POBLACION,EN,", "01,-,25,26", "DISTRITOS,-,AÑO,,2022,SE.,26",
                       "01,-,26,27POBLACION,EN,", "01,-,26,27", "DISTRITOS,-,AÑO,,2022,SE.,27",
                       "01,-,27,28POBLACION,EN,", "01,-,27,28", "DISTRITOS,-,AÑO,,2022,SE.,28",
                       "01,-,28,29POBLACION,EN,", "01,-,28,29", "DISTRITOS,-,AÑO,,2022,SE.,29",
                       "01,-,29,30POBLACION,EN,", "01,-,29,30", "DISTRITOS,-,AÑO,,2022,SE.,30",
                       "01,-,30,31POBLACION,EN,", "01,-,30,31", "DISTRITOS,-,AÑO,,2022,SE.,31",
                       "01,-,31,32POBLACION,EN,", "01,-,31,32", "DISTRITOS,-,AÑO,,2022,SE.,32",
                       "01,-,32,33POBLACION,EN,", "01,-,32,33", "DISTRITOS,-,AÑO,,2022,SE.,33",
                       "01,-,33,34POBLACION,EN,", "01,-,33,34", "DISTRITOS,-,AÑO,,2022,SE.,34",
                       "01,-,34,35POBLACION,EN,", "01,-,34,35", "DISTRITOS,-,AÑO,,2022,SE.,35",
                       "01,-,35,36POBLACION,EN,", "01,-,35,36", "DISTRITOS,-,AÑO,,2022,SE.,36",
                       "01,-,36,37POBLACION,EN,", "01,-,36,37", "DISTRITOS,-,AÑO,,2022,SE.,37",
                       "01,-,37,38POBLACION,EN,", "01,-,37,38", "DISTRITOS,-,AÑO,,2022,SE.,38",
                       "01,-,38,39POBLACION,EN,", "01,-,38,39", "DISTRITOS,-,AÑO,,2022,SE.,39",
                       "01,-,39,40POBLACION,EN,", "01,-,39,40", "DISTRITOS,-,AÑO,,2022,SE.,40",
                       "01,-,40,41POBLACION,EN,", "01,-,40,41", "DISTRITOS,-,AÑO,,2022,SE.,41",
                       "01,-,41,42POBLACION,EN,", "01,-,41,42", "DISTRITOS,-,AÑO,,2022,SE.,42",
                       "01,-,42,43POBLACION,EN,", "01,-,42,43", "DISTRITOS,-,AÑO,,2022,SE.,43",
                       "01,-,43,44POBLACION,EN,", "01,-,43,44", "DISTRITOS,-,AÑO,,2022,SE.,44",
                       "01,-,44,45POBLACION,EN,", "01,-,44,45", "DISTRITOS,-,AÑO,,2022,SE.,45"]
departamentos_compuestos = {
    "LA,LIBERTAD": "LA LIBERTAD",
    "MADRE,DE,DIOS": "MADRE DE DIOS",
    "SAN,MARTIN": "SAN MARTIN"
}
provincias_compuestas = {
    "RODRIGUEZ,DE,MENDOZA": "RODRIGUEZ DE MENDOZA",
    "ANTONIO,RAIMONDI": "ANTONIO RAIMONDI",
    "CARLOS,FERMIN,FITZCARRALD": "CARLOS FERMIN FITZCARRALD",
    "MARISCAL,LUZURIAGA": "MARISCAL LUZURIAGA",
    "LA,UNION": "LA UNION",
    "HUANCA,SANCOS": "HUANCA SANCOS",
    "LA,MAR": "LA MAR",
    "PAUCAR,DEL,SARA,SARA": "PAUCAR DEL SARA SARA",
    "VICTOR,FAJARDO": "VICTOR FAJARDO",
    "VILCAS,HUAMAN": "VILCAS HUAMAN",
    "SAN,IGNACIO": "SAN IGNACIO",
    "SAN,MARCOS": "SAN MARCOS",
    "SAN,MIGUEL": "SAN MIGUEL",
    "SAN,PABLO": "SAN PABLO",
    "SANTA,CRUZ": "SANTA CRUZ",
    "LA,CONVENCION": "LA CONVENCION",
    "DOS,DE,MAYO": "DOS DE MAYO",
    "LEONCIO,PRADO": "LEONCIO PRADO",
    "PUERTO,INCA": "PUERTO INCA",
    "GRAN,CHIMU": "GRAN CHIMU",
    "SANCHEZ,CARRION": "SANCHEZ CARRION",
    "SANTIAGO,DE,CHUCO": "SANTIAGO DE CHUCO",
    "ALTO,AMAZONAS": "ALTO AMAZONAS",
    "DATEM,DEL,MARAï¿½ON": "DATEM DEL MARAÑON",
    "MARISCAL,RAMON,CASTILLA": "MARISCAL RAMON CASTILLA",
    "GENERAL,SANCHEZ,CERRO": "GENERAL SANCHEZ CERRO",
    "MARISCAL,NIETO": "MARISCAL NIETO",
    "DANIEL,ALCIDES,CARRION": "DANIEL ALCIDES CARRION",
    "EL,COLLAO": "EL COLLAO",
    "SAN,ANTONIO,DE,PUTINA": "SAN ANTONIO DE PUTINA",
    "SAN,ROMAN": "SAN ROMAN",
    "EL,DORADO": "EL DORADO",
    "MARISCAL,CACERES": "MARISCAL CACERES",
    "SAN,MARTIN": "SAN MARTIN",
    "JORGE,BASADRE": "JORGE BASADRE",
    "CONTRALMIRANTE,VILLAR": "CONTRALMIRANTE VILLAR",
    "CORONEL,PORTILLO": "CORONEL PORTILLO",
    "PADRE,ABAD": "PADRE ABAD"
}
provincias_no_coinciden = {
    "DOS": "DOS DE MAYO",
    "MARAÃ": "MARAÑON",
    "MARAï¿½ON": "MARAÑON",
    "SANTIAGO": "SANTIAGO DE CHUCO",
    "FERREÃ": "FERREÑAFE",
    "FERREï¿½AFE": "FERREÑAFE",
    "CAÃ‘": "CAÑETE",
    "CAÃ": "CAÑETE",
    "CAï¿½ETE": "CAÑETE",
    "ALTO": "ALTO AMAZONAS",
    "DATEM": "DATEM DEL MARAÑON",
    "DATEM DEL MARAï¿1⁄2ON": "DATEM DEL MARAÑON",
    "MARISCAL": "MARISCAL RAMON CASTILLA",
    "SAN": "SAN ROMAN"
}
distritos_no_coinciden = {
    "SAN FRANCISCO DE YESO": "SAN FRANCISCO DEL YESO",
    "MILPUCC": "MILPUC",
    "NEPEï¿½A": "NEPEÑA",
    "NEPEÑ A": "NEPEÑA",
    "SAN JUAN DE CHACÃ ‘A": "SAN JUAN DE CHACÑA",
    "SAN JUAN DE CHACÑ A": "SAN JUAN DE CHACÑA",
    "SAN JUAN DE CHACï¿½A": "SAN JUAN DE CHACÑA",
    "SAÃ‘ AYCA": "SAÑAYCA",
    "SAï¿½AYCA": "SAÑAYCA",
    "ANCO HUALLO": "ANCO-HUALLO",
    "HUAILLATI": "HUAYLLATI",
    "QUEQUEÃ ‘A": "QUEQUEÑA",
    "QUEQUEÑ A": "QUEQUEÑA",
    "QUEQUEï¿½A": "QUEQUEÑA",
    "SANTA RITA DE SIHUAS": "SANTA RITA DE SIGUAS",
    "OCOï¿½A": "OCOÑA",
    "UÃ‘ ON": "UÑON",
    "UÑ ON": "UÑON",
    "Uï¿½ON": "UÑON",
    "ANDRES AVELINO CACERES D.": "ANDRES AVELINO CACERES DORREGARAY",
    "CHAVIï¿½A": "CHAVIÑA",
    "OCAï¿½A": "OCAÑA",
    "CORONEL CASTAÃ ‘ EDA": "CORONEL CASTAÑEDA",
    "CORONEL CASTAÑ  EDA": "CORONEL CASTAÑEDA",
    "CORONEL CASTAï¿½EDA": "CORONEL CASTAÑEDA",
    "HUACAï¿½A": "HUACAÑA",
    "ENCAï¿½ADA": "ENCAÑADA",
    "LOS BAï¿½OS DEL INCA": "LOS BAÑOS DEL INCA",
    "SANTA CRUZ DE TOLED": "SANTA CRUZ DE TOLEDO",
    "CHANCAYBAï¿½OS": "CHANCAYBAÑOS",
    "QUIÃ ‘ OTA": "QUIÑOTA",
    "QUIï¿½OTA": "QUIÑOTA",
    "QUIÃ  OTA": "QUIÑOTA",
    "KOSï¿½IPATA": "KOSÑIPATA",
    "KOSÃ  IPATA": "KOSÑIPATA",
    "HUALLAY-GRANDE": "HUAYLLAY GRANDE",
    "QUITO ARMA": "QUITO-ARMA",
    "ï¿½AHUIMPUQUIO": "ÑAHUIMPUQUIO",
    "Ñ AHUIMPUQUIO": "ÑAHUIMPUQUIO",
    "TOMAY-KICHWA": "TOMAY KICHWA",
    "DE MAYO LA UNION": "LA UNION",
    "PUï¿½OS": "PUÑOS",
    "BAÃ‘ OS": "BAÑOS",
    "BAÑ EOS": "BAÑOS",
    "BAï¿½OS": "BAÑOS",
    "DANIEL ALOMIA ROBLES": "DANIEL ALOMIAS ROBLES",
    "‘ ON CHOLON": "CHOLON",
    " ON CHOLON": "CHOLON",
    "‘ ON HUACRACHUCO": "HUACRACHUCO",
    " ON HUACRACHUCO": "HUACRACHUCO",
    "‘ ON LA MORADA": "LA MORADA",
    " ON LA MORADA": "LA MORADA",
    "‘ ON SAN BUENAVENTURA": "SAN BUENAVENTURA",
    " ON SAN BUENAVENTURA": "SAN BUENAVENTURA",
    "‘ ON SANTA ROSA DE ALTO YANAJANCA": "SANTA ROSA DE ALTO YANAJANCA",
    " ON SANTA ROSA DE ALTO YANAJANCA": "SANTA ROSA DE ALTO YANAJANCA",
    "LA TINGUIÃ ‘A": "LA TINGUIÑA",
    "LA TINGUIï¿½A": "LA TINGUIÑA",
    "SAï¿½O": "SAÑO",
    "SAN PEDRO DE SAï¿½O": "SAÑO",
    "LEONOR ORDOï¿½EZ": "LEONOR ORDOÑEZ",
    "HUAY HUAY": "HUAY-HUAY",
    "DE CHUCO SANTA CRUZ DE CHUCA": "SANTA CRUZ DE CHUCA",
    "SAï¿½A": "SAÑA",
    "‘ AFE CAï¿½ARIS": "CAÑARIS",
    "CAï¿½ARIS": "CAÑARIS",
    "‘ AFE INCAHUASI": "INCAHUASI",
    " AFE INCAHUASI": "INCAHUASI",
    "‘ AFE MANUEL ANTONIO MESONES MURO": "MANUEL ANTONIO MESONES MURO",
    " AFE MANUEL ANTONIO MESONES MURO": "MANUEL ANTONIO MESONES MURO",
    "‘ AFE PITIPO": "PITIPO",
    " AFE PITIPO": "PITIPO",
    "‘ AFE PUEBLO NUEVO": "PUEBLO NUEVO",
    " AFE PUEBLO NUEVO": "PUEBLO NUEVO",
    "FERREï¿½AFE": "FERREÑAFE",
    "ETE ASIA": "ASIA",
    "ETE CALANGO": "CALANGO",
    "ETE CERRO AZUL": "CERRO AZUL",
    "ETE CHILCA": "CHILCA",
    "ETE COAYLLO": "COAYLLO",
    "‘ ETE IMPERIAL": "IMPERIAL",
    "ETE LUNAHUANA": "LUNAHUANA",
    "ETE MALA": "MALA",
    "ETE NUEVO IMPERIAL": "NUEVO IMPERIAL",
    "ETE PACARAN": "PACARAN",
    "ETE QUILMANA": "QUILMANA",
    "ETE SAN ANTONIO": "SAN ANTONIO",
    "ETE SAN LUIS": "SAN LUIS",
    "ETE SANTA CRUZ DE FLORES": "SANTA CRUZ DE FLORES",
    "ETE ZUÃ‘ IGA": "ZUÑIGA",
    "ZUï¿½IGA": "ZUÑIGA",
    "SAN VICENTE DE CAï¿½ETE": "SAN VICENTE DE CAÑETE",
    "CASTA": "SAN PEDRO DE CASTA",
    "SAN JOSE DE LOS CHORRILLOS": "CUENCA",
    "BREï¿½A": "BREÑA",
    "ALLAUCA": "AYAUCA",
    "HUAï¿½EC": "HUAÑEC",
    "HUAÃ  EC": "HUAÑEC",
    "VIï¿½AC": "VIÑAC",
    "AMAZONAS SANTA CRUZ": "SANTA CRUZ",
    "DEL MARAÃ ‘ ON ANDOAS": "ANDOAS",
    "DEL MARAÃ  ON ANDOAS": "ANDOAS",
    "DEL MARAÃ ‘ ON BARRANCA": "BARRANCA",
    "DEL MARAÃ  ON BARRANCA": "BARRANCA",
    "DEL MARAÃ ‘ ON CAHUAPANAS": "CAHUAPANAS",
    "DEL MARAÃ  ON CAHUAPANAS": "CAHUAPANAS",
    "DEL MARAÃ ‘ ON MANSERICHE": "MANSERICHE",
    "DEL MARAÃ  ON MANSERICHE": "MANSERICHE",
    "DEL MARAÃ ‘ ON MORONA": "MORONA",
    "DEL MARAÃ  ON MORONA": "MORONA",
    "DEL MARAÃ ‘ ON PASTAZA": "PASTAZA",
    "DEL MARAÃ  ON PASTAZA": "PASTAZA",
    "RAMON CASTILLA SAN PABLO": "SAN PABLO",
    "Iï¿½APARI": "IÑAPARI",
    "ICHUï¿½A": "ICHUÑA",
    "SAN FCO DE ASIS DE YARUSYACAN": "SAN FRANCISCO DE ASIS DE YARUSYACAN",
    "PARIï¿½AS": "PARIÑAS",
    "PARIÑ  AS": "PARIÑAS",
    "MUï¿½ANI": "MUÑANI",
    "CAPASO": "CAPAZO",
    "NUï¿½OA": "NUÑOA",
    "MAï¿½AZO": "MAÑAZO",
    "ROMAN SAN MIGUEL": "SAN MIGUEL",
    "SAN PEDRO DE PUTINA PUNCU": "SAN PEDRO DE PUTINA PUNCO",
    "CUï¿½UMBUQUI": "CUÑUMBUQUI",
    "CASPIZAPA": "CASPISAPA",
    "CORONEL GREGORIO ALBARRACIN L.": "CORONEL GREGORIO ALBARRACIN LANCHIPA",
    "ESTIQUE PAMPA": "ESTIQUE-PAMPA",
    "UNION ASHANINKA": "UNION ASHÁNINKA"
}


def ubigeo(departamento, provincia, distrito):
    with open("../recursos/TB_UBIGEOS.csv", "r", encoding="utf8") as archivo_csv:
        data = archivo_csv.read()
    data = list(data.split("\n"))
    for fila in data:
        fila = list(fila.split(","))
        if len(fila) == 17:
            if fila[4] == departamento and fila[6] == provincia and fila[7] == distrito:
                return fila[2]


def fechas(semana):
    with open("../recursos/minsa/calendario.csv", "r") as archivo_csv:
        data = archivo_csv.read()
    fila = list(list(data.split("\n"))[semana - 1].split(','))
    return fila[1], fila[2]


# def parseo(archivo, semana, fecha_inicio, fecha_fin):
def parseo(archivo, semana):
    if semana == 1:
        nro_columnas = 7
    else:
        nro_columnas = 8
    contenido = ""
    try:
        pdf = PdfReader(archivo)
        for pagina in pdf.pages:
            linea = pagina.extractText().split("\n")
            for palabras in linea:
                fila = ""
                for palabra in palabras.split(" "):
                    fila += "{},".format(palabra)
                fila = fila[0:len(fila) - 1]
                if not (fila in filas_no_permitidas):
                    if len(palabras.split(" ")) > nro_columnas:
                        if "RONTOY" in fila:
                            fila = fila[:-13]
                        for departamento in departamentos_compuestos:
                            if departamento in fila:
                                fila = fila.replace(departamento, departamentos_compuestos[departamento], 1)
                                break
                        for provincia in provincias_compuestas:
                            if provincia in fila:
                                fila = fila.replace(provincia, provincias_compuestas[provincia], 1)
                                break
                        info = fila.split(",")
                        if len(info) > nro_columnas:
                            departamento = info[0]
                            provincia = info[1]
                            medidas = info[(len(info) - (nro_columnas - 3)):len(info)]
                            distrito_fraccionado = info[2:len(info) - (nro_columnas - 3)]
                            nueva_fila = "{},{},".format(departamento, provincia)
                            for fraccion in distrito_fraccionado:
                                nueva_fila += "{} ".format(fraccion)
                            nueva_fila = nueva_fila[0:len(nueva_fila) - 1]
                            nueva_fila += ","
                            for medida in medidas:
                                nueva_fila += "{},".format(medida)
                            nueva_fila = nueva_fila[0:len(nueva_fila) - 1]
                            fila = nueva_fila
                    if nro_columnas == 7:
                        nueva_fila = ""
                        i = 0
                        for valor in fila.split(","):
                            if i == 3:
                                nueva_fila += "{},{},".format(0, valor)
                            else:
                                nueva_fila += "{},".format(valor)
                            i += 1
                        nueva_fila = nueva_fila[0:len(nueva_fila) - 1]
                        fila = nueva_fila
                    info = fila.split(",")
                    provincia = info[1]
                    distrito = info[2]
                    if provincia in provincias_no_coinciden:
                        provincia = provincias_no_coinciden[provincia]
                    if distrito in distritos_no_coinciden:
                        distrito = distritos_no_coinciden[distrito]
                    # nueva_fila = "{},".format(ubigeo(info[0], provincia, distrito))
                    # for valor in info:
                    #     nueva_fila += "{},".format(valor)
                    nueva_fila = ""
                    i = 0
                    for valor in info:
                        if i == 1:
                            nueva_fila += "{},".format(provincia)
                        elif i == 2:
                            nueva_fila += "{},".format(distrito)
                        else:
                            nueva_fila += "{},".format(valor)
                        i += 1
                    nueva_fila = nueva_fila[0:len(nueva_fila) - 1]
                    fila = nueva_fila
                    # fila += ',{},{}'.format(fecha_inicio, fecha_fin)
                    fila += ',{}'.format(semana)
                    contenido += fila
                    contenido += "\n"
    except PdfReadError:
        os.remove(archivo)
        print("Archivo PDF inexistente para la Semana Epidemiológica {}".format(semana))
    return contenido


def main():
    anio = sys.argv[1]
    semana_final = int(sys.argv[2])
    # contenido = "Ubigeo,Departamento,Provincia,Distrito,SemanasEpidemologicasAnteriores,SemanaEpidemiologicaActual," \
    #             "TotalGeneral,Mortalidad,PoblacionEnRiesgo,FechaInicio,FechaFin\n"
    contenido = "Departamento,Provincia,Distrito,SemanasEpidemologicasAnteriores,SemanaEpidemiologicaActual," \
                "TotalGeneral,Mortalidad,PoblacionEnRiesgo,SemanaEpidemiologica\n"
    for semana in range(1, semana_final + 1):
        url = "https://www.dge.gob.pe/portal/docs/vigilancia/cdistritos/{}/{}/" \
              "IRA%20-%20DEFUNCIONES.pdf".format(anio, str(semana).zfill(2))
        print(url)
        r = requests.get(url)
        nombre_archivo = "{}-SE{}.pdf".format(anio, semana)
        archivo_destino = "../recursos/minsa/{}".format(nombre_archivo)
        with open(archivo_destino, 'wb') as f:
            f.write(r.content)
        # fecha_inicio, fecha_fin = fechas(semana)
        # contenido += parseo(archivo_destino, semana, fecha_inicio, fecha_fin)
        contenido += parseo(archivo_destino, semana)
    archivo = "minsa.csv"
    destino = "../recursos/minsa/{}".format(archivo)
    with open(destino, 'wb') as f:
        f.write(contenido.encode())
    cloud = Storage()
    bucket = cloud.crear_bucket(cloud.client.project)
    cloud.subir_archivo(bucket, archivo, destino)


if __name__ == "__main__":
    main()
