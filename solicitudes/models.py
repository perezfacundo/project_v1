from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime
from django.utils import timezone
# Create your models here.


class Estado(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion


class Solicitud(models.Model):
    desde = models.CharField(max_length=50)
    hasta = models.CharField(max_length=50)
    fechaSolicitud = models.DateField(blank=False, default=datetime.date(1, 1, 1))
    fechaTrabajo = models.DateField(blank=False, default=datetime.date(1, 1, 1))
    detalles = models.TextField(max_length=200, null=True)
    estados = [
        ('1', 'A presupuestar'),
        ('2', 'Confirmado'),
        ('3', 'En camino'),
        ('4', 'Entregado'),
        ('5', 'Cobrado'),
    ]
    estado = models.CharField(max_length=1, choices=estados, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        resultado = "{0} → {1}, el {2}. {3}"

        return resultado.format(self.desde, self.hasta, self.fechaTrabajo.strftime("%A %d/%m/%Y"), self.estados[int(self.estado)][1])
