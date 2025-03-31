from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path




urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('registro/', views.registro, name='registro'),
    path('completardatos/', views.completardatos, name='completardatos'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


