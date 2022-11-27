from big_query import BigQuery


def main():
    big_query = BigQuery()
    dataset = big_query.crear_dataset("capa_raw", "US")
    if dataset:
        tabla = big_query.crear_tabla(dataset, "ubigeo")
        if tabla:
            big_query.cargar_datos("gs://{}/TB_UBIGEOS.csv".format(big_query.project), tabla)
        tabla = big_query.crear_tabla(dataset, "calendario_epidemiologico")
        if tabla:
            big_query.cargar_datos("gs://{}/calendario.csv".format(big_query.project), tabla)
        tabla = big_query.crear_tabla(dataset, "minsa")
        if tabla:
            big_query.cargar_datos("gs://{}/minsa.csv".format(big_query.project), tabla)
            # big_query.cargar_datos("gs://{}/Minsa_limpio.txt".format(big_query.project), tabla)
        tabla = big_query.crear_tabla(dataset, "senamhiCO")
        if tabla:
            big_query.cargar_datos("gs://{}/senamhiCO.csv".format(big_query.project), tabla)
            # big_query.cargar_datos("gs://{}/SenamhiCO_limpio.txt".format(big_query.project), tabla)
            # big_query.cargar_datos("gs://{}/SenamhiCO_limpio_2.txt".format(big_query.project), tabla)
        tabla = big_query.crear_tabla(dataset, "senamhiEMA")
        if tabla:
            big_query.cargar_datos("gs://{}/senamhiEMA.csv".format(big_query.project), tabla)
            # big_query.cargar_datos("gs://{}/SenamhiEMA_limpio.txt".format(big_query.project), tabla)
            # big_query.cargar_datos("gs://{}/SenamhiEMA_limpio_2.txt".format(big_query.project), tabla)


if __name__ == "__main__":
    main()
