from django.db import models

class Departamento(models.Model):
    nombre = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=25, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    nombre = models.CharField(max_length=36)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    ubigeo = models.IntegerField()
    altitud = models.IntegerField()

    def __str__(self):
        return self.nombre
