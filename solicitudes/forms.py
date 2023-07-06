from django.forms import ModelForm
from .models import Solicitud
from django import forms


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['desde', 'hasta', 'fechaTrabajo', 'detalles']
        widgets = {
            'title': forms.
        }
