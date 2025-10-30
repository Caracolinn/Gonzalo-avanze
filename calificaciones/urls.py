# calificaciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/factores/', views.carga_masiva_factores, name='carga_masiva_factores'),
    # --- NUEVA RUTA ---
    path('upload/montos/', views.carga_masiva_montos, name='carga_masiva_montos'),
]