from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path  # ¡NUEVA importación!
from inicio import views as inicio_views  


class CustomAdminSite(AdminSite):
    site_header = _("OMBÜ Café")
    site_title = _("Administración de OMBÜ")
    index_title = _("Sitio administrativo")

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = 'admin_personalizado/admin.css'
        return context

    # ¡NUEVO MÉTODO! Aquí es donde añades tus URLs personalizadas al admin.
    def get_urls(self):
        urls = super().get_urls()  # Obtiene las URLs estándar del admin (para tus modelos registrados)
        custom_urls = [

            path('inicio/dashboard/', self.admin_view(inicio_views.dashboard), name='inicio_dashboard'),

        ]
        return custom_urls + urls  

# registrarán los modelos con esta CustomAdminSite.
admin.site = CustomAdminSite()

admin.site.site_header = _("OMBÜ Café")
admin.site.site_title = _("Administración de OMBÜ")
admin.site.index_title = _("Sitio administrativo")
