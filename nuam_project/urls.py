# nuam_project/urls.py
from django.contrib import admin
from django.urls import path, include # ¡Añade include!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Añade esta línea para conectar las URLs de tu aplicación
    path('calificaciones/', include('calificaciones.urls')),
]