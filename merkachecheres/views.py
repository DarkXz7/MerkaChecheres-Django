from django.shortcuts import render, redirect
from .models import Usuario
from .models import Producto, ImagenProducto
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

def registro(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        telefono = request.POST.get('telefono')
        departamento = request.POST.get('departamento')
        direccion = request.POST.get('direccion')
        municipio = request.POST.get('municipio', 'Sin municipio')
        ciudad = request.POST.get('ciudad')
        
        
        
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
            usuario = Usuario(
                full_name=full_name,
                email=email, 
                username=username, 
                password=password,
                telefono=telefono, 
                departamento=departamento, 
                direccion=direccion, 
                municipio=municipio, 
                ciudad=ciudad
                )
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
                return redirect('index')  # Redirige a la vista `index`
            elif usuario.rol == 3:  # Vendedor
                return redirect('vendedor_dashboard')

        except Usuario.DoesNotExist:
            messages.error(request, "Correo electrónico o contraseña incorrectos.")
            return render(request, 'login.html')
    return render(request, 'login.html')


from decimal import Decimal, InvalidOperation
import re

def publicar(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagenes = request.FILES.getlist('imagen')  # Capturar múltiples imágenes
        marca = request.POST.get('marca')
        descuento = request.POST.get('descuento')
        dimensiones = request.POST.get('dimensiones')
        stock = request.POST.get('Stock')  # Obtener el valor de stock del formulario

        # Validar que no se suban más de 12 imágenes
        if len(imagenes) > 12:
            messages.error(request, "Solo puedes subir un máximo de 12 imágenes.")

        # Validar campos obligatorios
        if not titulo:
            messages.error(request, "El campo 'Título' es obligatorio.")
        if not precio:
            messages.error(request, "El campo 'Precio' es obligatorio.")
        if not categoria:
            messages.error(request, "El campo 'Categoría' es obligatorio.")
        if not descripcion:
            messages.error(request, "El campo 'Descripción' es obligatorio.")
        if not stock:
            messages.error(request, "El campo 'Stock' es obligatorio.")

        # Si hay errores, no continuar
        if len(list(messages.get_messages(request))) > 0:
            return render(request, 'publicarArticulo.html')

        try:
            # Convertir categoría a entero
            categoria = int(categoria)

            # Convertir precio a Decimal
            precio = Decimal(precio.replace(',', '').replace('.', '')) / 100

            # Procesar descuento (si existe)
            if descuento:
                descuento = Decimal(descuento.replace('%', '').strip())

            # Validar y convertir stock a entero
            try:
                stock = int(stock)
                if stock < 0:
                    raise ValueError("El stock no puede ser negativo.")
            except ValueError:
                messages.error(request, "El campo Stock debe ser un número entero válido.")
                return render(request, 'publicarArticulo.html')

            # Guardar producto
            producto = Producto(
                titulo=titulo,
                precio=precio,
                categoria=categoria,
                descripcion=descripcion,
                marca=marca,
                descuento=descuento,
                dimensiones=dimensiones,
                stock=stock  # Asignar el valor de stock
            )
            producto.save()

            # Guardar las imágenes relacionadas
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto publicado exitosamente.")
            return render(request, 'publicarArticulo.html', {'redirect': True})

        except InvalidOperation:
            messages.error(request, "Error: Ingrese un precio válido.")
            return render(request, 'publicarArticulo.html')

        except Exception as e:
            messages.error(request, f"Error al guardar el producto: {e}")
            return render(request, 'publicarArticulo.html')

    return render(request, 'publicarArticulo.html')


def solicitar_cambio_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificar si el correo existe en la base de datos
        try:
            usuario = Usuario.objects.get(email=email)
            # Guardar el email en la sesión para usarlo en la siguiente vista
            request.session['email_para_cambio'] = email
            messages.success(request, "Correo verificado. Ahora puedes restablecer tu contraseña.")
            return redirect('restablecer_contrasena')  # Redirige al formulario de restablecimiento
        except Usuario.DoesNotExist:
            messages.error(request, "El correo electrónico no está registrado.")
            return render(request, 'solicitar_cambio_contrasena.html')

    return render(request, 'solicitar_cambio_contrasena.html')


def restablecer_contrasena(request):
    # Verificar si el email está en la sesión
    email = request.session.get('email_para_cambio')
    if not email:
        messages.error(request, "No se ha verificado ningún correo electrónico.")
        return redirect('solicitar_cambio_contrasena')

    try:
        usuario = Usuario.objects.get(email=email)

        if request.method == 'POST':
            nueva_contrasena = request.POST.get('password')
            confirmar_contrasena = request.POST.get('confirm_password')

            # Validar que las contraseñas coincidan
            if nueva_contrasena != confirmar_contrasena:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, 'restablecer_contrasena.html')

            # Actualizar la contraseña del usuario
            usuario.password = (nueva_contrasena)  # Encripta la contraseña
            usuario.save()

            # Eliminar el email de la sesión
            del request.session['email_para_cambio']

            # Mostrar mensaje de éxito y redirigir al login
            messages.success(request, "Tu contraseña ha sido restablecida exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')

        return render(request, 'restablecer_contrasena.html')

    except Usuario.DoesNotExist:
        messages.error(request, "El correo electrónico no es válido.")
        return redirect('solicitar_cambio_contrasena')



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

def producto(request, producto_id):
    try:
        # Buscar el producto por su ID
        producto = Producto.objects.get(id=producto_id)
        imagenes = producto.imagenes.all()  # Obtener las imágenes relacionadas
    except Producto.DoesNotExist:
        # Si el producto no existe, redirigir al índice con un mensaje de error
        messages.error(request, "El producto no existe.")
        return redirect('index')

    return render(request, 'producto.html', {
        'producto': producto,
        'imagenes': imagenes,
    })

def producto_view(request):
    # Example context data
    context = {
        'producto': {
            'titulo': 'Sample Product',
        },
        'imagenes': [],  # Add your image data here
    }
    return render(request, 'producto.html', context)


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto.html', {'producto': producto})


def index(request):
    # Obtén todos los productos disponibles
    
    productos = Producto.objects.order_by('?')[:5] 
    
    # Verifica si hay una sesión activa
    sesion_activa = request.session.get('validar', None)
    
    return render(request, "index.html", {
        'productos': productos,
        'productos_count': productos.count(),
        
    })

def adminlogin(request):
    return render(request, "adminlogin.html")

def completardatos(request):
    return render(request, "completardatos.html")