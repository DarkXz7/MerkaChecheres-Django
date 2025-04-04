from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    readonly_fields = ('imagen_preview',)
    fields = ('imagen_preview', 'imagen')
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" style="max-height: 200px; max-width: 200px;" />')
        return "No hay imagen disponible"
    
    imagen_preview.short_description = "Vista Previa"

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'categoria', 'fecha_publicacion', 'imagen_principal')
    list_filter = ('categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion')
    inlines = [ImagenProductoInline]
    
    def imagen_principal(self, obj):
        primera_imagen = obj.imagenes.first()
        if primera_imagen and primera_imagen.imagen:
            return mark_safe(f'<img src="{primera_imagen.imagen.url}" style="max-height: 100px; max-width: 100px;" />')
        return "Sin imagen"
    
    imagen_principal.short_description = "Imagen Principal"
    imagen_principal.allow_tags = True

admin.site.register(Usuario)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ImagenProducto)