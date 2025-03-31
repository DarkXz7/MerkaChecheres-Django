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
            
            # Try to authenticate the newly created user
            try:
                q = Usuario.objects.get(email=email, password=password)
                # Autenticación: Creamos la variable de sesión
                request.session["pista"] = {
                    "id": q.id,
                    "rol": q.rol,
                    "nombre": q.full_name  # Changed from q.nombre to match the field name
                }
                messages.success(request, "Bienvenido!!")
                return redirect("index")
            except Usuario.DoesNotExist:
                request.session["pista"] = None
                messages.error(request, "Error en el autologin después del registro")
                return redirect('index')
        
        except Exception as e:
            messages.error(request, f"Error al guardar el usuario: {e}")
            return render(request, 'registro.html')
    return render(request, 'registro.html')
        
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verificar si el usuario existe en la base de datos
        try:
            usuario = Usuario.objects.get(email=email, password=password)
            # Crear una sesión para el usuario
            request.session["validar"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.full_name
            }
            
            # Redirigir según el rol del usuario
            if usuario.rol == 1:  # Admin
                return redirect('admin_dashboard')
            elif usuario.rol == 2:  # Cliente
                return redirect('cliente_dashboard')
            elif usuario.rol == 3:  # Vendedor
                return redirect('vendedor_dashboard')

        except Usuario.DoesNotExist:
            # Si el usuario no existe, mostrar un mensaje de error
            messages.error(request, "Correo electrónico o contraseña incorrectos.")
            return render(request, 'login.html')
    return render(request, 'login.html')


def admin_dashboard(request):
    return render(request, 'admin.html')




def index(request):
    return render(request, "index.html")

def adminlogin(request):
    return render(request, "adminlogin.html")

def completardatos(request):
    return render(request, "completardatos.html")