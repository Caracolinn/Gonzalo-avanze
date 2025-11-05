# calificaciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mantenedor_calificaciones, name='mantenedor'),
    
    # Flujo de Ingreso
    path('ingresar/', views.ingresar_calificacion, name='ingresar_calificacion'),
    path('ingresar-montos/<int:calificacion_id>/', views.ingresar_montos, name='ingresar_montos'),
    
    # Flujo de Eliminación
    path('eliminar/<int:calificacion_id>/', views.eliminar_calificacion, name='eliminar_calificacion'),
    
    # Flujo de Modificación
    path('obtener/<int:calificacion_id>/', views.obtener_calificacion_json, name='obtener_calificacion_json'),
    path('modificar/<int:calificacion_id>/', views.modificar_calificacion, name='modificar_calificacion'),

    # Flujo de Guardado (Paso 3)
    path('guardar-factores/<int:calificacion_id>/', views.guardar_factores, name='guardar_factores'),
    
    # Flujo de Carga Masiva
    path('previsualizar-csv/', views.previsualizar_csv, name='previsualizar_csv'),
    path('upload/factores/', views.carga_masiva_factores, name='carga_masiva_factores'),
    path('upload/montos/', views.carga_masiva_montos, name='carga_masiva_montos'),
]