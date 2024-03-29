from django.utils import timezone
from datetime import datetime
from django.db import models
from django.forms import DateField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

# ACTORES DE LOS CASOS DE USO ====================


class TiposUsuario(models.Model):
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.descripcion}"

    def to_dict(self):
        return {"id": self.id, "descripcion": self.descripcion}

    class Meta:
        verbose_name_plural = "Tipos de usuarios"


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
    fecha_creacion = models.DateField(null=True)
    id_tipo_usuario = models.ForeignKey(TiposUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"0{self.id} - {self.last_name} {self.first_name} {self.id_tipo_usuario.descripcion}"

    def to_dict(self):
        return {
            "id": self.id,
            "is_superuser": self.is_superuser,
            "is_staff": self.is_staff,
            "username": self.username,
            "dni": self.dni,
            "tipo_usuario": self.id_tipo_usuario.descripcion,
            "is_active": self.is_active,
            "email": self.email,
        }

    class Meta:
        verbose_name_plural = "Usuarios"


class EstadosCliente(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = "Estados de clientes"


class Cliente(Usuario):
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
    # dni = charField
    # telefono = charField
    # id_tipo_usuario
    fecha_nac = models.DateField(null=True)
    puntos = models.IntegerField(null=True)
    id_estado_cliente = models.ForeignKey(EstadosCliente, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, parent_link=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "dni": self.dni,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "telefono": self.telefono,
            "email": self.email,
            "estado": self.id_estado_cliente.descripcion,
        }

    class Meta:
        verbose_name_plural = "Clientes"


class EstadosEmpleado(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = "Estados de empleados"


class Empleado(Usuario):
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
    administrativo = models.BooleanField(default=False, null=True)
    fecha_nac = models.DateField(null=True)
    tipo_carnet = models.CharField(max_length=2)
    ausencias = models.IntegerField()
    id_estado_empleado = models.ForeignKey(EstadosEmpleado, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, parent_link=True)

    def __str__(self):
        return f""

    def to_dict(self):
        fUltLogin = None
        if self.last_login:
            fUltLogin = self.last_login.strftime("%d/%m/%Y %H:%M:%S")
        else:
            fUltLogin = "no inició"

        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "last_login": fUltLogin,
            "telefono": self.telefono,
            "ausencias": self.ausencias,
            "estado": self.id_estado_empleado.descripcion,
        }

    class Meta:
        verbose_name_plural = "Empleados"


# ==================================================


class EstadosSolicitud(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.descripcion}"

    def to_dict(self):
        return {"id": self.id, "descripcion": self.descripcion}

    class Meta:
        verbose_name_plural = "Estados de solicitudes"


class Solicitud(models.Model):
    objetos_a_transportar = models.TextField(max_length=255, null=True)
    detalles = models.TextField(max_length=255, null=True)
    direccion_desde = models.CharField(max_length=255, null=True)
    latitud_desde = models.CharField(max_length=13, null=True)
    longitud_desde = models.CharField(max_length=13, null=True)
    direccion_hasta = models.CharField(max_length=255, null=True)
    latitud_hasta = models.CharField(max_length=13, null=True)
    longitud_hasta = models.CharField(max_length=13, null=True)
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_trabajo = models.DateField(null=True)
    presupuesto = models.IntegerField(null=True)
    ha_pagado = models.IntegerField(validators=[MinValueValidator(0)])
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )  # de 1☆ a 5☆
    devolucion = models.TextField(max_length=200)
    id_estado_solicitud = models.ForeignKey(EstadosSolicitud, on_delete=models.CASCADE)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return (
            f"ID:{self.id}- Desde:{self.direccion_desde}- Hasta:{self.direccion_hasta}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": f"{self.cliente_id.last_name} {self.cliente_id.first_name}",
            "direccion_desde": self.direccion_desde,
            "direccion_hasta": self.direccion_hasta,
            "fecha_solicitud": self.fecha_solicitud.strftime("%d-%m-%Y"),
            "fecha_trabajo": self.fecha_trabajo.strftime("%d-%m-%Y"),
            "calificacion": self.calificacion,
            "estado": self.id_estado_solicitud.descripcion,
        }

    class Meta:
        verbose_name_plural = "Solicitudes"


class EstadosVehiculo(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.descripcion}"

    def to_dict(self):
        return {"id": self.id, "descripcion": self.descripcion}

    class Meta:
        verbose_name_plural = "Estados de vehiculos"


class Vehiculo(models.Model):
    dominio = models.CharField(max_length=7, unique=True)
    marca = models.CharField(max_length=20)
    nombre = models.CharField(max_length=30)
    modelo = models.CharField(max_length=4)
    capacidad = models.IntegerField(null=True)
    kilometraje = models.IntegerField(null=True, default='0')  # agregar a tabla
    fecha_ult_service = models.DateField(null=True)  # agregar a tabla
    kilometraje_desde_ult_service = models.IntegerField(null=True, default='0')  # agregar a tabla
    id_estado_vehiculo = models.ForeignKey(EstadosVehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID:{self.id}"

    def to_dict(self):
        
        ult_service = ""

        if self.fecha_ult_service == None:
            ult_service = "No se hizo"
        else:
            ult_service = self.fecha_ult_service.strftime("%d/%m/%Y")

        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "marca": self.marca,
            "dominio": self.dominio,
            "fecha_ult_service": ult_service,
            "kilometraje": self.kilometraje,
            "kilometraje_desde_ult_service": self.kilometraje_desde_ult_service,
            "estado": self.id_estado_vehiculo.descripcion
        }

    class Meta:
        verbose_name_plural = "Vehiculos"


# =================================================


class SolicitudesEmpleados(models.Model):
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_empleado}"

    class Meta:
        verbose_name_plural = "Solicitudes y Empleados"


class SolicitudesVehiculos(models.Model):
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        # Acceder a las propiedades de la solicitud relacionada
        return f"{self.id}"

    class Meta:
        verbose_name_plural = "Solicitudes y vehiculos"
