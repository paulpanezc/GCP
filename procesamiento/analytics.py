from big_query import BigQuery


def main():
    big_query = BigQuery()
    big_query.crear_dataset("capa_analytics", "US")
    query = """
        CREATE OR REPLACE TABLE `{}.{}.{}` AS
        SELECT m.Ubigeo, m.Departamento, m.Provincia, m.Distrito, m.Mortalidad, m.PoblacionEnRiesgo, 
        CASE 
            WHEN m.Mortalidad BETWEEN 0 AND 65 THEN 0
            ELSE 1
            END AS NivelMortalidad,
        ROUND((m.Mortalidad / 100) * m.PoblacionEnRiesgo) AS Defunciones, 
        m.SemanasEpidemiologicas, m.FechaInicio AS FechaInicioSE, m.FechaFin AS FechaFinSE, 
        s.CodigoEstacion, s.NombreEstacion, s.TipoEstacion, s.Latitud, s.Longitud, CAST(s.Altitud AS INT64) AS Altitud, 
        s.Fecha AS FechaMedicion, s.Temperatura, s.Humedad, s.Precipitacion 
        FROM `{}.{}.{}` m
        INNER JOIN `{}.{}.{}` s
        ON m.Ubigeo = s.Ubigeo
        WHERE s.Fecha >= m.FechaInicio AND s.Fecha <= m.FechaFin
        ORDER BY m.Mortalidad DESC, m.PoblacionEnRiesgo DESC
    """.format(big_query.project, "capa_analytics", "minsa_senamhi", big_query.project, "capa_work",
               "minsa_puno_ubigeo_calendario", big_query.project, "capa_work", "senamhi_CO_EMA_ubigeo")
    big_query.ejecutar_consulta(query)


if __name__ == "__main__":
    main()
