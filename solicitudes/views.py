from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from .models import Usuario, EstadosCliente, Cliente, EstadosEmpleado, Empleado, TiposUsuario, EstadosSolicitud, Solicitud, EstadosVehiculo, Vehiculo, SolicitudesEmpleados, SolicitudesVehiculos
from django.contrib.auth.decorators import login_required
import re
import requests
from datetime import datetime
from django.core import serializers
from django.forms.models import model_to_dict
import json

# VISTAS AUTENTICACION


def home(request):
    logout(request)
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                # VALIDACIONES

                if validarUsername(request.POST['username']):
                    if Usuario.objects.filter(username=request.POST['username']):
                        return render(request, 'signup.html', {
                            'error': "El nombre de usuario ya pertenece a una cuenta existente"
                        })
                else:
                    return render(request, 'signup.html', {
                        'error': "El nombre de usuario puede contener solo numeros o letras"
                    })

                if Usuario.objects.filter(email=request.POST['email']):
                    return render(request, 'signup.html', {
                        'error': "El correo electrónico ya pertenece a una cuenta existente"
                    })

                longitud = len(request.POST['dni'])
                if longitud <= 8:
                    if Usuario.objects.filter(dni=request.POST['dni']):
                        return render(request, 'signup.html', {
                            'error': "El dni ya pertenece a una cuenta existente"
                        })
                else:
                    return render(request, 'signup.html', {
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
                    id_tipo_usuario=TiposUsuario.objects.get(
                        id=id_tipo_usuario),
                    fecha_nac=request.POST['fecha_nac'],
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

        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

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
def signout(request):
    logout(request)
    return redirect('home')


# VISTAS SOLICITUDES

@login_required
def solicitudes(request):

    return render(request, 'solicitudes.html')


def solicitudes_listado(request):

    objUsuario = Usuario.objects.get(username=request.session["username"])
    usuario = objUsuario.to_dict()

    if objUsuario.id_tipo_usuario.descripcion == "Cliente":
        solicitudes = Solicitud.objects.filter(cliente_id=objUsuario.id)
    else:
        solicitudes = Solicitud.objects.all()

    solicitudes_data = [solicitud.to_dict() for solicitud in solicitudes]

    objEstados = EstadosSolicitud.objects.values()
    estados = list(objEstados)

    data = {
        'solicitudes': solicitudes_data,
        'estados': estados,
        'usuario': usuario
    }
    return JsonResponse(data, safe=False)


@login_required
def solicitudes_crear(request):
    if request.method == 'GET':
        return render(request, 'solicitudes_crear.html')
    else:
        try:
            id_estado_solicitud = request.POST.get('id_estado_solicitud', None)

            solicitud = Solicitud.objects.create(
                objetos_a_transportar=request.POST['objetos_a_transportar'],
                detalles=request.POST['detalles'],

                direccion_desde=request.POST['direccion_desde'],
                latitud_desde=request.POST['latitud_desde'],
                longitud_desde=request.POST['longitud_desde'],

                direccion_hasta=request.POST['direccion_hasta'],
                latitud_hasta=request.POST['latitud_hasta'],
                longitud_hasta=request.POST['longitud_hasta'],
                pago_faltante=0,
                devolucion="",
                id_estado_solicitud=EstadosSolicitud.objects.get(
                    id=id_estado_solicitud),
                fecha_trabajo=request.POST['fecha_trabajo'],
                cliente_id=Cliente.objects.get(
                    username=request.user.username)
            )

            solicitud.save()

            return redirect('solicitudes')
        except Exception as e:
            if e == "Cliente matching query does not exist.":
                print("Error en solicitudes_crear:", e)
                return render(request, 'solicitudes_crear.html', {
                    'error': "Usted no se encuentra hablitado para crear una solicitud."
                })
            else:
                print("Error en solicitudes_crear:", e)
                return render(request, 'solicitudes_crear.html', {
                    'error': "No ha sido posible guardar la solicitud."
                })


@login_required
def solicitud_detalle(request, solicitud_id):

    tipo_usuario = Usuario.objects.get(username=request.user.username)

    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    estados = EstadosSolicitud.objects.all()

    lista_empleados_disponibles = list(
        Empleado.objects.filter(id_estado_empleado=1))
    lista_empleados_asignados = [
        sel.id_empleado for sel in SolicitudesEmpleados.objects.filter(id_solicitud=solicitud_id)]
    lista_vehiculos_disponibles = list(
        Vehiculo.objects.filter(id_estado_vehiculo=1))
    lista_vehiculos_asignados = [
        sel.id_vehiculo for sel in SolicitudesVehiculos.objects.filter(id_solicitud=solicitud_id)]

    if request.method == 'GET':
        return render(request, 'solicitud_detalle.html', {
            'solicitud': solicitud,
            'estados': estados,
            'lista_empleados_disponibles': lista_empleados_disponibles,
            'lista_empleados_asignados': lista_empleados_asignados,
            'lista_vehiculos_disponibles': lista_vehiculos_disponibles,
            'lista_vehiculos_asignados': lista_vehiculos_asignados
        })
    elif request.method == 'POST':
        form_data = request.POST.copy()
        form_data.pop('csrfmiddlewaretoken', None)

        empleados_asignados = form_data.getlist('empleados')
        vehiculos_asignados = form_data.getlist('vehiculos')

        # 1: Actualizar los datos modificados de la solicitud
        resultado_solicitud = actualizar_solicitud(solicitud, form_data)

        resultado_empleados = True
        resultado_vehiculos = True

        if tipo_usuario.id_tipo_usuario.id != 1:
            # 2: Actualizar los empleados asignados al viaje
            resultado_empleados = actualizar_empleados_asignados(
                solicitud, empleados_asignados)

            # 3: Actualizar los vehiculos asignados al viaje
            resultado_vehiculos = actualizar_vehiculos_asignados(
                solicitud, vehiculos_asignados)

        if resultado_solicitud and resultado_empleados and resultado_vehiculos:
            return redirect('solicitudes')
        else:
            error = ""
            if resultado_solicitud is False:
                error = "No se pudo actualizar la solicitud"
            elif resultado_empleados is False:
                error = "No se pudo actualizar la asignacion de empleados a la solicitud"
            elif resultado_vehiculos is False:
                error = "No se pudo actualizar la asignacion de vehiculos a la solicitud"

            return render(request, 'solicitud_detalle.html', {
                'solicitud': solicitud,
                'estados': estados,
                'lista_empleados_disponibles': lista_empleados_disponibles,
                'lista_empleados_asignados': lista_empleados_asignados,
                'lista_vehiculos_disponibles': lista_vehiculos_disponibles,
                'lista_vehiculos_asignados': lista_vehiculos_asignados,
                'error': error
            })


@transaction.atomic
def actualizar_solicitud(solicitud, form_data):
    try:
        for campo, nuevo_valor in form_data.items():
            if campo == "id_estado_solicitud":
                nuevo_estado = EstadosSolicitud.objects.get(id=nuevo_valor)
                if solicitud.id_estado_solicitud != nuevo_estado:
                    solicitud.id_estado_solicitud = nuevo_estado
            elif campo == "objetos_a_transportar":
                solicitud.objetos_a_transportar = nuevo_valor
            elif campo == "detalles":
                solicitud.detalles = nuevo_valor
            elif campo == "direccion_desde":
                solicitud.direccion_desde = nuevo_valor
            elif campo == "direccion_hasta":
                solicitud.direccion_hasta = nuevo_valor
            elif campo == "calificacion":
                solicitud.calificacion = nuevo_valor
            elif campo == "devolucion":
                solicitud.devolucion = nuevo_valor

        solicitud.save()
        return True
    except Exception as e:
        print("Error al actualizar_solicitud", e)
        return False


@transaction.atomic
def actualizar_empleados_asignados(solicitud, lista_empleados_asignados):

    try:

        # Eliminar registros de empleados deseleccionados
        empleados_solicitud = SolicitudesEmpleados.objects.filter(
            id_solicitud=solicitud)
        for empleado_relacion in empleados_solicitud:
            if str(empleado_relacion.id_empleado_id) not in lista_empleados_asignados:
                empleado_relacion.delete()

        # Agregar registros para empleados seleccionados
        for empleado_id in lista_empleados_asignados:
            if not SolicitudesEmpleados.objects.filter(id_solicitud=solicitud, id_empleado_id=empleado_id).exists():
                empleado_relacion = SolicitudesEmpleados(
                    id_solicitud=solicitud, id_empleado_id=empleado_id)
                empleado_relacion.save()

        return True
    except Exception as e:
        print("Error al actualizar asignacion de empleados", e)
        return False


@transaction.atomic
def actualizar_vehiculos_asignados(solicitud, lista_vehiculos_asignados):
    try:
        # Eliminar registros de vehiculos deselecciondos
        vehiculos_solicitud = SolicitudesVehiculos.objects.filter(
            id_solicitud=solicitud)
        for vehiculo_relacion in vehiculos_solicitud:
            if str(vehiculo_relacion.id_vehiculo_id) not in lista_vehiculos_asignados:
                vehiculo_relacion.delete()

        # Agregar registros para vehiculos seleccionados
        for vehiculo_id in lista_vehiculos_asignados:
            if not SolicitudesVehiculos.objects.filter(id_solicitud=solicitud, id_vehiculo_id=vehiculo_id).exists():
                vehiculo_relacion = SolicitudesVehiculos(
                    id_solicitud=solicitud, id_vehiculo_id=vehiculo_id)
                vehiculo_relacion.save()

        return True
    except Exception as e:
        print("Error al actualzar asignacion de vehiculos", e)
        return False


@login_required
def solicitud_eliminar(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    solicitud.delete()
    return redirect('solicitudes')


@login_required
def solicitud_calificar(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

    if request.method == 'GET':
        return render(request, 'solicitud_calificar.html', {
            'solicitud_id': solicitud_id
        })
    elif request.method == 'POST':

        form_data = request.POST.copy()
        form_data.pop('csrfmiddlewaretoken', None)

        resultado_solicitud = actualizar_solicitud(solicitud, form_data)

        if resultado_solicitud:
            return redirect('solicitudes')
        else:
            error = "No se pudo guardar los datos"

        return render(request, 'solicitud_calificar.html', {
            'solicitud': solicitud,
            'error': error
        })

@login_required
def solicitudes_reportes(request):
    

# VISTAS EMPLEADOS

@login_required
def empleados(request):
    empleados = Empleado.objects.all()
    try:

        return render(request, 'empleados.html', {
            'empleados': empleados
        })
    except Exception as e:
        print("Error en empleados:", e)
        return render(request, 'empleados.html', {
            'error': "Ha ocurrido un error al listar los empleados"
        })


@login_required
def empleados_crear(request):
    if request.method == 'GET':
        return render(request, 'empleados_crear.html')
    else:
        try:

            # VALIDACIONES
            if validarUsername(request.POST['username']):
                if Usuario.objects.filter(username=request.POST['username']):
                    return render(request, 'signup.html', {
                        'error': "El nombre de usuario ya pertenece a una cuenta existente"
                    })
            else:
                return render(request, 'signup.html', {
                    'error': "El nombre de usuario puede contener solo numeros o letras"
                })

            if Usuario.objects.filter(email=request.POST['email']):
                return render(request, 'signup.html', {
                    'error': "El correo electrónico ya pertenece a una cuenta existente"
                })

            longitud = len(request.POST['dni'])
            if longitud <= 8:
                if Usuario.objects.filter(dni=request.POST['dni']):
                    return render(request, 'signup.html', {
                        'error': "El dni ya pertenece a una cuenta existente"
                    })
            else:
                return render(request, 'signup.html', {
                    'error': "El dni debe tener hasta 8 cifras"
                })

            id_estado_empleado = request.POST.get(
                'id_estado_empleado', None)
            id_tipo_usuario = request.POST.get(
                'id_tipo_usuario', None)

            empleado = Empleado.objects.create_user(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                username=request.POST['username'],
                password=request.POST['last_name'] + "-e",
                email=request.POST['email'],
                dni=request.POST['dni'],
                telefono=request.POST['telefono'],
                fecha_nac=request.POST['fecha_nac'],
                tipo_carnet=request.POST['tipo_carnet'],
                ausencias=0,
                is_staff=1,
                id_estado_empleado=EstadosEmpleado.objects.get(
                    id=id_estado_empleado),
                id_tipo_usuario=TiposUsuario.objects.get(
                    id=id_tipo_usuario)
            )
            empleado.save()
            return redirect('empleados')
        except Exception as e:
            print("Error en empleados_crear:", e)
            return render(request, 'empleados_crear.html', {
                'error': "Ocurrio un error al registrar el empleado."
            })


@login_required
def empleado_detalle(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    estados = EstadosEmpleado.objects.all()

    if request.method == 'GET':

        return render(request, 'empleado_detalle.html', {
            'empleado': empleado,
            'estados': estados
        })
    else:  # POST

        r_post = request.POST.copy()
        r_post.pop('csrfmiddlewaretoken', None)

        resultado = actualizar_empleado(r_post, empleado_id)

        if resultado:
            return redirect('empleados')
        else:
            return redirect('empleado_detalle.html')


def actualizar_empleado(r_post, empleado_id):
    try:
        empleado = Empleado.objects.get(id=empleado_id)
    except Empleado.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():

        try:
            if campo == "id_estado_empleado":
                nuevo_estado = EstadosEmpleado.objects.get(id=nuevo_valor)
                if empleado.id_estado_empleado != nuevo_estado:
                    empleado.id_estado_empleado = nuevo_estado

            elif getattr(empleado, campo) != nuevo_valor:
                setattr(empleado, campo, nuevo_valor)
        except Exception as e:
            print("Error en empleado_detalle:", e)

    if any(getattr(empleado, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()):
        empleado.save()
    return True


@login_required
def empleado_eliminar(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    if request.method == 'POST':
        empleado.delete()
    return redirect('empleados')


# VISTAS VEHICULOS

@login_required
def vehiculos(request):
    try:
        vehiculos = Vehiculo.objects.all()
        print(vehiculos)
        return render(request, 'vehiculos.html', {
            'vehiculos': vehiculos
        })
    except Exception as e:
        print("Error en vehiculos:", e)
        return render(request, 'vehiculos.html', {
            'error': "Ha ocurrido un error al listar los vehiculos"
        })


@login_required
def vehiculos_crear(request):
    vehiculo = ""
    if request.method == 'GET':
        return render(request, 'vehiculos_crear.html')
    else:
        try:

            id_estado_vehiculo = request.POST.get('id_estado_vehiculo', None)
            vehiculo = Vehiculo.objects.create(
                dominio=request.POST['dominio'],
                marca=request.POST['marca'],
                nombre=request.POST['nombre'],
                modelo=request.POST['modelo'],
                capacidad=request.POST['capacidad'],
                id_estado_vehiculo=EstadosVehiculo.objects.get(
                    id=id_estado_vehiculo)
            )

            vehiculo.save()

            return redirect('vehiculos')
        except Exception as e:  # revisar bug
            if e == "UNIQUE constraint failed: solicitudes_vehiculo.dominio":
                print("Error en patente ", e)
                return render(request, 'vehiculos_crear.html', {
                    'vehiculo': vehiculo,
                    'error': "El dominio ya pertenece a otro vehiculo registrado"
                })
            else:
                print("Error en vehiculos_crear: ", e)
                return render(request, 'vehiculos_crear.html', {
                    'vehiculo': vehiculo,
                    'error': "No se pudo registrar el vehiculo"
                })


@login_required
def vehiculo_detalle(request, vehiculo_id):
    if request.method == 'GET':
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        estados = EstadosVehiculo.objects.all()

        return render(request, 'vehiculo_detalle.html', {
            'vehiculo': vehiculo,
            'estados': estados
        })
    else:  # POST

        r_post = request.POST.copy()
        r_post.pop('csrfmiddlewaretoken', None)
        resultado = actualizar_vehiculo(r_post, vehiculo_id)

        if resultado:
            return redirect('vehiculos')
        else:
            return render(request, 'vehiculo_detalle.html', {
                'error': "Ha ocurrido un error al actualizar los datos del vehiculo"
            })


def actualizar_vehiculo(r_post, vehiculo_id):
    try:
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    except Vehiculo.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():
        try:
            if campo == 'id_estado_vehiculo':
                nuevo_estado = EstadosVehiculo.objects.get(id=nuevo_valor)
                if vehiculo.id_estado_vehiculo != nuevo_estado:
                    vehiculo.id_estado_vehiculo = nuevo_estado
            elif getattr(vehiculo, campo) != nuevo_valor:
                setattr(vehiculo, campo, nuevo_valor)
        except Exception as e:
            print("Error en actualizar vehiculo: ", e)

    if any(getattr(vehiculo, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()):
        vehiculo.save()
    return True


@login_required
def vehiculo_eliminar(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
    return redirect('vehiculos')

# VISTAS CLIENTES


@login_required
def clientes_crear(request):
    print("hola")


@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    try:
        return render(request, 'clientes.html', {
            'clientes': clientes
        })
    except Exception as e:
        print("Error en clientes: ", e)
        return render(request, 'clientes.html', {
            'error': "Ha ocurrido un error al listar los clientes"
        })


@login_required
def cliente_detalle(request, cliente_id):
    if request.method == 'GET':
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        estados = EstadosCliente.objects.all()

        return render(request, 'cliente_detalle.html', {
            'cliente': cliente,
            'estados': estados
        })
    else:
        print(request)
        r_post = request.POST.copy()
        print(r_post)
        r_post.pop('csrfmiddlewaretoken', None)
        print(r_post)

        resultado = actualizar_cliente(r_post, cliente_id)
        print(resultado)

        if resultado:
            return redirect('clientes')
        else:
            return render(request, 'cliente_detalle.html', {
                'error': "Ha ocurrido un error al actualizar los datos del cliente"
            })


def actualizar_cliente(r_post, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():
        try:
            if campo == 'id_estado_cliente':
                nuevo_estado = EstadosCliente.objects.get(id=nuevo_valor)
                if cliente.id_estado_cliente != nuevo_estado:
                    cliente.id_estado_cliente = nuevo_estado
            elif getattr(cliente, campo) != nuevo_valor:
                setattr(cliente, campo, nuevo_valor)
        except Exception as e:
            print("Error en actualizar cliente: ", e)

    if any(getattr(cliente, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()):
        cliente.save()
    return True


@login_required
def cliente_eliminar(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
    return redirect('clientes')


def objetos_a_json(objeto_o_lista):
    if isinstance(objeto_o_lista, list):
        json_resultado = [objeto.__dict__ for objeto in objeto_o_lista]
    else:
        json_resultado = objeto_o_lista.__dict__

    return json.dumps(json_resultado, indent=4)
