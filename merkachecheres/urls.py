from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path




urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('publicar/', views.publicar, name='publicar'),
    
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('completardatos/', views.completardatos, name='completardatos'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cliente_dashboard/', views.cliente_dashboard, name='cliente_dashboard'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


