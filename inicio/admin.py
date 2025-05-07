from django.contrib import admin
<<<<<<< HEAD
from .models import Pedidos, Inventario, Usuario, Producto, Reserva
=======
from .models import Rol, Categoria, Usuario, Producto, Reserva
>>>>>>> ee9a663acf74db5e6e4ac7b72c1de1e2ac7921c6

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
<<<<<<< HEAD

=======
>>>>>>> ee9a663acf74db5e6e4ac7b72c1de1e2ac7921c6
