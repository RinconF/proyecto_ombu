from django.contrib import admin, messages
from .models import Pedido, Usuario, Producto, Mesa, GaleriaFoto, ConfiguracionGeneral, ActividadReciente
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.admin.utils import flatten_fieldsets
from django.utils.html import format_html
from django.urls import reverse, path
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
from io import BytesIO
from xhtml2pdf import pisa
from django.utils.translation import ngettext
import datetime
from collections import defaultdict

# --- Clase UsuarioAdmin ---
@admin.register(Usuario, site=custom_admin_site) # Asegúrate de que custom_admin_site esté importado
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
        ('Roles y Permisos', {'fields': ('rol', 'is_active', )}),
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
            fieldsets = super().get_fieldsets(request, obj)
            new_fieldsets = []
            for name, opts in fieldsets:
                current_fields = opts.get('fields', ())
                new_fields = [f for f in current_fields if f != 'usable_password']
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
        if obj is None:
            return self.add_form
        return super().get_form(request, obj, **kwargs)

    def acciones(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
        delete_url = reverse(f'admin:{app_label}_{model_name}_delete', args=[obj.pk])
        pdf_url = reverse(f'admin:{app_label}_{model_name}_download_pdf', args=[obj.pk])
        return format_html(
            '<a class="button action-edit" href="{}"><i class="fa fa-pencil"></i> Editar</a>&nbsp;' 
            '<a class="button action-delete" href="{}"><i class="fa fa-trash"></i> Eliminar</a>&nbsp;'
            '<a class="button action-download-pdf" href="{}"><i class="fa fa-download"></i> Descargar PDF</a>',
            edit_url, 
            delete_url,
            pdf_url     
        )
        
    acciones.short_description = 'Acciones'
    acciones.allow_tags = True

    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',)
        }
        # js = ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js',)

    # --- SOBRESCRIBIR LA ACCIÓN 'delete_selected' ---
    # Asegúrate de que 'delete_selected' esté en la lista de acciones si tienes alguna explícita
    # actions = ['delete_selected'] # Si defines otras acciones, inclúyela

    def delete_selected(self, request, queryset):
        """
        Sobrescribe la acción 'delete_selected' para eliminar directamente los objetos
        desde la solicitud POST de tu botón global, sin redirección a la página de confirmación.
        """
        # Ya que tu JS se encarga de la confirmación visual, aquí simplemente ejecutamos la eliminación.
        # Capturamos el número de objetos eliminados para el mensaje.
        deleted_count, _ = queryset.delete()
        self.message_user(request, ngettext(
            "%d usuario fue eliminado exitosamente.",
            "%d usuarios fueron eliminados exitosamente.",
            deleted_count
        ) % deleted_count, messages.SUCCESS)

        # Opcional: registrar la actividad de eliminación
        for obj in queryset:
            ActividadReciente.objects.create(
                usuario=request.user,
                accion=f'Eliminó el Usuario {obj.username} (ID: {obj.id}).'
            )

    delete_selected.short_description = _("Eliminar usuarios seleccionados") # Texto que aparece en la acción
    
    
    # --- NUEVA VISTA PARA DESCARGAR PDF DE TODOS LOS USUARIOS (botón global) ---
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/download_pdf/', # Usamos object_id para ser genéricos
                 self.admin_site.admin_view(self.download_user_pdf_view),
                 name='{}_{}_download_pdf'.format(self.model._meta.app_label, self.model._meta.model_name)),
        ]
        return custom_urls + urls

    def download_user_pdf_view(self, request, object_id):
        usuario = get_object_or_404(Usuario, pk=object_id) # Obtener el usuario específico
        context = {
            'title': f'Reporte de Usuario: {usuario.username}',
            'usuario': usuario, # Pasar el objeto único de usuario
            'request': request,
            'STATIC_URL': settings.STATIC_URL,
            'MEDIA_URL': settings.MEDIA_URL,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        filename = f"reporte_usuario_{usuario.username}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response = render_to_pdf('pages/Admin/usuarios_pdf.html', context) # <-- Nueva plantilla
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


# --- Clase ProductoAdmin ---
@admin.register(Producto, site=custom_admin_site)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio','cantidad_disponible', 'get_estado_display','get_categoria_display','acciones',)
    list_filter = ('estado', 'categoria',)
    search_fields = ('titulo', 'descripcion','categoria')
    ordering = ('titulo',)

    fields = ('titulo', 'descripcion', 'precio', 'cantidad_disponible', 'estado', 'foto', 'categoria', 'opciones')

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
        pdf_url = reverse(f'admin:{app_label}_{model_name}_download_pdf', args=[obj.pk])

        return format_html(
            '<a class="button action-edit" href="{}"><i class="fa fa-pencil"></i> Editar</a>&nbsp;'
            '<a class="button deletelink custom-delete-button" href="{}" data-object-name="{}"><i class="fa fa-trash"></i> Eliminar</a>&nbsp;' 
            '<a class="button action-download-pdf" href="{}"><i class="fa fa-download"></i> Descargar PDF</a>',
            edit_url,
            delete_url,
            # obj,
            obj.pk, 
            pdf_url
        )
        
    acciones.short_description = 'Acciones'
    acciones.allow_tags = True

    def get_categoria_display(self, obj):
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

    # --- SOBRESCRIBIR LA ACCIÓN 'delete_selected' ---
    def delete_selected(self, request, queryset):
        deleted_count, _ = queryset.delete()
        self.message_user(request, ngettext(
            "%d producto fue eliminado exitosamente.",
            "%d productos fueron eliminados exitosamente.",
            deleted_count
        ) % deleted_count, messages.SUCCESS)

        for obj in queryset:
            ActividadReciente.objects.create(
                usuario=request.user,
                accion=f'Eliminó el Producto {obj.titulo} (ID: {obj.id}).'
            )

    delete_selected.short_description = _("Eliminar productos seleccionados")
    
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/download_pdf/', # Usamos object_id para ser genéricos
                 self.admin_site.admin_view(self.download_product_pdf_view),
                 name='{}_{}_download_pdf'.format(self.model._meta.app_label, self.model._meta.model_name)),
            
            path('download_all_products_by_category_pdf/',
                 self.admin_site.admin_view(self.download_products_pdf_all),
                 name='{}_{}_all_by_category_pdf'.format(self.model._meta.app_label, self.model._meta.model_name)),
        ]
        return custom_urls + urls

    def download_product_pdf_view(self, request, object_id):
        producto = get_object_or_404(Producto, pk=object_id) 
        context = {
            'title': f'Reporte de Producto: {producto.titulo}',
            'producto': producto, 
            'request': request,
            'STATIC_URL': settings.STATIC_URL,
            'MEDIA_URL': settings.MEDIA_URL,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        filename = f"reporte_producto_{producto.titulo}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response = render_to_pdf('pages/Admin/productos_pdf.html', context) # <-- Nueva plantilla
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    
    def download_products_pdf_all(sefl, request,):
                # Obtener todos los productos y agruparlos por categoría
        # Asegúrate de que 'categoria' en tu modelo Producto es un campo.
        # Si 'categoria' es un CharField con choices, el get_categoria_display() es útil.
        all_products = Producto.objects.all().order_by('categoria', 'titulo')

        # Agrupar productos por categoría
        products_by_category = defaultdict(list)
        for product in all_products:
            # Usar get_categoria_display() para el nombre legible de la categoría
            category_name = product.get_categoria_display()
            products_by_category[category_name].append(product)

        # Puedes convertir defaultdict a un listado de tuplas (nombre_categoria, lista_productos)
        # y ordenarlas alfabéticamente por nombre de categoría si lo deseas.
        sorted_categories = sorted(products_by_category.items(), key=lambda item: item[0])

        context = {
            'title': 'Reporte General de Productos por Categoría',
            'categories_data': sorted_categories, # Pasamos los productos agrupados por categoría
            'request': request,
            'STATIC_URL': settings.STATIC_URL,
            'MEDIA_URL': settings.MEDIA_URL,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        filename = f"reporte_productos_por_categoria_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        # Usamos una nueva plantilla para este reporte agrupado
        response = render_to_pdf('pages/Admin/productos_lista_pdf.html', context)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Asegúrate de que esta línea exista, si no la tienes, agrégala.
        # Tu changelist_view ya la tenía, solo es para recordatorio.
        extra_context['categorias'] = Producto.CATEGORIAS

        # URL para el botón de descarga global
        download_url = reverse('admin:{}_{}_all_by_category_pdf'.format(self.model._meta.app_label, self.model._meta.model_name))
        extra_context['download_products_pdf_all'] = download_url
        return super().changelist_view(request, extra_context=extra_context)



# --- Clase GaleriaFotoAdmin ---
@admin.register(GaleriaFoto, site= custom_admin_site)
class GaleriaFotoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'get_uso_display', 'fecha_subida', 'admin_thumbnail_preview', 'acciones',)
    list_filter = ('uso', 'fecha_subida')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_subida', 'admin_thumbnail_preview')

    fieldsets = (
        (None, {
            'fields': ('titulo', 'imagen', 'descripcion', 'uso'),
        }),
    )

    def admin_thumbnail_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="auto" style="border-radius: 5px;" />')
        return "No Image"
    admin_thumbnail_preview.short_description = 'Miniatura'

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

    def get_uso_display(self, obj):
        display_value = obj.get_uso_display()
        if obj.uso == 'en_uso':
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', display_value)
        elif obj.uso == 'no_en_uso':
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', display_value)
        return display_value
    get_uso_display.short_description = 'Estado de Uso'

    def save_model(self, request, obj, form, change):
        if obj.uso == 'en_uso':
            en_uso_count = GaleriaFoto.objects.filter(uso='en_uso').exclude(pk=obj.pk).count()
            if en_uso_count >= 2:
                messages.error(request, '¡Error! Solo se pueden tener 2 imágenes "En Uso" a la vez. Desactiva otra imagen primero.')
                return
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': (
                'admin_personalizado/css_panel/acc_user.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
            )
        }

    # --- SOBRESCRIBIR LA ACCIÓN 'delete_selected' ---
    def delete_selected(self, request, queryset):
        deleted_count, _ = queryset.delete()
        self.message_user(request, ngettext(
            "%d foto de galería fue eliminada exitosamente.",
            "%d fotos de galería fueron eliminadas exitosamente.",
            deleted_count
        ) % deleted_count, messages.SUCCESS)

        for obj in queryset:
            ActividadReciente.objects.create(
                usuario=request.user,
                accion=f'Eliminó la foto de galería "{obj.titulo}" (ID: {obj.id}).'
            )

    delete_selected.short_description = _("Eliminar fotos seleccionadas")


