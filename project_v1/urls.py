"""
URL configuration for project_v1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))"""

from django.contrib import admin
from django.urls import path
from solicitudes import views

# from django.views import defaults

handler500 = 'solicitudes.views.error_view_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('historial_tasas_cambio/', views.historial_tasas_cambio, name="historial_tasas_cambio"),
    path('grafico_anual_solicitudes/', views.grafico_anual_solicitudes, name='grafico_anual_solicitudes'),
    path('grafico_anual_clientes/', views.grafico_anual_clientes, name='grafico_anual_clientes'),
    # rutas solicitudes
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('solicitudes_listado/', views.solicitudes_listado, name='solicitudes_listado'),
    path('solicitudes/crear/', views.solicitudes_crear, name='solicitudes_crear'),
    path('solicitudes/<int:solicitud_id>/', views.solicitud_detalle, name='solicitud_detalle'),
    path('solicitudes/eliminar/<int:solicitud_id>/', views.solicitud_eliminar, name='solicitud_eliminar'),
    path('solicitudes/calificar/<int:solicitud_id>/', views.solicitud_calificar, name='solicitud_calificar'),
    path('solicitudes/reportes/', views.solicitudes_reportes, name='solicitudes_reportes'),

    # rutas empleados
    path('empleados/', views.empleados, name='empleados'),
    path('empleados_listado/', views.empleados_listado, name='empleados_listado'),
    path('empleados/crear/', views.empleados_crear, name='empleados_crear'),
    path('empleados/<int:empleado_id>/', views.empleado_detalle, name='empleado_detalle'),
    path('empleados/<int:empleado_id>/eliminar/', views.empleado_eliminar, name='empleado_eliminar'),
    path('empleados/reportes/', views.empleados_reportes, name='empleados_reportes'),

    # rutas vehiculos
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos_listado/', views.vehiculos_listado, name='vehiculos_listado'),
    path('vehiculos/crear/', views.vehiculos_crear, name='vehiculos_crear'),
    path('vehiculos/<int:vehiculo_id>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculos/<int:vehiculo_id>/eliminar/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
    path('vehiculos/reportes/', views.vehiculos_reportes, name='vehiculos_reportes'),

    # rutas clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes_listado/', views.clientes_listado, name='clientes_listado'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:cliente_id>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),
    path('clientes/reportes/', views.clientes_reportes, name='clientes_reportes'),

    # rutas authenticate
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('recuperarCuenta/', views.recuperarCuenta, name='recuperarCuenta'),
    path('ingresarCodigoRecuperacion/', views.ingresarCodigoRecuperacion, name='ingresarCodigoRecuperacion'),
    path('cambiarClave/', views.cambiarClave, name='cambiarClave'),
]
