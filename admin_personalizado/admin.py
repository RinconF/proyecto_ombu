# from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.urls import path  # ¡NUEVA importación!
# from inicio import views as inicio_views  
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
import json
from django.shortcuts import render
from django.template.response import TemplateResponse

class CustomAdminSite(AdminSite):
    site_header = _("OMBÜ Café")
    site_title = _("Administración de OMBÜ")
    index_title = _("Sitio administrativo")
    # Asegúrate de que index_template NO esté definido aquí si quieres que use
    # admin_personalizado/templates/admin/index.html (por el orden en INSTALLED_APPS)
    # Si quieres forzarlo, podrías poner: index_template = 'admin/index.html'

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = 'admin_personalizado/admin.css' # Si lo necesitas
        return context

    # MÉTODO INDEX REVISADO PARA MODIFICAR EL CONTEXTO CORRECTAMENTE
    def index(self, request, extra_context=None):
        # 1. Obtiene la TemplateResponse estándar del método index del padre.
        #    Esta respuesta ya contendrá el contexto base del admin (app_list, user, etc.).
        response = super().index(request, extra_context)

        # 2. Asegúrate de que la respuesta es una TemplateResponse (no un Redirect, por ejemplo).
        if not isinstance(response, TemplateResponse):
            return response # Si no es TemplateResponse, devuelve la respuesta original.

        # 3. Accede al diccionario de contexto de la respuesta para modificarlo.
        context_data = response.context_data

        # 4. Agrega tu lógica para obtener y formatear las actividades recientes (tal como la tenías).
        recent_activities = LogEntry.objects.order_by('-action_time')[:10]
        formatted_activities = []
        for entry in recent_activities:
            action_detail_message = ""
            action_description = ""
            object_display_name_text = entry.object_repr if entry.object_repr else _("un objeto desconocido")
            admin_url = entry.get_admin_url()

            if admin_url:
                object_display_name = format_html("<a href='{}'>{}</a>", admin_url, object_display_name_text)
            else:
                object_display_name = object_display_name_text

            if entry.is_addition():
                action_description = _(f"Añadido '{object_display_name}'")
            elif entry.is_change():
                action_description = _(f"Modificado '{object_display_name}'")
                if entry.change_message:
                    try:
                        message_data = json.loads(entry.change_message)
                        if isinstance(message_data, list):
                            for msg in message_data:
                                if 'changed' in msg and 'fields' in msg['changed']:
                                    changed_fields = ', '.join(msg['changed']['fields'])
                                    action_detail_message = _(f"Se actualizaron los campos: {changed_fields}.")
                                elif 'added' in msg and 'name' in msg['added'] and 'object' in msg['added']:
                                    added_name = msg['added']['name']
                                    added_object = msg['added']['object']
                                    action_detail_message = _(f"Se añadió '{added_object}' a '{added_name}'.")
                                elif 'deleted' in msg and 'name' in msg['deleted'] and 'object' in msg['deleted']:
                                    deleted_name = msg['deleted']['name']
                                    deleted_object = msg['deleted']['object']
                                    action_detail_message = _(f"Se eliminó '{deleted_object}' de '{deleted_name}'.")
                                elif isinstance(msg, dict) and msg.get('message'):
                                    action_detail_message = _(f"Detalles del cambio: {msg['message']}.")
                        elif isinstance(message_data, dict) and message_data.get('message'):
                            action_detail_message = _(f"Detalles del cambio: {message_data['message']}.")
                        else:
                            if entry.change_message.strip():
                                action_detail_message = _(f"Detalles del cambio: {entry.change_message.strip()}.")
                    except json.JSONDecodeError:
                        if entry.change_message.strip():
                            action_detail_message = _(f"Detalles del cambio: {entry.change_message.strip()}.")
                        else:
                            action_detail_message = _("No se especificaron detalles del cambio.")
                else:
                    action_detail_message = _("No se especificaron detalles del cambio.")
            elif entry.is_deletion():
                action_description = _(f"Eliminado '{object_display_name}'")
            else:
                action_description = _(f"Acción desconocida sobre '{object_display_name}'")

            final_action_text = action_description
            if action_detail_message:
                final_action_text += f": {action_detail_message}"
            final_action_text += f" por {entry.user.username}"

            formatted_activities.append({
                'accion': final_action_text,
                'fecha_hora': entry.action_time,
            })

        # 5. Agrega las actividades formateadas y tu variable de prueba al contexto_data.
        context_data['actividades_recientes'] = formatted_activities
        context_data['variable_prueba_simple'] = "¡Hola desde AdminSite MODIFICADO y PASADO!"
        context_data['title'] = 'Dashboard Administrativo OMBÚ' # Para el breadcrumbs

        # 6. Tus impresiones de depuración en la consola.
        print(f"DEBUG en admin.py (context_data modificada): actividades_recientes = {context_data['actividades_recientes']}")
        print(f"DEBUG en admin.py (context_data modificada): variable_prueba_simple = {context_data['variable_prueba_simple']}")

        # 7. Devuelve la TemplateResponse con el contexto modificado.
        return response

custom_admin_site = CustomAdminSite(name='sitio_admin_inicio')


    # ¡NUEVO MÉTODO! Aquí es donde añades tus URLs personalizadas al admin.
    # def get_urls(self):
    #     urls = super().get_urls()  # Obtiene las URLs estándar del admin (para tus modelos registrados)
    #     custom_urls = [

    #         path('inicio/dashboard/', self.admin_view(inicio_views.dashboard), name='inicio_dashboard'),

    #     ]
    #     return custom_urls + urls  

# registrarán los modelos con esta CustomAdminSite.
# admin.site = CustomAdminSite()

# admin.site.site_header = _("OMBÜ Café")
# admin.site.site_title = _("Administración de OMBÜ")
# admin.site.index_title = _("Sitio administrativo")