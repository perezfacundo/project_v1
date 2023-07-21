from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import datetime
from django.utils import timezone

# ACTORES DE LOS CASOS DE USO ====================
class Usuario(AbstractUser):
    # id int [primary key]
    # password varchar
    # last_login datetime
    # is_superuser boolean
    # username varchar
    # first_name varchar
    # last_name varchar
    # email varchar
    # is_staff boolean //0 = no es empleado
    # is_active boolean
    # date_joined datetime
    dni = models.CharField(max_length=8)
    telefono = models.CharField(max_length=10)
    
class EstadosCliente(models):
    descripcion = models.CharField(max_length=20)
    
class Cliente(Usuario):
    puntos = models.IntegerField()
    idEstado = models.ForeignKey(EstadosCliente, on_delete=models.CASCADE)

class EstadosEmpleadoCalle(models):
    descripcion = models.CharField(max_length=20)

class EmpleadoCalle(Usuario):
    tipoCarnet = models.CharField()
    ausencias = models.IntegerField()
    idEstado = models.ForeignKey(EstadosEmpleadoCalle, on_delete=models.CASCADE)

class EstadosEmpleadoAdmnistrativo(models):
    descripcion = models.CharField(max_length=20)

class EmpleadoAdministrativo(Usuario):
    ausencias = models.IntegerField()
    idEstado = models.ForeignKey(EstadosEmpleadoAdmnistrativo, on_delete=models.CASCADE)

#==================================================

class EstadosSolicitud(models):
    descripcion = models.CharField(max_length=20)

class Solicitud(models):
    desde = models.CharField()
    hasta = models.CharField()
    fechaSolicitud = models.DateField(blank=False, default=datetime.date(1, 1, 1))
    fechaTrabajo = models.DateField(blank=False, default=datetime.date(1, 1, 1))
    detalles = models.TextField(max_length=200) #heladera, sillon, televisor, escritorio
    pagoFaltante = models.IntegerField() #10000
    calificacion = models.IntegerField() #de 1☆ a 5☆
    devolucion = models.TextField() #Los trabajadores fueron puntuales. Las cosas llegaron a destino en perfecto estado
    idEstado = models.ForeignKey(EstadosSolicitud, on_delete=models.CASCADE)

class EstadosTransporte(models):
    descripcion = models.CharField(max_length=20)

class Transporte(models):
    dominio = models.CharField(max_length=7)
    marca = models.CharField()
    nombre = models.CharField()
    modelo = models.IntegerField(max_length=4)
    capacidad = models.IntegerField()
    idEstado = models.ForeignKey(EstadosTransporte, on_delete=models.CASCADE)

#=================================================

class SolicitudesEmpleados(models):
    idSolicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    idEmpleado = models.ForeignKey(EmpleadoCalle, on_delete=models.CASCADE)

class SolicitudesTransportes(models):
    idSolicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    idTransporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)