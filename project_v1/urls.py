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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # rutas solicitudes
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('solicitudes/crear/', views.solicitudes_crear, name='solicitudes_crear'),
    path('solicitudes/<int:solicitud_id>/', views.solicitud_detalle, name='solicitud_detalle'),
    path('solicitudes/<int:solicitud_id>/eliminar/', views.solicitud_eliminar, name='solicitud_eliminar'),

    #rutas empleados
    path('empleados/', views.empleados, name='empleados'),
    path('empleados/crear/', views.empleados_crear, name='empleados_crear'),
    path('empleados/<int:empleado_id>/', views.empleado_detalle, name='empleado_detalle'),
    path('empleados/<int:empleado_id>/eliminar/', views.empleado_eliminar, name='empleado_eliminar'),

    #rutas vehiculos
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos/crear/', views.vehiculos_crear, name='vehiculos_crear'),
    path('vehiculos/<int:vehiculo_id>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculos/<int:vehiculo_id>/eliminar/', views.vehiculo_eliminar, name='vehiculo_eliminar'),

    #rutas clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear/', views.clientes_crear, name='clientes_crear'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:cliente_id>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),

    #rutas authenticate
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]
