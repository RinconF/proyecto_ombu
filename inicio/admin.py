from django.contrib import admin
from .models import Rol, Categoria, Usuario, Producto, Reserva

# Clase para mejorar la vista del modelo Usuario en el admin
class UsuarioAdmin(admin.ModelAdmin):   
    list_display = ('nombre', 'apellido', 'correo', 'rol')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter = ('rol',)

class CategoriaAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista dentro del admin
    list_display = ('nombreCategoria',)
    search_fields = ('nombreCategoria',)
    ordering = ('nombreCategoria',)
    
class ProductoAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista dentro del admin
    list_display = ('nombreProducto',)
    search_fields = ('nombreProducto',)
    ordering = ('nombreProducto',)

# Registros
admin.site.register(Rol)
admin.site.register(Categoria)
# admin.site.register(Inventario)
admin.site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
admin.site.register(Producto)
admin.site.register(Reserva)
