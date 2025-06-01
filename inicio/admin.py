from django.contrib import admin, messages
from .models import Pedido, Usuario, Producto, Mesa, GaleriaFoto, ConfiguracionGeneral, ActividadReciente
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.admin.utils import flatten_fieldsets
from django.utils.html import format_html
from django.urls import reverse
from django.utils.html import mark_safe
from django.db.models import Q
from admin_personalizado.admin import custom_admin_site
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

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
@admin.register(Producto, site=custom_admin_site) 
class ProductoAdmin(admin.ModelAdmin):
    # ¡AQUÍ DEFINES LAS COLUMNAS PARA LA TABLA DE PRODUCTOS!
    list_display = ('titulo', 'precio', 'get_estado_display','get_categoria_display','acciones',)
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
    
    
    # --- MÉTODO CORREGIDO PARA MOSTRAR LA CATEGORÍA ---
    def get_categoria_display(self, obj):
        # Aquí estaba el error tipográfico: 'caregoria' debe ser 'categoria'
        # obj.get_CAMPO_display() es la forma estándar de obtener el valor legible de un campo con choices.
        return obj.get_categoria_display()
    
    get_categoria_display.short_description = 'Categoría'
        
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['categorias'] = Producto.CATEGORIAS
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',) 
        }
    
@admin.register(GaleriaFoto, site= custom_admin_site)
class GaleriaFotoAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'get_uso_display', 'fecha_subida', 'admin_thumbnail_preview', 'acciones',)
    list_filter = ('uso', 'fecha_subida') 
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_subida', 'admin_thumbnail_preview')

    # Los campos que aparecerán en el formulario de edición/creación
    fieldsets = (
        (None, {
            'fields': ('titulo', 'imagen', 'descripcion', 'uso'), # Asegúrate de que 'uso' esté aquí
        }),
    )

    # --- Método para la columna 'Miniatura' ---
    def admin_thumbnail_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="auto" style="border-radius: 5px;" />')
        return "No Image"
    admin_thumbnail_preview.short_description = 'Miniatura'

    # --- Método para la columna 'Acciones' (Editar/Eliminar) ---
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
            obj # Pasamos el objeto completo para el atributo data-object-name si lo usas en JS
        )
    acciones.short_description = 'Acciones'
    # 'allow_tags = True' es redundante con 'format_html' pero no hace daño
    # acciones.allow_tags = True 

    # --- NUEVO MÉTODO para la columna 'Estado' ---
    def get_uso_display(self, obj):
        # Utiliza get_FOO_display() para obtener la representación legible de un campo con choices
        display_value = obj.get_uso_display() 
        
        # Puedes añadir estilos condicionales si quieres
        if obj.uso == 'en_uso':
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', display_value)
        elif obj.uso == 'no_en_uso':
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', display_value)
        return display_value
    get_uso_display.short_description = 'Estado de Uso' # Nombre de la columna

    # --- Lógica de validación para el límite de 2 imágenes 'en_uso' ---
    def save_model(self, request, obj, form, change):
        if obj.uso == 'en_uso':
            # Contar cuántas imágenes ya están 'en_uso', excluyendo la imagen actual si ya existe
            en_uso_count = GaleriaFoto.objects.filter(uso='en_uso').exclude(pk=obj.pk).count()

            if en_uso_count >= 2:
                messages.error(request, '¡Error! Solo se pueden tener 2 imágenes "En Uso" a la vez. Desactiva otra imagen primero.')
                # No llamar a super().save_model() evita que el objeto se guarde
                return 
        
        # Si la validación pasa o el 'uso' no es 'en_uso', guardamos el objeto
        super().save_model(request, obj, form, change)

    # --- Configuración de recursos estáticos (CSS/JS) ---
    class Media:
        css = {
            'all': (
                'admin_personalizado/css_panel/acc_user.css', # Tu CSS personalizado para los botones
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css', # Font Awesome para los íconos
            )
        }
    

