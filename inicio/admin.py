from django.contrib import admin
from .models import Pedidos, Inventario, Usuario, Producto, Reserva

# Clase para mejorar la vista del modelo Usuario en el admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo', 'rol')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter = ('rol',)

# Registros
admin.site.register(Pedidos)
admin.site.register(Inventario)
admin.site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
admin.site.register(Producto)
admin.site.register(Reserva)

