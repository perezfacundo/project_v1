from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Usuario, EstadosCliente, Cliente, EstadosEmpleadoCalle, EmpleadoCalle, EstadosEmpleadoAdmnistrativo, EmpleadoAdministrativo, tipo_usuario, EstadosSolicitud, Solicitud, EstadosTransporte, Transporte, SolicitudesEmpleados, SolicitudesTransportes
from django.contrib.auth.decorators import login_required
import re
import requests
from datetime import datetime
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
                # VALIDACIONES

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

                id_estado_cliente = request.POST.get('id_estado_cliente', None)
                id_tipo_usuario = request.POST.get('id_tipo_usuario', None)

                cliente = Cliente.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    dni=request.POST['dni'],
                    telefono=request.POST['telefono'],
                    id_estado_cliente=EstadosCliente.objects.get(
                        id=id_estado_cliente),
                    id_tipo_usuario=tipo_usuario.objects.get(
                        id=id_tipo_usuario),
                    puntos=0
                )
                cliente.save()
                login(request, cliente)
                return redirect('solicitudes')
            except Exception as e:
                print("Error en signup:", e)
                return render(request, 'signup.html', {
                'error': "Ocurrio un error al registrar el usuario."
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Las claves no coinciden"
        })


def validarUsername(cadena):
    regex = r'^[a-zA-Z0-9]+$'
    return bool(re.match(regex, cadena))


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "El usuario o la contraseña son incorrectos"
            })
        else:
            login(request, user)
            request.session['username'] = user.username
            return redirect('solicitudes')


@login_required
def solicitudes(request):
    solicitudes = Solicitud.objects.all()

    try:
        for solicitud in solicitudes:
            solicitud.fecha_trabajo = solicitud.fecha_trabajo.strftime(
                "%d/%m/%Y")
            solicitud.fecha_solicitud = solicitud.fecha_solicitud.strftime(
                "%d/%m/%Y")
        return render(request, 'solicitudes.html', {
            'solicitudes': solicitudes
        })
    except Exception as e:
        print("Error en solicitudes:", e)
        return render(request, 'solicitudes.html', {
            'error': "Ha ocurrido un error al listar las solicitudes"
        })

@login_required
def solicitudes_crear(request):
    if request.method == 'GET':
        return render(request, 'crear_solicitud.html')
    else:
        try:
            print(request.POST)

            id_estado_solicitud = request.POST.get('id_estado_solicitud', None)
                        
            solicitud = Solicitud.objects.create(
                objetos_a_transportar=request.POST['objetos_a_transportar'],
                detalles=request.POST['detalles'],
                direccion_desde=request.POST['direccion_desde'],
                direccion_hasta=request.POST['direccion_hasta'],
                coordenadas_desde="prueba",
                coordenadas_hasta="prueba",
                pago_faltante=0,
                devolucion="",
                id_estado_solicitud=EstadosSolicitud.objects.get(id=id_estado_solicitud),
                fecha_trabajo=request.POST['fecha_trabajo'],
                cliente_id = Cliente.objects.get(username = request.session['username'])
            )

            solicitud.save()

            return redirect('solicitudes')
        except Exception as e:
            if e == "Cliente matching query does not exist.":
                print("Error en solicitudes_crear:", e)
                return render(request, 'crear_solicitud.html', {
                'error': "Usted no se encuentra hablitado para crear una solicitud."
                })
            else: 
                print("Error en solicitudes_crear:", e)
                return render(request, 'crear_solicitud.html', {
                'error': "No ha sido posible guardar la solicitud."
                })


@login_required
def solicitud_detalle(request, solicitud_id):
    if request.method == 'GET':
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

        estados = EstadosSolicitud.objects.all()
        return render(request, 'solicitud_detalle.html', {
            'solicitud': solicitud,
            'estados': estados
        })
    else: #POST
        r_post = request.POST.copy()
        r_post.pop('csrfmiddlewaretoken', None)
        
        resultado = actualizar_solicitud(r_post, solicitud_id)
        
        if resultado:
            return redirect('solicitudes')
        else:
            return render(request, 'solicitud_detalle.html', {
                'error': "Ha ocurrido un error al procesar la solicitud"
            })


def actualizar_solicitud(r_post, solicitud_id):
    try:
        solicitud = Solicitud.objects.get(id=solicitud_id)
    except Solicitud.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():
        if campo == "id_estado_solicitud":
            nuevo_estado = EstadosSolicitud.objects.get(id=nuevo_valor)
            if solicitud.id_estado_solicitud != nuevo_estado:
                solicitud.id_estado_solicitud = nuevo_estado
        
        elif getattr(solicitud, campo) != nuevo_valor:
            setattr(solicitud, campo, nuevo_valor)

        if any(getattr(solicitud, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()):
            solicitud.save()
    return True

@login_required
def empleados():
    empleados_calle = EmpleadoCalle.objects.all()
    empleados_administrativos = EmpleadoAdministrativo.objects.all()

    return render('empleados.html', {
        'empleados_calle': empleados_calle,
        'empleados_administrativos': empleados_administrativos
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
