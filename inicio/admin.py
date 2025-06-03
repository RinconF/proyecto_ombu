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
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
import os
from django.http import HttpResponse

# Agregar imports para pdfs
from io import BytesIO
from xhtml2pdf import pisa
from django.utils.translation import ngettext




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
            'all': ('admin_personalizado/css_panel/agregar_forms.css','admin_personalizado/css_panel/acc_user.css')
                  
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
    

@admin.register(Mesa, site=custom_admin_site)
class MesaAdmin(admin.ModelAdmin):
    # Asegúrate de incluir 'is_active' en list_display
    list_display = ('numero', 'capacidad', 'estado', 'is_active', 'total_pedido_actual', 'fecha_ultima_actividad', 'acciones_mesa')
    list_filter = ('is_active', 'estado', 'capacidad') # Agrega 'is_active' al filtro
    search_fields = ('numero',)
    actions = ['activar_mesas_seleccionadas', 'desactivar_mesas_seleccionadas']
    # Permite editar el estado activo directamente desde la lista
    list_editable = ('is_active',)


    def fecha_ultima_actividad(self, obj):
        # Para obtener la última actividad (pedido) de la mesa
        ultimo_pedido = obj.pedido_set.order_by('-fecha').first()
        if ultimo_pedido:
            # Puedes ajustar el formato de fecha y hora como necesites
            return ultimo_pedido.fecha.strftime('%Y-%m-%d %H:%M')
        return "N/A"
    fecha_ultima_actividad.short_description = "Última Actividad"


    def total_pedido_actual(self, obj):
        # Filtra por pedidos pendientes para esta mesa
        ultimo_pedido_pendiente = obj.pedido_set.filter(estado='pendiente').order_by('-fecha').first()
        if ultimo_pedido_pendiente:
            return f"${ultimo_pedido_pendiente.total:.2f}"
        return "N/A"
    total_pedido_actual.short_description = 'Total Pedido Actual'


    def acciones_mesa(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name

        # Enlace para editar la MESA
        edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
        # Enlace para ver los pedidos de esa MESA
        pedidos_url = reverse('admin:%s_%s_changelist' % (obj._meta.app_label, 'pedido')) + f'?mesa__id__exact={obj.pk}'

        return format_html(
            '<a class="button action-edit" href="{}"><i class="fa fa-pencil"></i> Editar Mesa</a>&nbsp;'
            '<a class="button action-view" href="{}"><i class="fa fa-eye"></i> Ver Pedidos</a>',
            edit_url,
            pedidos_url
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
            self.message_user(request, ngettext(
                '%d mesa fue activada correctamente.',
                '%d mesas fueron activadas correctamente.',
                num_activadas
            ) % num_activadas, messages.SUCCESS) # Uso ngettext para el plural
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
        self.message_user(request, ngettext(
            '%d mesa fue desactivada correctamente.',
            '%d mesas fueron desactivadas correctamente.',
            count
        ) % count, messages.SUCCESS) # Uso ngettext para el plural

    desactivar_mesas_seleccionadas.short_description = "Desactivar mesas seleccionadas"

    # Este método ya lo tenías, y es la forma correcta de mostrar un booleano con un ícono.
    @admin.display(
        description='Estado Activa',
        boolean=True,
    )
    def mostrar_estado_activo(self, obj):
        return obj.is_active
    
    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',)
        }

@admin.register(Pedido, site=custom_admin_site)
class PedidoAdmin(admin.ModelAdmin):
    # Asegúrate de que estos campos sean correctos según tu models.py
    list_display = ('id', 'mesa', 'fecha', 'estado', 'total_pedido_display', 'realizado_por', 'acciones_pedido')
    list_filter = ('estado', 'fecha', 'mesa') 
    search_fields = ('id', 'mesa__numero__icontains', 'mesero__username__icontains')
    ordering = ('-fecha',) # Ahora usa 'fecha'
    
    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',)
        }

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

    # Método para añadir URLs personalizadas al admin (para el PDF)
    def get_urls(self):
        # Importa las urls de admin por defecto
        from django.urls import path
        urls = super().get_urls()
        
        # Define la URL personalizada para la descarga del PDF
        # El 'name' debe coincidir con cómo lo llamas en reverse() en acciones_pedido
        custom_urls = [
            path('<int:pedido_id>/download_pdf/', 
                 self.admin_site.admin_view(self.download_pedido_pdf_view), 
                 name='{}_{}_download_pdf'.format(self.model._meta.app_label, self.model._meta.model_name)),
        ]
        return custom_urls + urls # Añade tus URLs personalizadas antes de las por defecto

    # Método para la columna "Acciones"
    def acciones_pedido(self, obj):
        # Enlace para ver el detalle del pedido
        view_url = reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        
        # Enlace para descargar el PDF
        pdf_url = reverse('admin:{}_{}_download_pdf'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
    
        return format_html(
            '<a class="button action-view" href="{}"><i class="fa fa-eye"></i> Ver Contenido</a>&nbsp;'
            '<a class="button action-download" href="{}"><i class="fa fa-download"></i> Descargar PDF</a>',
            view_url,
            pdf_url
        )
    acciones_pedido.short_description = 'Acciones' # Título de la columna en el panel
    
    # La vista que genera el PDF (definida como un método de la clase PedidoAdmin)
    def download_pedido_pdf_view(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        # Asume que Pedido tiene un related_name 'detalles' para PedidoDetalle
        detalles_pedido = pedido.detalles.all() 

        context = {
            'pedido': pedido,
            'detalles_pedido': detalles_pedido,
            # Puedes pasar más contexto si lo necesitas en tu plantilla PDF, como un logo
            'request': request, # Útil para generar URLs absolutas si las necesitas en el PDF
            'STATIC_URL': settings.STATIC_URL, # Pasa la URL estática para usar en la plantilla
            'MEDIA_URL': settings.MEDIA_URL, # Pasa la URL de medios para usar en la plantilla
        }
        
        # Llama a la función auxiliar para generar el PDF
        response = render_to_pdf('pages/Admin/pedidos_pdf.html', context)
        
        # Establece el nombre del archivo PDF al descargarse
        response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.id}.pdf"'
        return response




#FUNCION PARA LA TOMA DE LOS PDFS.
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = BytesIO()

    # Función de callback para xhtml2pdf para encontrar archivos estáticos y de medios
    # Esto es CRUCIAL si tu plantilla de PDF usa CSS o imágenes de STATIC_URL/MEDIA_URL
    def link_callback(uri, rel):
        # Asegúrate de que settings.STATIC_URL y settings.MEDIA_URL estén definidos
        # Y que settings.STATIC_ROOT y settings.MEDIA_ROOT apunten a directorios reales
        if uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        elif uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        else:
            return uri # Retorna la URI original si no es un archivo estático/media

        # Asegúrate de que el archivo exista antes de devolver la ruta
        if not os.path.isfile(path):
            print(f"Advertencia: Archivo no encontrado para PDF: {path}") # Para depuración
            return uri # Fallback a la URI original si el archivo no existe
        return path

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback # Usa el callback para los archivos estáticos
    )
    if pisa_status.err:
        return HttpResponse('Tuvimos algunos errores al generar el PDF <pre>%s</pre>' % html, status=400)
    
    response_pdf = HttpResponse(response.getvalue(), content_type='application/pdf')
    return response_pdf




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


