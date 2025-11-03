# calificaciones/admin.py
from django.contrib import admin
from .models import CalificacionTributaria, Corredor

@admin.register(Corredor)
class CorredorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_corredor', 'activo')
    search_fields = ('nombre', 'codigo_corredor')

@admin.register(CalificacionTributaria)
class CalificacionTributariaAdmin(admin.ModelAdmin):
    list_display = (
        'instrumento', 
        'fecha', 
        'corredor', 
        'tipo_mercado', 
        'fuente_ingreso', # NUEVO
        'fecha_modificacion', # NUEVO
        'origen',
    )
    
    list_filter = (
        'corredor', 
        'tipo_mercado', 
        'fuente_ingreso', # NUEVO
        'origen',
        'fecha_modificacion', # NUEVO
    )
    
    search_fields = ('instrumento', 'secuencia', 'corredor__nombre', 'descripcion_dividendo')

    fieldsets = (
        ('Datos de Identificación', {
            'fields': (
                'corredor', 
                'instrumento', 
                'instrumento_no_inscrito', 
                'fecha',
                'tipo_mercado',
                'descripcion_dividendo',
                'acogido_isfut',
                'origen',
                'factor_actualizacion',
                'fuente_ingreso', # NUEVO
                'secuencia', 
                'numero_dividendo', 
                'tipo_sociedad', 
                'valor_historico'
            )
        }),
        ('Fechas de Auditoría', { # NUEVA SECCIÓN
            'classes': ('collapse',),
            'fields': ('fecha_modificacion',)
        }),
        ('Factores Tributarios', {
            'classes': ('collapse',),
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
    
    # Hacemos que los campos de auditoría sean de solo lectura
    readonly_fields = ('fecha_modificacion',)