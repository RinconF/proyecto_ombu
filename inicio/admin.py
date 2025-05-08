from django.contrib import admin
from .models import Pedidos, Inventario, Usuario, Producto, Reserva
from django.contrib.auth.admin import UserAdmin

# Clase para mejorar la vista del modelo Usuario en el admin
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'date_joined')
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
            'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'rol'),
        }),
    )

# Registros
admin.site.register(Pedidos)
admin.site.register(Inventario)
admin.site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
admin.site.register(Producto)
admin.site.register(Reserva)



