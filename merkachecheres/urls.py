from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path




urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('publicar/', views.publicar, name='publicar'),
    path('producto/<int:producto_id>/', views.producto, name='producto'),
    path('producto/', views.producto, name='producto'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('completardatos/', views.completardatos, name='completardatos'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cliente_dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('cambio-contrasena/', views.solicitar_cambio_contrasena, name='solicitar_cambio_contrasena'),
    path('restablecer-contrasena/', views.restablecer_contrasena, name='restablecer_contrasena'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)