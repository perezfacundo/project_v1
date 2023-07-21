# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator
# import datetime
# from django.utils import timezone
# # Create your models here.


# class Estado(models.Model):
#     descripcion = models.CharField(max_length=20)

#     def __str__(self):
#         return self.descripcion


# class Solicitud(models.Model):
#     desde = models.CharField(max_length=50)
#     hasta = models.CharField(max_length=50)
#     fechaSolicitud = models.DateField(blank=False, default=datetime.date(1, 1, 1))
#     fechaTrabajo = models.DateField(blank=False, default=datetime.date(1, 1, 1))
#     detalles = models.TextField(max_length=200, null=True)
#     estados = [
#         ('1', 'A presupuestar'),
#         ('2', 'Confirmado'),
#         ('3', 'En camino'),
#         ('4', 'Entregado'),
#         ('5', 'Cobrado'),
#     ]
#     estado = models.CharField(max_length=1, choices=estados, default=1)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         resultado = "{0} → {1}, el {2}. {3}"

#         return resultado.format(self.desde, self.hasta, self.fechaTrabajo.strftime("%A %d/%m/%Y"), self.estados[int(self.estado)][1])

from django.db import models
from django.contrib.auth.models import AbstractUser

class usuario(AbstractUser):
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
    idEstado = models.CharField(max_length=2)
    
class cliente(usuario):
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
    # dni = models.CharField(max_length=8)
    # telefono = models.CharField(max_length=10)
    # idEstado = models.CharField(max_length=2)
    
    
    
    # es_propietario = models.BooleanField(default=False, verbose_name='es propietario')
    # es_administrativo = models.BooleanField(default=False, verbose_name='es administrativo')
    # es_empleadoCalle = models.BooleanField(default=False, verbose_name='es empleado de vehiculo')
    # es_cliente = models.BooleanField(default=True, verbose_name='es cliente')

    # def __str__(self):
    #     r = "{0} {1}, es {3}"
    #     tipoUsuario = ""
    #     if self.es_propietario:
    #         tipoUsuario+= self.es_propietario._meta.get_field('es_propietario') 
    #     if self.es_administrativo:
    #         tipoUsuario+= self.es_administrativo._meta.get_field('es_administrativo')
    #     if self.es_empleadoCalle:
    #         tipoUsuario+= self.empleadoCalle._meta.get_field('es_empleado de vehiculo')
    #     if self.es_cliente:
    #         tipoUsuario+= self.es_cliente._meta.get_field('es_cliente')
    #     return r.format(self.last_name, self.first_name, tipoUsuario)
