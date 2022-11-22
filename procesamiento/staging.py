from big_query import BigQuery


def main():
    big_query = BigQuery()
    big_query.crear_dataset("capa_staging", "US")
    query = """
        SELECT Departamento, SUM(Mortalidad) AS Defunciones
        FROM `{}.{}.{}`
        GROUP BY Departamento
        ORDER BY SUM(Mortalidad) DESC
        LIMIT 10
    """.format(big_query.project, "capa_raw", "minsa")
    query_job = big_query.ejecutar_consulta(query)
    for row in query_job:
        print("Departamento={}, defunciones={}".format(row[0], row["Defunciones"]))


if __name__ == "__main__":
    main()
