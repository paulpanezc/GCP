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
        ON u.departamento = m.Departamento AND u.provincia = m.Provincia AND u.distrito = m.Distrito
        INNER JOIN `{}.{}.{}` c
        ON c.A__o = m.A__o AND c.SemanaEpidemiologica = m.SemanaEpidemiologica
        WHERE m.Departamento = 'PUNO'
        GROUP BY u.ubigeo_inei, m.Departamento, m.Provincia, m.Distrito, m.SemanasEpidemologicasAnteriores, 
        m.SemanaEpidemiologicaActual, m.TotalGeneral, m.Mortalidad, m.PoblacionEnRiesgo
    """.format(big_query.project, "capa_work", "minsa_puno_ubigeo_calendario", big_query.project, "capa_raw", "minsa",
               big_query.project, "capa_raw", "ubigeo", big_query.project, "capa_raw", "calendario_epidemiologico")
    big_query.ejecutar_consulta(query)
    query = """
        CREATE OR REPLACE TABLE `{}.{}.{}` AS
        SELECT u.ubigeo_inei AS Ubigeo, e.Departamento, e.Provincia, e.Distrito, u.Latitud, u.Longitud, 
        SUBSTRING(e.Altitud, 0 ,4) AS Altitud, CAST(e.C__digo AS STRING) AS CodigoEstacion, e.Estaci__n AS 
        NombreEstacion, e.Tipo AS TipoEstacion, e.Fecha, AVG(CAST(e.Temperatura___C_ AS FLOAT64)) AS Temperatura, 
        AVG(CAST(e.Precipitaci__n_mm_hora_ AS FLOAT64)) * 24 AS Precipitacion, AVG(CAST(e.Humedad___ AS FLOAT64)) AS 
        Humedad
        FROM `{}.{}.{}` e
        INNER JOIN `{}.{}.{}` u 
        ON u.departamento = e.Departamento AND u.provincia = e.Provincia AND u.distrito = e.Distrito
        WHERE e.Temperatura___C_ <> 'S/D' AND e.Precipitaci__n_mm_hora_ <> 'S/D' AND e.Humedad___ <> 'S/D'
        GROUP BY e.Fecha, u.ubigeo_inei, e.Departamento, e.Provincia, e.Distrito, u.Latitud, u.Longitud, e.Altitud, 
        e.C__digo, e.Estaci__n, e.Tipo
        
        UNION ALL
        
        SELECT u.ubigeo_inei AS Ubigeo, c.Departamento, c.Provincia, c.Distrito, u.Latitud, u.Longitud, 
        SUBSTRING(c.Altitud, 0 ,4) AS Altitud, CAST(c.C__digo AS STRING) AS CodigoEstacion, 
        c.Estaci__n AS NombreEstacion, c.Tipo AS TipoEstacion, c.Fecha, CAST(c.TemperaturaMin___C_ AS FLOAT64) AS 
        Temperatura, CAST(c.Precipitacion_mm_d__a_ AS FLOAT64) AS Precipitacion, CAST(c.HumedadRelativa___ AS FLOAT64) 
        AS Humedad
        FROM `{}.{}.{}` c
        INNER JOIN `{}.{}.{}` u 
        ON u.departamento = c.Departamento AND u.provincia = c.Provincia AND u.distrito = c.Distrito
        WHERE c.TemperaturaMin___C_ <> 'S/D' AND c.Precipitacion_mm_d__a_ NOT IN  ('S/D', 'T') AND 
        c.HumedadRelativa___ <> 'S/D'
    """.format(big_query.project, "capa_work", "senamhi_CO_EMA_ubigeo", big_query.project, "capa_raw", "senamhiEMA",
               big_query.project, "capa_raw", "ubigeo", big_query.project, "capa_raw", "senamhiCO",
               big_query.project, "capa_raw", "ubigeo")
    big_query.ejecutar_consulta(query)


if __name__ == "__main__":
    main()