@admin.register(Mesa, site=custom_admin_site) # <<-- MUY IMPORTANTE: Asegúrate que 'site=custom_admin_site' esté aquí
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado', 'mostrar_estado_activo', 'total_pedido_actual', 'fecha_ultima_actividad', 'acciones_mesa')
    list_filter = ('estado', 'is_active',)
    search_fields = ('numero',)
    actions = ['activar_mesas_seleccionadas', 'desactivar_mesas_seleccionadas']
    
    search_fields = ['numero']

    def fecha_ultima_actividad(self, obj):
        # Placeholder por ahora.
        return "N/A"
    fecha_ultima_actividad.short_description = "Última Actividad"


    def total_pedido_actual(self, obj):
        # CORRECCIÓN AQUÍ: Cambia 'obj.pedidos' a 'obj.pedido_set'
        ultimo_pedido = obj.pedido_set.filter(estado='pendiente').order_by('-fecha').first()
        if ultimo_pedido:
            return f"${ultimo_pedido.total:.2f}"
        return "N/A"
    total_pedido_actual.short_description = 'Total Pedido Actual' 


    def acciones_mesa(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = reverse('admin:%s_%s_changelist' % (obj._meta.app_label, 'pedido'))

        edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
        
        
        return format_html(
            '<a class="button action-edit" href="{}"><i class="fa fa-pencil"></i> Editar</a>&nbsp;'
            '<a class="button" href="{}?mesa__id__exact={}">Ver Pedidos</a>&nbsp;',
            url,
            edit_url,
            obj.pk
        )
        
        
        
        
    acciones_mesa.short_description = 'Acciones'


    def activar_mesas_seleccionadas(self, request, queryset):
        config = ConfiguracionGeneral.objects.first()
        if not config:
            self.message_user(request, "Error: No se ha configurado el límite de mesas activas.", level=messages.ERROR)
            return

        limite_mesas = config.limite_mesas
        mesas_activas_actuales = Mesa.objects.filter(is_active=True).count()
        mesas_a_activar = queryset.filter(is_active=False)
        
        num_activadas = 0
        for mesa in mesas_a_activar:
            if mesas_activas_actuales < limite_mesas:
                mesa.is_active = True
                mesa.save()
                num_activadas += 1
                mesas_activas_actuales += 1
                ActividadReciente.objects.create(
                    usuario=request.user,
                    accion=f'Activó la Mesa {mesa.numero} (ID: {mesa.id}).'
                )
            else:
                messages.warning(request, f"No se pudo activar la Mesa {mesa.numero}. Se alcanzó el límite de {limite_mesas} mesas activas.")
                break

        if num_activadas > 0:
            self.message_user(request, f"{num_activadas} mesa(s) activada(s) correctamente.")
        else:
            messages.info(request, "Ninguna mesa seleccionada pudo ser activada debido al límite o ya estaban activas.")

    activar_mesas_seleccionadas.short_description = "Activar mesas seleccionadas"

    def desactivar_mesas_seleccionadas(self, request, queryset):
        count = queryset.update(is_active=False)
        for mesa in queryset:
            ActividadReciente.objects.create(
                usuario=request.user,
                accion=f'Desactivó la Mesa {mesa.numero} (ID: {mesa.id}).'
            )
        self.message_user(request, f"{count} mesa(s) desactivada(s) correctamente.")
    desactivar_mesas_seleccionadas.short_description = "Desactivar mesas seleccionadas"

    @admin.display(
        description='Estado Activa',
        boolean=True,
    )
    def mostrar_estado_activo(self, obj):
        return obj.is_active

@admin.register(Pedido, site=custom_admin_site)
class PedidoAdmin(admin.ModelAdmin):
    # Asegúrate de que estos campos sean correctos según tu models.py
    list_display = ('id', 'mesa', 'fecha', 'estado', 'total_pedido_display', 'realizado_por')
    list_filter = ('estado', 'fecha', 'mesa') 
    search_fields = ('id', 'mesa__numero', 'mesero__username')
    ordering = ('-fecha',) # Ahora usa 'fecha'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def total_pedido_display(self, obj):
        return f"${obj.total:.2f}"
    total_pedido_display.short_description = _("Total del Pedido")
    
    def realizado_por(self, obj):
        return obj.mesero.username if obj.mesero else _("Desconocido")
    realizado_por.short_description = _("Realizado por")


# Registros
# custom_admin_site.register(Pedido)
# admin.site.register(Inventario)
custom_admin_site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
# custom_admin_site.register(Producto, ProductoAdmin)
# admin.site.register(Reserva)
# admin.site.register(ActividadReciente)
# admin.site.register(Perfil)
# custom_admin_site.register(GaleriaFoto,GaleriaFotoAdmin)
# custom_admin_site.register(Mesa)


