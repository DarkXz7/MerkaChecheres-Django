from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) 
    telefono = models.CharField(max_length=15, default="Sin teléfono")  # Valor por defecto
    departamento = models.CharField(max_length=100, default="Sin departamento")  # Valor por defecto
    direccion = models.CharField(max_length=255, default="Sin dirección")  # Valor por defecto
    municipio = models.CharField(max_length=100, default="Sin municipio")  # Valor por defecto
    ciudad = models.CharField(max_length=100, default="Sin ciudad")  # Valor por defecto
    ROLES = (
        (1, "Admin"),
        (2, "Cliente"),
        (3, "Vendedor")
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    
    def __str__(self):
        return self.username


class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dimensiones = models.CharField(max_length=100, null=True, blank=True)
    stock = models.IntegerField()
    marca = models.CharField(max_length=100, null=True, blank=True)
    
    categoria = (
        (1, "Muebles"),
        (2, "Electrónica"),
        (3, "Ropa y Accesorios"),
        (4, "Hogar y Jardín")
    )
    categoria = models.IntegerField(choices=categoria, default=0)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/imagenes/')

    
    def __str__(self):
        return f"Imagen de {self.producto.titulo}"