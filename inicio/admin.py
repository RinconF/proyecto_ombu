from django.contrib import admin
from .models import Pedidos, Inventario, Usuario, Producto, Reserva
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva
from .forms import customusuario_crear,customusuario_change
from django.contrib.admin.utils import flatten_fieldsets


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'date_joined')
    list_filter = ('is_active', 'rol', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
     
    add_form = customusuario_crear  
    form = customusuario_change     
    
    
    fieldsets = (
         (None, {'fields': ('username',)}),
         ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
         ('Roles y Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),  
         ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
     )
    readonly_fields = ('last_login', 'date_joined')
    def get_add_fieldsets(self, request, obj=None):
        return (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'first_name', 'last_name', 'rol', 'password1', 'password2'),
            }),
        )
    
    def get_fieldsets(self, request, obj=None):
        # Si estamos en la vista de añadir (obj es None), usamos los add_fieldsets definidos.
        if obj is None:
            return self.get_add_fieldsets(request, obj)
        # Si estamos en la vista de edición (obj existe), obtenemos los fieldsets predeterminados
        # de la clase padre y nos aseguramos de que 'usable_password' sea eliminado.
        else:
            # Obtenemos los fieldsets de la clase padre (BaseUserAdmin)
            fieldsets = super().get_fieldsets(request, obj)
            new_fieldsets = []
            for name, opts in fieldsets:
                # Filtramos 'usable_password' de la lista de campos
                current_fields = opts.get('fields', ())
                new_fields = [f for f in current_fields if f != 'usable_password']

                # Si después de filtrar quedan campos, los añadimos a los nuevos fieldsets
                if new_fields:
                    new_fieldsets.append(
                        (name, {
                            'fields': tuple(new_fields),
                            'classes': opts.get('classes', ()),
                            'description': opts.get('description', ''),
                        })
                    )
            return tuple(new_fieldsets)
    
    
    def get_form(self, request, obj=None, **kwargs):
        # Si obj es None, significa que estamos en la vista de "añadir nuevo usuario".
        if obj is None:
            # En este caso, devolvemos directamente nuestra clase de formulario de creación.
            # Esto evita cualquier lógica de la clase padre (BaseUserAdmin)
            # que pueda estar intentando añadir 'usable_password' o manipular los campos.
            return self.add_form
        # Para la vista de edición (obj existe), seguimos usando la lógica normal
        # y llamamos a la clase padre para que maneje el formulario de cambio.
        return super().get_form(request, obj, **kwargs)
     
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
