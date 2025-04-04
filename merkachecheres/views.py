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


def publicar(request):
    if request.method == 'POST':
        print(f"Número de imágenes recibidas: {len(request.FILES.getlist('imagen'))}")  # Debug
        for img in request.FILES.getlist('imagen'):
            print(f"Imagen: {img.name} - Tamaño: {img.size} bytes")

            
        titulo = request.POST.get('titulo')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagenes = request.FILES.getlist('imagen')  # Obtener todas las imágenes
        marca = request.POST.get('marca')
        descuento = request.POST.get('descuento')
        dimensiones = request.POST.get('dimensiones')
        stock = request.POST.get('Stock')
        
        # Validaciones básicas
        if not all([titulo, precio, categoria, descripcion, stock]):
            messages.error(request, "Todos los campos obligatorios deben estar completos.")
            return render(request, 'publicarArticulo.html')

        try:
            # Procesar precio
            precio = Decimal(precio.replace(',', '').replace('.', '')) / 100
            
            # Procesar descuento si existe
            descuento_value = None
            if descuento:
                descuento_value = Decimal(descuento.replace('%', '').strip())
            
            # Crear el producto
            producto = Producto(
                titulo=titulo,
                precio=precio,
                categoria=int(categoria),
                descripcion=descripcion,
                marca=marca,
                descuento=descuento_value,
                dimensiones=dimensiones,
                stock=int(stock)
            )
            producto.save()

            # Guardar CADA imagen
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto publicado exitosamente con todas las imágenes.")
            return redirect('index')

        except Exception as e:
            messages.error(request, f"Error al publicar el producto: {str(e)}")
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