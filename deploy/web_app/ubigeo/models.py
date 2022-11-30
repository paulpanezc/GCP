from django.db import models

class Departamento(models.Model):
    nombre = models.CharField(max_length=13, unique=True, blank=False, null=False)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=25, unique=True, blank=False, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    nombre = models.CharField(max_length=36, blank=False, null=False)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    ubigeo = models.IntegerField()
    altitud = models.IntegerField()
    latitud = models.CharField(max_length=8, blank=False, null=False)
    longitud = models.CharField(max_length=8, blank=False, null=False)

    def __str__(self):
        return self.nombre
