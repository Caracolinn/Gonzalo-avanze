# calificaciones/forms.py
from django import forms
from .models import Corredor, CalificacionTributaria

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
        super().__init__(*args, **kwargs)
        self.fields['corredor'].choices = [
            (c.id, c.nombre) for c in Corredor.objects.filter(activo=True)
        ]

# ... (después de la clase IngresoMontosForm)

# --- NUEVO FORMULARIO PARA LA MODAL "PASO 3" (FACTORES) ---
class IngresoFactoresForm(forms.Form):
    # Creamos un campo dinámico para cada factor, del 8 al 37
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(8, 38):
            self.fields[f'factor_{i}'] = forms.DecimalField(
                label=f'Factor {i}',
                required=False,
                initial=0.0,
                max_digits=9,
                decimal_places=8,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'})
            )
            
# ... (después de la clase IngresoBasicoForm)

# --- NUEVO FORMULARIO PARA LA MODAL "INGRESAR MONTOS" (Paso 2) ---
class IngresoMontosForm(forms.Form):
    # Creamos un campo dinámico para cada monto, del 8 al 37
    # (Usamos 38 porque el rango no incluye el último número)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(8, 38):
            self.fields[f'monto_{i}'] = forms.DecimalField(
                label=f'Monto {i}',
                required=False,
                initial=0.0,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
            
# --- FORMULARIO PARA LOS FILTROS DEL MANTENEDOR ---
class FiltroCalificacionesForm(forms.Form):
    MERCADO_CHOICES = [('', 'Todos')] + CalificacionTributaria.TIPO_MERCADO_CHOICES
    ORIGEN_CHOICES = [('', 'Todos')] + CalificacionTributaria.ORIGEN_CHOICES
    
    tipo_mercado = forms.ChoiceField(
        choices=MERCADO_CHOICES,
        required=False,
        label="Mercado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    origen = forms.ChoiceField(
        choices=ORIGEN_CHOICES,
        required=False,
        label="Origen",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    periodo_comercial = forms.IntegerField(
        required=False,
        label="Periodo Comercial (Año)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2025'})
    )

# --- NUEVO FORMULARIO PARA LA VENTANA MODAL "INGRESAR" ---
class IngresoBasicoForm(forms.ModelForm):
    # Hacemos que la secuencia empiece en 10001
    secuencia = forms.IntegerField(
        initial=10001,
        min_value=10001,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # Hacemos que el dividendo empiece en 0
    numero_dividendo = forms.IntegerField(
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # Hacemos que el factor de actualización empiece en 0
    factor_actualizacion = forms.DecimalField(
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # Añadimos un campo para el año (periodo)
    periodo = forms.IntegerField(
        label="Año (Periodo)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False # Lo hacemos opcional
    )

    class Meta:
        model = CalificacionTributaria
        # Campos que pediste en la Historia de Usuario #2
        fields = [
            'tipo_mercado',
            'instrumento',
            'secuencia',
            'numero_dividendo',
            'fecha',
            'valor_historico',
            'descripcion_dividendo',
            'acogido_isfut',
            'factor_actualizacion',
            'periodo', # Este no está en el modelo, lo manejaremos en la vista
        ]
        widgets = {
            'tipo_mercado': forms.Select(attrs={'class': 'form-select'}),
            'instrumento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_historico': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion_dividendo': forms.TextInput(attrs={'class': 'form-control'}),
            'acogido_isfut': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }