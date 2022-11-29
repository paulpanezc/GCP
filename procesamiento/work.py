from big_query import BigQuery


def main():
    big_query = BigQuery()
    big_query.crear_dataset("capa_work", "US")
    query = """
        CREATE OR REPLACE TABLE `{}.{}.{}` AS
        SELECT u.ubigeo_inei AS Ubigeo, m.Departamento, m.Provincia, m.Distrito, m.SemanasEpidemologicasAnteriores,
        m.SemanaEpidemiologicaActual, m.TotalGeneral, m.Mortalidad, m.PoblacionEnRiesgo,
        STRING_AGG(CAST(m.SemanaEpidemiologica AS STRING), ',') AS SemanasEpidemiologicas,
        ARRAY_AGG(c.FechaInicio ORDER BY c.FechaInicio ASC LIMIT 1)[OFFSET(0)] AS FechaInicio,
        ARRAY_AGG(c.FechaFin ORDER BY c.FechaFin DESC LIMIT 1)[OFFSET(0)] AS FechaFin
        FROM `{}.{}.{}` m
        INNER JOIN `{}.{}.{}` u
        ON u.distrito = m.Distrito
        INNER JOIN `{}.{}.{}` c
        ON c.SemanaEpidemiologica = m.SemanaEpidemiologica
        WHERE m.Departamento = 'PUNO' AND u.departamento = m.Departamento AND u.provincia = m.Provincia
        GROUP BY u.ubigeo_inei, m.Departamento, m.Provincia, m.Distrito, m.SemanasEpidemologicasAnteriores,
        m.SemanaEpidemiologicaActual, m.TotalGeneral, m.Mortalidad, m.PoblacionEnRiesgo
    """.format(big_query.project, "capa_work", "minsa_puno_ubigeo_calendario", big_query.project, "capa_raw", "minsa",
               big_query.project, "capa_raw", "ubigeo", big_query.project, "capa_raw", "calendario_epidemiologico")
    big_query.ejecutar_consulta(query)
    query = """
        CREATE OR REPLACE TABLE `{}.{}.{}` AS
        SELECT u.ubigeo_inei AS Ubigeo, e.Departamento, e.Provincia, e.Distrito, e.Latitud, e.Longitud,
        SUBSTRING(e.Altitud, 0 ,4) AS Altitud, e.C__digo AS CodigoEstacion, e.Estaci__n AS NombreEstacion,
        e.Tipo AS TipoEstacion, e.Fecha, e.Temperatura___C_ AS Temperatura,
        e.Precipitaci__n__mm_hora__ * 24 AS Precipitacion, e.Humedad___ AS Humedad
        FROM `{}.{}.{}` e
        INNER JOIN `{}.{}.{}` u
        ON u.distrito = e.Distrito
        WHERE u.departamento = e.Departamento AND u.provincia = e.Provincia
        
        UNION ALL
        
        SELECT u.ubigeo_inei AS Ubigeo, c.Departamento, c.Provincia, c.Distrito, c.Latitud, c.Longitud,
        SUBSTRING(c.Altitud, 0 ,4) AS Altitud, CAST(c.C__digo AS STRING) AS CodigoEstacion,
        c.Estaci__n AS NombreEstacion, c.Tipo AS TipoEstacion, c.Fecha, c.TemperaturaMin___C_ AS Temperatura,
        c.Precipitacion_mm_d__a_ AS Precipitacion, c.HumedadRelativa___ AS Humedad
        FROM `{}.{}.{}` c
        INNER JOIN `{}.{}.{}` u
        ON u.distrito = c.Distrito
        WHERE u.departamento = c.Departamento AND u.provincia = c.Provincia
    """.format(big_query.project, "capa_work", "senamhi_CO_EMA_ubigeo", big_query.project, "capa_raw", "senamhiEMA",
               big_query.project, "capa_raw", "ubigeo", big_query.project, "capa_raw", "senamhiCO",
               big_query.project, "capa_raw", "ubigeo")
    big_query.ejecutar_consulta(query)


if __name__ == "__main__":
    main()
