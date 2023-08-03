from django.utils import timezone
import datetime
from django.db import models
from django.forms import DateField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

# ACTORES DE LOS CASOS DE USO ====================
class Usuario(AbstractUser):
    # id int [primary key]
    # password varchar !
    # last_login datetime
    # is_superuser boolean
    # username varchar !
    # first_name varchar !
    # last_name varchar !
    # email varchar !
    # is_staff boolean //0 = no es empleado
    # is_active boolean 
    # date_joined datetime
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=10)
    
class EstadosCliente(models.Model):
    descripcion = models.CharField(max_length=20)
    
class Cliente(Usuario):
    puntos = models.IntegerField()
    idEstadoCliente = models.ForeignKey(EstadosCliente, on_delete=models.CASCADE)

class EstadosEmpleadoCalle(models.Model):
    descripcion = models.CharField(max_length=20)

class EmpleadoCalle(Usuario):
    tipoCarnet = models.CharField(max_length=2)
    ausencias = models.IntegerField()
    idEstadoEmpleadoCalle = models.ForeignKey(EstadosEmpleadoCalle, on_delete=models.CASCADE)

class EstadosEmpleadoAdmnistrativo(models.Model):
    descripcion = models.CharField(max_length=20)

class EmpleadoAdministrativo(Usuario):
    ausencias = models.IntegerField()
    idEstadoEmpleadoAdministrativo = models.ForeignKey(EstadosEmpleadoAdmnistrativo, on_delete=models.CASCADE)

class tipoUsuario(models.Model):
    descripcion = models.CharField(max_length=30)
    
#==================================================

class EstadosSolicitud(models.Model):
    descripcion = models.CharField(max_length=20)

class Solicitud(models.Model):
    desde = models.CharField(max_length=50, null=False)
    hasta = models.CharField(max_length=50, null=False)
    fechaSolicitud = models.DateField(auto_now_add=True)
    detalles = models.TextField(max_length=200) #heladera, sillon, televisor, escritorio
    pagoFaltante = models.IntegerField(validators=[MinValueValidator(0)]) #10000
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) #de 1☆ a 5☆
    devolucion = models.TextField(max_length=200) #Los trabajadores fueron puntuales. Las cosas llegaron a destino en perfecto estado
    idEstadoSolicitud = models.ForeignKey(EstadosSolicitud, on_delete=models.CASCADE)

    def validar_dia_habil(value):
        if value < datetime.date.today():
            raise models.ValidationError("La fecha debe ser posterior al día de hoy.")
        
        # Verificar si la fecha seleccionada es un día hábil (diferente de sábado y domingo)
        weekday = value.weekday()
        if weekday >= 5:
            raise models.ValidationError("La fecha seleccionada debe ser un día hábil (de lunes a viernes).")
        pass

    fechaTrabajo = models.DateField(blank=False, validators=[validar_dia_habil])

class EstadosTransporte(models.Model):
    descripcion = models.CharField(max_length=20)

class Transporte(models.Model):
    dominio = models.CharField(max_length=7)
    marca = models.CharField(max_length=20)
    nombre = models.CharField(max_length=30)
    modelo = models.CharField(max_length=4)
    capacidad = models.IntegerField()
    idEstadoTransporte = models.ForeignKey(EstadosTransporte, on_delete=models.CASCADE)

#=================================================

class SolicitudesEmpleados(models.Model):
    idSolicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    idEmpleado = models.ForeignKey(EmpleadoCalle, on_delete=models.CASCADE)

class SolicitudesTransportes(models.Model):
    idSolicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    idTransporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)