# --- Clase MesaAdmin ---
@admin.register(Mesa, site=custom_admin_site)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidad', 'estado', 'is_active', 'total_pedido_actual', 'fecha_ultima_actividad', 'acciones_mesa')
    list_filter = ('is_active', 'estado', 'capacidad')
    search_fields = ('numero',)
    actions = ['activar_mesas_seleccionadas', 'desactivar_mesas_seleccionadas'] # Mantén estas acciones
    list_editable = ('is_active',)

    def fecha_ultima_actividad(self, obj):
        ultimo_pedido = obj.pedido_set.order_by('-fecha').first()
        if ultimo_pedido:
            return ultimo_pedido.fecha.strftime('%Y-%m-%d %H:%M')
        return "N/A"
    fecha_ultima_actividad.short_description = "Última Actividad"

    def total_pedido_actual(self, obj):
        ultimo_pedido_pendiente = obj.pedido_set.filter(estado='pendiente').order_by('-fecha').first()
        if ultimo_pedido_pendiente:
            return f"${ultimo_pedido_pendiente.total:.2f}"
        return "N/A"
    total_pedido_actual.short_description = 'Total Pedido Actual'

    def acciones_mesa(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
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
            ) % num_activadas, messages.SUCCESS)
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
        ) % count, messages.SUCCESS)

    desactivar_mesas_seleccionadas.short_description = "Desactivar mesas seleccionadas"

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

    # --- SOBRESCRIBIR LA ACCIÓN 'delete_selected' ---
    # Añade 'delete_selected' a la lista de actions si aún no está.
    actions = ['activar_mesas_seleccionadas', 'desactivar_mesas_seleccionadas', 'delete_selected']

    def delete_selected(self, request, queryset):
        deleted_count, _ = queryset.delete()
        self.message_user(request, ngettext(
            "%d mesa fue eliminada exitosamente.",
            "%d mesas fueron eliminadas exitosamente.",
            deleted_count
        ) % deleted_count, messages.SUCCESS)

        for obj in queryset:
            ActividadReciente.objects.create(
                usuario=request.user,
                accion=f'Eliminó la Mesa {obj.numero} (ID: {obj.id}).'
            )

    delete_selected.short_description = _("Eliminar mesas seleccionadas")


