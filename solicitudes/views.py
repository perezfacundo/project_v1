from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import SolicitudForm
from .models import Estado, Solicitud
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('solicitudes')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El nombre de usuario ya existe"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Las claves no coinciden"
        })


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
            new_sol = form.save(commit=False)
            new_sol.fechaTrabajo = request.POST['fechaTrabajo']
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
        solicitud.fechaTrabajo = fechaTrabajo.strftime('%d/%m/%Y')
        form = SolicitudForm(instance=solicitud)
        return render(request, 'solicitud_detalle.html', {
            'solicitud': solicitud,
            'form': form
        })
    else:
        try:
            solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
            #fechaT = request.POST['fechaTrabajo']
            # request.POST['fechaTrabajo'] = datetime.strptime(fechaT, 'Y%/%m/%d')
            form = SolicitudForm(request.POST, instance=solicitud)
            form.save()
            return redirect('solicitudes')
        except ValueError:
            fecha = solicitud.fechaTrabajo
            solicitud.fechaTrabajo = fecha.strftime('%d/%m/%Y')
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
