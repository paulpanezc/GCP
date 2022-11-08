from PyPDF2 import PdfReader


filas_no_permitidas = ["01,-,40,41", "RIESGOCasos,Notificados,de,DEFUNCIONES,notificadas,por,neumonías,(Intra,y,Extra,Hospitalarias),,en,menores,de,5,años",
                       "DISTRITOS,-,AÑO,,2022,SE.,41", "DEPARTAMENTO,PROVINCIAS,DISTRITOSSEM.,EPIDEMIOLOGICAS,TOTAL,",
                       "GENERALMORTALIDAD", "Elaborado:,Area,de,Gestión,de,Desarrollo,de,Sistemas,de,la,Información,-,CDC",
                       "01,-,40,41POBLACION,EN,"]
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
    "PAUCAR,DEL,SARA": "PAUCAR DEL SARA SARA",
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
    "DATEM,DEL,MARAï¿½ON": "DATEM DEL MARAï¿1⁄2ON",
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


def main():
    contenido = "Departamento,Provincia,Distrito,SemanaEpidemiologica01-40,SemanaEpidemiologica41,TotalGeneral,Mortalidad,PoblacionEnRiesgo\n"
    with open("../recursos/minsa/defunciones.pdf", 'rb') as f:
        pdf = PdfReader(f)
        for pagina in pdf.pages:
            linea = pagina.extractText().split("\n")
            for palabras in linea:
                fila = ""
                for palabra in palabras.split(" "):
                    fila += "{},".format(palabra)
                fila = fila[0:len(fila) - 1]
                if not (fila in filas_no_permitidas):
                    if len(palabras.split(" ")) > 8:
                        for departamento in departamentos_compuestos:
                            if departamento in fila:
                                fila = fila.replace(departamento, departamentos_compuestos[departamento], 1)
                                break
                        for provincia in provincias_compuestas:
                            if provincia in fila:
                                fila = fila.replace(provincia, provincias_compuestas[provincia], 1)
                                break
                        if len(fila.split(",")) > 8:
                            departamento = fila.split(",")[0]
                            provincia = fila.split(",")[1]
                            info = fila.split(",")
                            medidas = fila.split(",")[(len(info) - 5):len(info)]
                            distrito_fraccionado = fila.split(",")[2:len(info) - 5]
                            nueva_fila = "{},{},".format(departamento, provincia)
                            for fraccion in distrito_fraccionado:
                                nueva_fila += "{} ".format(fraccion)
                            nueva_fila = nueva_fila[0:len(nueva_fila) - 1]
                            nueva_fila += ","
                            for medida in medidas:
                                nueva_fila += "{},".format(medida)
                            nueva_fila = nueva_fila[0:len(nueva_fila) - 1]
                            fila = nueva_fila
                    contenido += fila
                    contenido += "\n"
    with open("../recursos/minsa/defunciones.csv", 'wb') as f:
        f.write(contenido.encode())


if __name__ == "__main__":
    main()
