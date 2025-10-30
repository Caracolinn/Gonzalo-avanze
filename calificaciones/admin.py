# calificaciones/admin.py
from django.contrib import admin
from .models import CalificacionTributaria, Corredor

# --- CONFIGURACIÓN PARA EL MODELO CORREDOR ---
@admin.register(Corredor)
class CorredorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_corredor', 'activo')
    search_fields = ('nombre', 'codigo_corredor')

# --- CONFIGURACIÓN PARA EL MODELO CALIFICACIÓN TRIBUTARIA ---
@admin.register(CalificacionTributaria)
class CalificacionTributariaAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista principal
    list_display = ('instrumento', 'fecha', 'corredor', 'instrumento_no_inscrito', 'secuencia')
    
    # Habilita filtros en la barra lateral
    list_filter = ('corredor', 'tipo_sociedad', 'fecha', 'instrumento_no_inscrito')
    
    # Habilita un campo de búsqueda (incluyendo búsqueda por nombre del corredor)
    search_fields = ('instrumento', 'secuencia', 'corredor__nombre')

    # Organiza los campos del formulario en secciones
    fieldsets = (
        ('Datos de Identificación', {
            'fields': (
                'corredor', 
                'instrumento', 
                'instrumento_no_inscrito', 
                'fecha', 
                'secuencia', 
                'numero_dividendo', 
                'tipo_sociedad', 
                'valor_historico'
            )
        }),
        ('Factores Tributarios', {
            'classes': ('collapse',), # Esta sección aparecerá colapsada por defecto
            'fields': (
                ('factor_8', 'factor_9', 'factor_10'),
                ('factor_11', 'factor_12', 'factor_13'),
                ('factor_14', 'factor_15', 'factor_16'),
                ('factor_17', 'factor_18', 'factor_19'),
                ('factor_20', 'factor_21', 'factor_22'),
                ('factor_23', 'factor_24', 'factor_25'),
                ('factor_26', 'factor_27', 'factor_28'),
                ('factor_29', 'factor_30', 'factor_31'),
                ('factor_32', 'factor_33', 'factor_34'),
                ('factor_35', 'factor_36', 'factor_37'),
            )
        }),
    )