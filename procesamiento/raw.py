from big_query import BigQuery


def main():
    big_query = BigQuery()
    dataset = big_query.crear_dataset("capa_raw", "US")
    if dataset:
        tabla = big_query.crear_tabla(dataset, "minsa")
        if tabla:
            big_query.cargar_datos("gs://dataminers-369202/minsa.csv", tabla)
        tabla = big_query.crear_tabla(dataset, "senamhiCO")
        if tabla:
            big_query.cargar_datos("gs://dataminers-369202/SenamhiCO_limpio_2.txt", tabla)
        tabla = big_query.crear_tabla(dataset, "senamhiEMA")
        if tabla:
            big_query.cargar_datos("gs://dataminers-369202/SenamhiEMA_limpio_2.txt", tabla)


if __name__ == "__main__":
    main()
