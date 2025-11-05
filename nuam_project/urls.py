# nuam_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- ¡CAMBIO! ---
    # Ahora la raíz del sitio ('') es la página de Login
    path('', auth_views.LoginView.as_view(template_name='calificaciones/login.html'), name='login'),
    
    path('admin/', admin.site.urls),
    
    # La ruta de logout se mantiene
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['post', 'get', 'options']), name='logout'),

    # La ruta de tu aplicación
    path('calificaciones/', include('calificaciones.urls')),
]