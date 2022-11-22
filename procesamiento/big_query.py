from google.cloud import bigquery


class BigQuery:
    def __init__(self):
        self.client = bigquery.Client()
        self.project = self.client.project

    def crear_dataset(self, nombre_dataset, locacion):
        dataset_id = "{}.{}".format(self.project, nombre_dataset)
        try:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = locacion
            dataset = self.client.create_dataset(dataset, timeout=30)
            print("Dataset {} creado en el proyecto {}".format(dataset.dataset_id, self.project))
        except:
            dataset = self.client.get_dataset(dataset_id)
            print("Dataset {} ya existe.".format(nombre_dataset))
        return dataset

    def crear_tabla(self, dataset, nombre_tabla):
        tabla_id = "{}.{}.{}".format(self.project, dataset.dataset_id, nombre_tabla)
        try:
            tabla = bigquery.Table(tabla_id)
            tabla = self.client.create_table(tabla)
            print("Tabla {}.{}.{} creada".format(tabla.project, tabla.dataset_id, tabla.table_id))
        except:
            tabla = self.client.get_table(tabla_id)
            print("Tabla {} ya existe.".format(nombre_tabla))
        return tabla

    def cargar_datos(self, uri, tabla):
        tabla_id = "{}.{}.{}".format(tabla.project, tabla.dataset_id, tabla.table_id)
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
        )
        load_job = self.client.load_table_from_uri(
            uri, tabla_id, job_config=job_config
        )
        load_job.result()
        print("Se cargaron {} filas.".format(tabla.num_rows))

    def ejecutar_consulta(self, query):
        query_job = self.client.query(query)
        return query_job
