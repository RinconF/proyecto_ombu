from django.contrib import admin
from .models import Pedidos, Inventario, Usuario, Producto, Reserva
from django.contrib.auth.admin import UserAdmin
# from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva
from .forms import customusuario_crear,customusuario_change

# Clase para mejorar la vista del modelo Usuario en el admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'date_joined')
    add_form = customusuario_crear  # Usa tu formulario de creación personalizado
    form = customusuario_change     # Usa tu formulario de edición personalizado
    fieldsets = (
         (None, {'fields': ('username', 'password')}),
         ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
         ('Roles y Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions')}),  # Añadidos groups y user_permissions
         ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
     )
    readonly_fields = ('last_login', 'date_joined')
    add_fieldsets = (
         (None, {
             'classes': ('wide',),
             'fields': ('username', 'email', 'first_name', 'last_name', 'rol'),   #se elimino password
         }),
     )
     
# Registros
admin.site.register(Pedidos)
admin.site.register(Inventario)
admin.site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
admin.site.register(Producto)
admin.site.register(Reserva)




# from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva

# @admin.register(Rol)
# class RolAdmin(admin.ModelAdmin):
#     list_display = ('tipoRol',)

# @admin.register(Categoria)
# class CategoriaAdmin(admin.ModelAdmin):
#     list_display = ('nombreCategoria',)
#     search_fields = ('nombreCategoria',)
#     ordering      = ('nombreCategoria',)

# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
#     list_display  = ('nombre', 'apellido', 'correo', 'rol')
#     search_fields = ('nombre', 'apellido', 'correo')
#     list_filter   = ('rol',)
#     ordering      = ('apellido',)

# @admin.register(Producto)
# class ProductoAdmin(admin.ModelAdmin):
#     list_display  = ('nombreProducto', 'precio', 'categoria')
#     search_fields = ('nombreProducto',)
#     list_filter   = ('categoria',)
#     ordering      = ('nombreProducto',)

# @admin.register(Mesa)
# class MesaAdmin(admin.ModelAdmin):
#     list_display = ('numero',)
#     ordering     = ('numero',)

# @admin.register(Pedido)
# class PedidoAdmin(admin.ModelAdmin):
#     list_display    = ('id', 'usuario', 'mesa', 'total', 'fecha')
#     list_filter     = ('fecha', 'mesa')
#     date_hierarchy  = 'fecha'

# @admin.register(Reserva)
# class ReservaAdmin(admin.ModelAdmin):
#     list_display    = ('id', 'usuario', 'mesa', 'fecha', 'estado')
#     list_filter     = ('estado', 'fecha')
#     date_hierarchy  = 'fecha'
c