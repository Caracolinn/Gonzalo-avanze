# calificaciones/forms.py
from django import forms

class CargaCSVForm(forms.Form):
    archivo_csv = forms.FileField(
        label='Seleccionar archivo CSV',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    corredor = forms.ChoiceField(
        label='Seleccionar Corredor',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        from .models import Corredor
        super().__init__(*args, **kwargs)
        # Obtenemos los corredores activos y los ponemos como opciones
        self.fields['corredor'].choices = [
            (c.id, c.nombre) for c in Corredor.objects.filter(activo=True)
        ]