from django.contrib import admin
from .models import Usuario, Producto, Reserva

# Clase para mejorar la vista del modelo Usuario en el admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter = ('rol',)

# Registros
# admin.site.register(Rol)
# admin.site.register(Categoria)
admin.site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
admin.site.register(Producto)
admin.site.register(Reserva)
# admin.site.register(Factura)
