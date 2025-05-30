from django.contrib import admin
from .models import Pedido, Usuario, Producto, Mesa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.admin.utils import flatten_fieldsets
from django.utils.html import format_html
from django.urls import reverse


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'date_joined', 'acciones')
    list_filter = ('is_active', 'rol', 'is_staff', 'is_superuser',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    
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
        if obj is None:
            return self.get_add_fieldsets(request, obj)
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
    
    
    # --- Método para la nueva columna de acciones ---
    def acciones(self, obj):
        # Usamos obj._meta.app_label y obj._meta.model_name para obtener los nombres dinámicamente
        # Esto es importante porque tu modelo de usuario está en la app 'inicio'
        app_label = obj._meta.app_label # Debería ser 'inicio'
        model_name = obj._meta.model_name # Debería ser 'usuario' (en minúsculas)

        edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
        delete_url = reverse(f'admin:{app_label}_{model_name}_delete', args=[obj.pk])

        return format_html(
            '<a class="button action-edit" href="{}"><i class="fa fa-pencil"></i> Editar</a>&nbsp;' # Añadimos clases para CSS
            '<a class="button action-delete" href="{}"><i class="fa fa-trash"></i> Eliminar</a>',
            edit_url,
            delete_url
        )
    acciones.short_description = 'Acciones' # Nombre de la columna
    acciones.allow_tags = True # Permitir HTML en la celda

    # Para cargar tu CSS personalizado si no lo estás haciendo ya en otro lugar
    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',) # Asegúrate de que esta ruta sea correcta
        }
        # Si usas Font Awesome y no lo has incluido globalmente en tus plantillas
        # js = ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js',) # Esto es un CDN. Considera servirlo localmente.

    
    
    

# --- CLASE ProductoAdmin (Esta es la importante para las columnas) ---
@admin.register(Producto) 
class ProductoAdmin(admin.ModelAdmin):
    # ¡AQUÍ DEFINES LAS COLUMNAS PARA LA TABLA DE PRODUCTOS!
    list_display = ('titulo', 'precio', 'get_estado_display', 'acciones')
    list_filter = ('estado', 'categoria',)
    search_fields = ('titulo', 'descripcion','categoria')
    ordering = ('titulo',) 

    def get_estado_display(self, obj):
        display_value = obj.get_estado_display() 
        if obj.estado == 'disponible':
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', display_value)
        elif obj.estado == 'no_disponible':
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', display_value)
        return display_value 
    
    get_estado_display.short_description = 'Estado'


    def acciones(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name

        edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
        delete_url = reverse(f'admin:{app_label}_{model_name}_delete', args=[obj.pk])

        return format_html(
            '<a class="button action-edit" href="{}"><i class="fa fa-pencil"></i> Editar</a>&nbsp;'
            '<a class="button deletelink custom-delete-button" href="{}" data-object-name="{}"><i class="fa fa-trash"></i> Eliminar</a>',
            edit_url,
            delete_url,
            obj 
        )
    acciones.short_description = 'Acciones'
    acciones.allow_tags = True 

    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',) 
        }
    
     
# Registros
admin.site.register(Pedido)
admin.site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Mesa)




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
