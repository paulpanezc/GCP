from big_query import BigQuery


def main():
    big_query = BigQuery()
    big_query.crear_dataset("capa_analytics", "US")
    query = """
        CREATE OR REPLACE TABLE `{}.{}.{}` AS
        SELECT m.Ubigeo, m.Departamento, m.Provincia, m.Distrito, m.PoblacionEnRiesgo, m.Mortalidad, 
        m.SemanasEpidemiologicas, m.FechaInicio AS FechaInicioSE, m.FechaFin AS FechaFinSE, 
        s.CodigoEstacion, s.NombreEstacion, s.TipoEstacion, s.Latitud, s.Longitud, s.Altitud, 
        ARRAY_AGG(s.Fecha) AS FechaMedicion, ARRAY_AGG(s.Temperatura) AS Temperatura, 
        ARRAY_AGG(s.Humedad) AS Humedad, ARRAY_AGG(s.Precipitacion) AS Precipitacion
        FROM `{}.{}.{}` m
        INNER JOIN `{}.{}.{}`s
        ON m.Ubigeo = s.Ubigeo
        WHERE s.Fecha >= m.FechaInicio AND s.Fecha <= m.FechaFin
        GROUP BY m.Ubigeo, m.Departamento, m.Provincia, m.Distrito, m.PoblacionEnRiesgo, 
        m.Mortalidad, m.SemanasEpidemiologicas, m.FechaInicio, m.FechaFin, 
        s.CodigoEstacion, s.NombreEstacion, s.TipoEstacion, s.Latitud, s.Longitud, s.Altitud
        ORDER BY m.Mortalidad DESC
    """.format(big_query.project, "capa_analytics", "minsa_senamhi", big_query.project, "capa_work",
               "minsa_puno_ubigeo_calendario", big_query.project, "capa_work", "senamhi_CO_EMA_ubigeo")
    big_query.ejecutar_consulta(query)


if __name__ == "__main__":
    main()
