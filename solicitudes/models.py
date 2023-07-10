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
    ESTADO_CHOICES = (
        ('1', 'A presupuestar'),
        ('2', 'Confirmado'),
        ('3', 'En camino'),
        ('4', 'Entregado'),
        ('6', 'Cobrado'),
        ('7', 'Cancelado'),
    )

    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=False, default="")
    telefono = models.CharField(max_length=20, blank=False, default="")
    inicio = models.CharField(max_length=100, blank=False, default="")
    fin = models.CharField(max_length=100, blank=False, default="")
    correo = models.CharField(max_length=100, blank=False, default="")
    fecha_entrada = models.DateField(blank=False, default=datetime.date(1, 1, 1))
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ESPERA')

    def __str__(self):
        return f"{self.nombre} - DNI: {self.dni}, Estado: {self.estado}"


    class Transporte(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    patente = models.CharField(max_length=100)
    # Otros campos del modelo Transporte

    def __str__(self):
        return f"Transporte para {self.solicitud} - tipo: {self.tipo} - patente: {self.patente}"

