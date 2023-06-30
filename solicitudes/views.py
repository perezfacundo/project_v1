from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import SolicitudForm
from .models import Estado, Solicitud
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


def solicitudes(request):
    return render(request, 'solicitudes.html')


def crear_solicitud(request):
    if request.method == 'GET':
        return render(request, 'crear_solicitud.html', {
            'form': SolicitudForm
        })
    else:
        try:
            form = SolicitudForm(request.POST)
            new_sol = form.save(commit=False)
            new_sol.user = request.user
            new_sol.save()
            return redirect('solicitudes')
        except:
            return render(request, 'crear_solicitud.html', {
                'form': SolicitudForm,
                'error': "Por favor controle que los datos sean validos"
            })


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
        print(request.POST)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "El usuario o la contraseña son incorrectos"
            })
        else:
            login(request, user)
            return redirect('solicitudes')
