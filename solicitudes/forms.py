from django.forms import ModelForm
from django import forms
from .models import Solicitud


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['desde', 'hasta', 'fechaTrabajo', 'detalles']
        widgets = {
            'desde': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el punto de partida'}),
            'hasta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el punto de destino'}),
            'fechaTrabajo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique la fecha del trabajo'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Aquí puede dejar detalles del viaje en caso de que los haya'}),
        }
