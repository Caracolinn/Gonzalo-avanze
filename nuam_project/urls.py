# nuam_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('login/', auth_views.LoginView.as_view(template_name='calificaciones/login.html'), name='login'),
    
    # --- ¡LÍNEA MODIFICADA! ---
    # Le decimos que también acepte 'get' para cerrar sesión
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['post', 'get', 'options']), name='logout'),

    path('calificaciones/', include('calificaciones.urls')),
]