from django.shortcuts import render, redirect
from .models import Usuario
from .models import Producto, ImagenProducto
from django.contrib import messages
from decimal import Decimal, InvalidOperation

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


def publicar(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagenes = request.FILES.getlist('imagen')  # Capturar múltiples imágenes

        if not titulo or not precio or not categoria or not descripcion:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'publicarArticulo.html')

        try:
            # Convertir categoría a entero
            categoria = int(categoria)

            # Formatear el precio eliminando caracteres no numéricos
            precio = precio.replace(',', '').replace('.', '')  # Quita separadores
            precio = Decimal(precio) / 100  # Divide entre 100 para obtener 2 decimales

            # Validar que el precio no sea muy grande
            if precio > Decimal('99999999.99'):
                messages.error(request, "El precio no puede superar 99,999,999.99.")
                return render(request, 'publicarArticulo.html')

            # Guardar producto
            producto = Producto(
                titulo=titulo,
                precio=precio,
                categoria=categoria,
                descripcion=descripcion
            )
            producto.save()

            # Guardar las imágenes relacionadas
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto publicado exitosamente.")
            return redirect('index')  # Redirigir al índice después de guardar

        except InvalidOperation:
            messages.error(request, "Error: Ingrese un precio válido.")
            return render(request, 'publicarArticulo.html')

        except Exception as e:
            messages.error(request, f"Error al guardar el producto: {e}")
            return render(request, 'publicarArticulo.html')

    return render(request, 'publicarArticulo.html')


def logout(request):
    # Elimina la sesión del usuario
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')



def admin_dashboard(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admin.html', {'usuarios': usuarios})
    
def cliente_dashboard(request):    
    return render(request, 'index.html')
def vendedor_dashboard(request):
    return render(request, 'vendedor.html')


def index(request):
    productos = Producto.objects.order_by('?')[:5]  # Obtiene los 5 primeros productos
    return render(request, "index.html", {'productos': productos})

def adminlogin(request):
    return render(request, "adminlogin.html")

def completardatos(request):
    return render(request, "completardatos.html")