# --- Clase PedidoAdmin (No necesita sobrescribir delete_selected porque ya has deshabilitado has_delete_permission) ---
@admin.register(Pedido, site=custom_admin_site)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'fecha', 'estado', 'total_pedido_display', 'realizado_por', 'acciones_pedido')
    list_filter = ('estado', 'fecha', 'mesa')
    search_fields = ('id', 'mesa__numero__icontains', 'mesero__username__icontains')
    ordering = ('-fecha',)

    class Media:
        css = {
            'all': ('admin_personalizado/css_panel/acc_user.css',)
        }

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False # Correcto, deshabilitado para Pedidos

    def total_pedido_display(self, obj):
        return f"${obj.total:.2f}"
    total_pedido_display.short_description = _("Total del Pedido")

    def realizado_por(self, obj):
        return obj.mesero.username if obj.mesero else _("Desconocido")
    realizado_por.short_description = _("Realizado por")

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:pedido_id>/download_pdf/',
                 self.admin_site.admin_view(self.download_pedido_pdf_view),
                 name='{}_{}_download_pdf'.format(self.model._meta.app_label, self.model._meta.model_name)),
        ]
        return custom_urls + urls

    def acciones_pedido(self, obj):
        view_url = reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        pdf_url = reverse('admin:{}_{}_download_pdf'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html(
            '<a class="button action-view" href="{}"><i class="fa fa-eye"></i> Ver Contenido</a>&nbsp;'
            '<a class="button action-download" href="{}"><i class="fa fa-download"></i> Descargar PDF</a>',
            view_url,
            pdf_url
        )
    acciones_pedido.short_description = 'Acciones'

    def download_pedido_pdf_view(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        detalles_pedido = pedido.detalles.all()

        context = {
            'pedido': pedido,
            'detalles_pedido': detalles_pedido,
            'request': request,
            'STATIC_URL': settings.STATIC_URL,
            'MEDIA_URL': settings.MEDIA_URL,
        }
        response = render_to_pdf('pages/Admin/pedidos_pdf.html', context)
        response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.id}.pdf"'
        return response

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = BytesIO()

    def link_callback(uri, rel):
        if uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        elif uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        else:
            return uri
        if not os.path.isfile(path):
            print(f"Advertencia: Archivo no encontrado para PDF: {path}")
            return uri
        return path

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback
    )
    if pisa_status.err:
        return HttpResponse('Tuvimos algunos errores al generar el PDF <pre>%s</pre>' % html, status=400)

    response_pdf = HttpResponse(response.getvalue(), content_type='application/pdf')
    return response_pdf




# Registros
# custom_admin_site.register(Pedido)
# admin.site.register(Inventario)
# custom_admin_site.register(Usuario, UsuarioAdmin)  # Con la clase personalizada
# custom_admin_site.register(Producto, ProductoAdmin)
# admin.site.register(Reserva)
# admin.site.register(ActividadReciente)
# admin.site.register(Perfil)
# custom_admin_site.register(GaleriaFoto,GaleriaFotoAdmin)
# custom_admin_site.register(Mesa)


