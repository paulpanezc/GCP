PROYECTO PARA ANALIZAR LA MORTALIDAD EN MENORES DE 5 AÑOS POR NEUMONIA DEBIDO A HELADAS EN LA REGION DE PUNO

1.- Instalar las dependencias con el comando

> pip install -r requirements.txt 

2.- Descargar las credenciales para acceder al proyecto en google cloud

> gcloud auth application-default login

3.- Declarar la variable de entorno GOOGLE_APPLICATION_CREDENTIALS apuntando a la ubicación del archivo json que contiene las credenciales

4.- Ejecutar el sgte comando para crear un cluster que contenga las dependencias para la ingesta de datos

> gcloud dataproc clusters create cluster-ingesta-almacenamiento-procesamiento --region=us-east1 --properties=^#^dataproc:pip.packages='PyPDF2==2.11.1,requests==2.28.1'

5.- Seguir los pasos declarados en el directorio ingesta

6.- Seguir los pasos declarados en el directorio procesamiento
