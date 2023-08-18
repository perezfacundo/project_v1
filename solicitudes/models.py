from django.utils import timezone
import datetime
from django.db import models
from django.forms import DateField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

# ACTORES DE LOS CASOS DE USO ====================

class tipo_usuario(models.Model):
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.descripcion}"

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
    id_tipo_usuario = models.ForeignKey(tipo_usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"0{self.id} - {self.last_name} {self.first_name}"

class EstadosCliente(models.Model):
    descripcion = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.descripcion}"

class Cliente(Usuario):
    puntos = models.IntegerField()
    id_estado_cliente = models.ForeignKey(EstadosCliente, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, parent_link=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} "

class EstadosEmpleadoCalle(models.Model):
    descripcion = models.CharField(max_length=20)

class EmpleadoCalle(Usuario):
    tipo_carnet = models.CharField(max_length=2)
    ausencias = models.IntegerField()
    id_estado_empleado_calle = models.ForeignKey(EstadosEmpleadoCalle, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, parent_link=True)

class EstadosEmpleadoAdmnistrativo(models.Model):
    descripcion = models.CharField(max_length=20)

class EmpleadoAdministrativo(Usuario):
    ausencias = models.IntegerField()
    id_estado_empleado_administrativo = models.ForeignKey(EstadosEmpleadoAdmnistrativo, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, parent_link=True)
    
#==================================================

class EstadosSolicitud(models.Model):
    descripcion = models.CharField(max_length=20)

class Solicitud(models.Model):
    objetos_a_transportar = models.TextField(max_length=255, null=True) #heladera, sillon, televisor, escritorio
    detalles = models.TextField(max_length=255, null=True) 
    direccion_desde = models.CharField(max_length=255, null=True)
    direccion_hasta = models.CharField(max_length=255, null=True)
    coordenadas_desde = models.CharField(max_length=50, blank=True, null=True)
    coordenadas_hasta = models.CharField(max_length=50, blank=True, null=True)
    fecha_solicitud = models.DateField(auto_now_add=True)
    pago_faltante = models.IntegerField(validators=[MinValueValidator(0)]) #10000
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True) #de 1☆ a 5☆
    devolucion = models.TextField(max_length=200) #Los trabajadores fueron puntuales. Las cosas llegaron a destino en perfecto estado
    id_estado_solicitud = models.ForeignKey(EstadosSolicitud, on_delete=models.CASCADE)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)

    def validar_dia_habil(value):
        if value < datetime.date.today():
            raise models.ValidationError("La fecha debe ser posterior al día de hoy.")
        
        # Verificar si la fecha seleccionada es un día hábil (diferente de sábado y domingo)
        weekday = value.weekday()
        if weekday >= 5:
            raise models.ValidationError("La fecha seleccionada debe ser un día hábil (de lunes a viernes).")
        pass

    fecha_trabajo = models.DateField(blank=False, validators=[validar_dia_habil])

class EstadosTransporte(models.Model):
    descripcion = models.CharField(max_length=20)

class Transporte(models.Model):
    dominio = models.CharField(max_length=7)
    marca = models.CharField(max_length=20)
    nombre = models.CharField(max_length=30)
    modelo = models.CharField(max_length=4)
    capacidad = models.IntegerField()
    id_estado_transporte = models.ForeignKey(EstadosTransporte, on_delete=models.CASCADE)

#=================================================

class SolicitudesEmpleados(models.Model):
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(EmpleadoCalle, on_delete=models.CASCADE)

class SolicitudesTransportes(models.Model):
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    id_transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)