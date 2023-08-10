from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import EstadosCliente, Cliente, EstadosEmpleadoCalle, EmpleadoCalle, EstadosEmpleadoAdmnistrativo, EmpleadoAdministrativo, tipo_usuario, EstadosSolicitud, Solicitud, EstadosTransporte, Transporte, SolicitudesEmpleados, SolicitudesTransportes
from .forms import SolicitudForm
from django.contrib.auth.decorators import login_required
import re

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                #VALIDACIONES

                if validarUsername(request.POST['username']):
                    if Cliente.objects.filter(username=request.POST['username']):
                        return render(request, 'signup.html', {
                            'form': UserCreationForm,
                            'error': "El nombre de usuario ya pertenece a una cuenta existente"
                        })
                else:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': "El nombre de usuario puede contener solo numeros o letras"
                    })

                if Cliente.objects.filter(email=request.POST['email']):
                    return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El correo electrónico ya pertenece a una cuenta existente"
                })

                longitud = len(request.POST['dni'])
                if longitud <= 8:
                    if Cliente.objects.filter(dni=request.POST['dni']):
                        return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': "El dni ya pertenece a una cuenta existente"
                    })
                else:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': "El dni debe tener hasta 8 cifras"
                    })
                

                id_estado_cliente = request.POST.get('idEstadoCliente', None)

                cliente = Cliente.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'], 
                    password=request.POST['password1'], 
                    email=request.POST['email'], 
                    dni=request.POST['dni'],
                    telefono=request.POST['telefono'],
                    idEstadoCliente=EstadosCliente.objects.get(id=id_estado_cliente),
                    puntos=0
                    )
                cliente.save()
                login(request, cliente)
                return redirect('solicitudes')
            except IntegrityError:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': "Ha ocurrido un error al guardar el usuario"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Las claves no coinciden"
        })

def validarUsername(cadena):
    regex = r'^[a-zA-Z0-9]+$'
    return bool(re.match(regex,cadena))

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "El usuario o la contraseña son incorrectos"
            })
        else:
            login(request, user)
            return redirect('solicitudes')

@login_required
def solicitudes(request):
    solicitudes = Solicitud.objects.all()

    for solicitud in solicitudes:
        solicitud.fechaTrabajo = solicitud.fechaTrabajo.strftime("%d/%m/%Y")
        solicitud.fechaSolicitud = solicitud.fechaSolicitud.strftime(
            "%d/%m/%Y")
    return render(request, 'solicitudes.html', {
        'solicitudes': solicitudes
    })


@login_required
def crear_solicitud(request):
    if request.method == 'GET':
        return render(request, 'crear_solicitud.html', {
            'form': SolicitudForm
        })
    else:
        try:
            form = SolicitudForm(request.POST)
            print(request.POST)
            new_sol = form.save(commit=False)
            new_sol.user = request.user
            new_sol.save()
            return redirect('solicitudes')
        except:
            return render(request, 'crear_solicitud.html', {
                'form': SolicitudForm,
                'error': "Por favor controle que los datos sean validos"
            })


@login_required
def solicitud_detalle(request, solicitud_id):
    if request.method == 'GET':
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
        solicitud.estados = solicitud.estados[int(solicitud.estado)][1]
        fechaTrabajo = solicitud.fechaTrabajo
        solicitud.fechaTrabajo = fechaTrabajo.strftime('%Y/%m/%d').replace('/','-')
        form = SolicitudForm(instance=solicitud)
        return render(request, 'solicitud_detalle.html', {
            'solicitud': solicitud,
            'form': form
        })
    else:
        try:
            solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
            form = SolicitudForm(request.POST, instance=solicitud)
            form.save()
            return redirect('solicitudes')
        except:
            solicitud.estados = solicitud.estados[int(solicitud.estado)][1]
            fechaTrabajo = solicitud.fechaTrabajo
            solicitud.fechaTrabajo = fechaTrabajo.strftime('%d/%m/%Y')
            form = SolicitudForm(instance=solicitud)
            return render(request, 'solicitud_detalle.html', {
                'solicitud': solicitud,
                'form': form,
                'error': 'Error al actualizar la solicitud'
            })


@login_required
def solicitud_eliminar(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    if request.method == 'POST':
        solicitud.delete()
    return redirect('solicitudes')


@login_required
def signout(request):
    logout(request)
    return redirect('home')
