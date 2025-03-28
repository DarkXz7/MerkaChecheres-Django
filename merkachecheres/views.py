from django.shortcuts import render
import random
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages


from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validar que los campos no estén vacíos
        if not full_name or not email or not username or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'registro.html')

        # Validar que el correo electrónico y el nombre de usuario sean únicos
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return render(request, 'registro.html')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return render(request, 'registro.html')

        # Crear el usuario y guardarlo en la base de datos
        try:
            usuario = Usuario(full_name=full_name, email=email, username=username, password=password)
            usuario.save()
            messages.success(request, "Cuenta creada exitosamente.")
            return redirect('index')  # Redirige al inicio
        except Exception as e:
            messages.error(request, f"Error al guardar el usuario: {e}")
            return render(request, 'registro.html')

    return render(request, 'registro.html')

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def completardatos(request):
    return render(request, "completardatos.html")

def index(request):
    #return HttpResponse("Index")
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def registro(request):
    return render(request, "registro.html")

def completardatos(request):
    return render(request, "completardatos.html")