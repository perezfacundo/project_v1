from django.contrib import admin
from .models import Usuario, EstadosCliente, Cliente, EstadosEmpleadoCalle, EmpleadoCalle, EstadosEmpleadoAdmnistrativo, EmpleadoAdministrativo, tipo_usuario, EstadosSolicitud, Solicitud, EstadosTransporte, Transporte, SolicitudesEmpleados, SolicitudesTransportes

# Register your models here.

admin.site.register(Usuario)
admin.site.register(EstadosCliente)
admin.site.register(Cliente)
admin.site.register(EstadosEmpleadoCalle)
admin.site.register(EmpleadoCalle)
admin.site.register(EstadosEmpleadoAdmnistrativo)
admin.site.register(EmpleadoAdministrativo)
admin.site.register(tipo_usuario)
admin.site.register(EstadosSolicitud)
admin.site.register(Solicitud)
admin.site.register(EstadosTransporte)
admin.site.register(Transporte)
admin.site.register(SolicitudesEmpleados)
admin.site.register(SolicitudesTransportes)