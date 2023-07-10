from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime
from django.utils import timezone
# Create your models here.


class TiposRegistros(models.Model):
    idTipoRegistro = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion


class Estados(models.Model):
    idEstado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=30)
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion


class Provincias(models.Model):
    idProvincia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Localidades(models.Model):
    idLocalidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    idProvincia = models.ForeignKey(Provincias, on_delete=models.CASCADE)
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Transportes(models.Model):
    idTransporte = models.AutoField(primary_key=True)
    patente = models.CharField(max_length=7)
    marca = models.CharField(max_length=30)
    modelo = models.SmallIntegerField()
    nombre = models.CharField(max_length=30)
    capacidad = models.IntegerField()
    idEstado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Clientes(models.Model):
    idCliente = models.AutoField(primary_key=True)
    dniCliente = models.IntegerField()
    apellidos = models.CharField(max_length=30)
    nombres = models.CharField(max_length=30)
    fechaNac = models.DateField()
    telefono = models.CharField(max_length=10)
    domicilio = models.CharField(max_length=40)
    correo = models.CharField(max_length=30)
    clave = models.CharField(max_length=250)
    idEstado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    idLocalidad = models.ForeignKey(Localidades, on_delete=models.CASCADE)
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class Solicitudes(models.Model):
    idSolicitud = models.IntegerField(primary_key=True)
    idCliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    coordDesde = models.CharField(max_length=50)
    coordHasta = models.CharField(max_length=50)
    fechaSolicitud = models.DateField()
    fechaTrabajo = models.DateField()
    pagoFaltante = models.DecimalField(max_digits=6, decimal_places=2)
    idEstado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    idLocalidadDesde = models.ForeignKey(Localidades, on_delete=models.CASCADE, related_name='solicitudes_desde')
    idLocalidadHasta = models.ForeignKey(Localidades, on_delete=models.CASCADE, related_name='solicitudes_hasta')
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return f"Solicitud {self.idSolicitud}"


class Empleados(models.Model):
    idEmpleado = models.IntegerField(primary_key=True)
    dniEmpleado = models.IntegerField()
    apellidos = models.CharField(max_length=30)
    nombres = models.CharField(max_length=30)
    fechaNac = models.DateField()
    porcComision = models.IntegerField()
    correo = models.CharField(max_length=30)
    clave = models.CharField(max_length=250)
    idEstado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    idTipoRegistro = models.ForeignKey(TiposRegistros, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class SolicitudesEmpleados(models.Model):
    idSE = models.IntegerField(primary_key=True)
    idSolicitud = models.ForeignKey(Solicitudes, on_delete=models.CASCADE)
    idEmpleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)

    def __str__(self):
        return f"Solicitud {self.idSolicitud} - Empleado {self.idEmpleado}"


class SolicitudesTransportes(models.Model):
    idST = models.IntegerField(primary_key=True)
    idSolicitud = models.ForeignKey(Solicitudes, on_delete=models.CASCADE)
    idTransporte = models.ForeignKey(Transportes, on_delete=models.CASCADE)

    def __str__(self):
        return f"Solicitud {self.idSolicitud} - Transporte {self.idTransporte}"

