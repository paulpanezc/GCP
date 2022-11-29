import os
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from ubigeo.models import Departamento, Provincia, Distrito


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


class API():
    def get_distritos(self, request, provincia_id):
        distritos = Distrito.objects.filter(provincia_id=provincia_id).order_by('nombre')
        data = serializers.serialize("json", distritos)
        return HttpResponse(data, content_type='application/json')

    def get_provincias(self, request, departamento_id):
        provincias = Provincia.objects.filter(departamento_id=departamento_id).order_by('nombre')
        data = serializers.serialize("json", provincias)
        return HttpResponse(data, content_type='application/json')

    def prediction(self, request):
        data = None
        # temas = Tema.objects.filter(topico_id = request.GET['id']).order_by('nombre')
        # data = serializers.serialize("json", temas)
        return HttpResponse(data, content_type='application/json')

    def ubigeo(self, request):
        ubigeo_csv = os.path.join(PROJECT_PATH, "../../../recursos/TB_UBIGEOS.csv")
        print(ubigeo_csv)
        with open(ubigeo_csv, "r", encoding="utf8") as archivo_csv:
            data = archivo_csv.read()
        data = list(data.split("\n"))
        i = 0
        for fila in data:
            if i > 0:
                fila = list(fila.split(","))
                print(fila)
                if len(fila) > 14:
                    ubigeo = fila[2]
                    nombre_departamento = fila[4]
                    nombre_provincia = fila[6]
                    nombre_distrito = fila[7]
                    altitud = fila[14]
                    if len(altitud) == 0:
                        altitud = 0
                    departamento = None
                    provincia = None
                    departamentos = Departamento.objects.filter(nombre=nombre_departamento)
                    if len(departamentos) == 0:
                        departamento = Departamento(nombre=nombre_departamento)
                        departamento.save()
                    elif len(departamentos) == 1:
                        departamento = departamentos[0]
                    if departamento:
                        print(departamento)
                        provincias = Provincia.objects.filter(nombre=nombre_provincia, departamento_id=departamento.id)
                        if len(provincias) == 0:
                            provincia = Provincia(nombre=nombre_provincia, departamento_id=departamento.id)
                            provincia.save()
                        elif len(provincias) == 1:
                            provincia = provincias[0]
                        if provincia:
                            print(provincia)
                            distritos = Distrito.objects.filter(nombre=nombre_distrito, provincia_id=provincia.id)
                            if len(distritos) == 0:
                                distrito = Distrito(nombre=nombre_distrito, provincia_id=provincia.id, ubigeo=ubigeo,
                                                    altitud=altitud)
                                distrito.save()
            i += 1
        return HttpResponse("Ubigeo creado satisfactoriamente.")
