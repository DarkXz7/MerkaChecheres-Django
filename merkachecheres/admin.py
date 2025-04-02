from django.contrib import admin
from .models import *
from django.utils.html import format_html

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1  # Número de imágenes adicionales que se pueden agregar en el admin
    readonly_fields = ('vista_previa',)  # Campo de solo lectura para mostrar la imagen
    fields = ('vista_previa', 'imagen')  # Orden de los campos en el formulario

    # Método para mostrar la miniatura de la imagen
    def vista_previa(self, obj):
        if obj.imagen:  # Verificar si existe una imagen
            return format_html('<img src="{}" style="width: 250px; height: 200px;" />', obj.imagen.url)
        return "No hay imagen"

    vista_previa.short_description = "Vista previa"  # Nombre del campo en el admin

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'categoria', 'fecha_publicacion', 'mostrar_imagen')
    readonly_fields = ('fecha_publicacion',)
    inlines = [ImagenProductoInline]  # Mostrar imágenes relacionadas en el admin

    def mostrar_imagen(self, obj):
        primera_imagen = obj.imagenes.first()  # Obtener la primera imagen relacionada
        if primera_imagen and primera_imagen.imagen:  # Verificar si existe una imagen
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', primera_imagen.imagen.url)
        return "No hay imagen"

    mostrar_imagen.short_description = "Imagen"

# Registrar los modelos en el panel de administración
admin.site.register(Usuario)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ImagenProducto)
