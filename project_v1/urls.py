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

    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('solicitudes/crear/', views.solicitudes_crear, name='solicitudes_crear'),
    path('solicitudes/<int:solicitud_id>/', views.solicitud_detalle, name='solicitud_detalle'),
    path('solicitudes/<int:solicitud_id>/eliminar/', views.solicitud_eliminar, name='solicitud_eliminar'),

    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]
