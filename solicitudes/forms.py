from django.forms import ModelForm
from .models import Solicitud

class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['desde', 'hasta', 'fechaTrabajo', 'detalles']