# calificaciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mantenedor_calificaciones, name='mantenedor'),
    path('ingresar/', views.ingresar_calificacion, name='ingresar_calificacion'),
    
    # --- NUEVA RUTA para el formulario de montos (Paso 2) ---
    # Usamos <int:calificacion_id> para saber a qué registro añadirle los montos
    path('ingresar-montos/<int:calificacion_id>/', views.ingresar_montos, name='ingresar_montos'),
    
    path('upload/factores/', views.carga_masiva_factores, name='carga_masiva_factores'),
    path('upload/montos/', views.carga_masiva_montos, name='carga_masiva_montos'),
]