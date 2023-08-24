from django.contrib import admin
from .models import Usuario, EstadosCliente, Cliente, EstadosEmpleado, Empleado, TiposUsuario, EstadosSolicitud, Solicitud, EstadosVehiculo, Vehiculo, SolicitudesEmpleados, SolicitudesVehiculos

# Register your models here.

admin.site.register(Usuario)
admin.site.register(EstadosCliente)
admin.site.register(Cliente)
admin.site.register(EstadosEmpleado)
admin.site.register(Empleado)
# admin.site.register(EstadosEmpleadoAdmnistrativo)
# admin.site.register(EmpleadoAdministrativo)
admin.site.register(TiposUsuario)
admin.site.register(EstadosSolicitud)
admin.site.register(Solicitud)
admin.site.register(EstadosVehiculo)
admin.site.register(Vehiculo)
admin.site.register(SolicitudesEmpleados)
admin.site.register(SolicitudesVehiculos)