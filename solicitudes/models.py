from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Estado(models.Model):
    descripcion = models.CharField(max_length=20)
    def __str__(self):
        return self.descripcion

class Solicitud(models.Model):
    desde = models.CharField(max_length=50)
    hasta = models.CharField(max_length=50)
    fechaSolicitud = models.DateTimeField(auto_now_add=True)
    fechaTrabajo = models.DateTimeField()
    detalles = models.TextField(max_length=200, null=True)
    estado = models.ForeignKey(Estado, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    
    def __str__(self):
        # return f"{self.desde} -> {self.hasta} el {self.fechaTrabajo.day}/{self.fechaTrabajo.month}/{self.fechaTrabajo.year}. {self.estado.descripcion}"

        resultado = "{0} → {1}, el {2}. {3}"
        return resultado.format(self.desde, self.hasta, self.fechaTrabajo.strftime("%A %d/%m/%Y"), self.estado)