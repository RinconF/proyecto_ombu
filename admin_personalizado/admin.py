from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = 'admin_personalizado/admin.css'
        return context

# Puedes reemplazar el sitio admin por defecto
admin.site = CustomAdminSite()

admin.site.site_header = _("OMBÜ Café")
admin.site.site_title = _("Administración de OMBÜ")
admin.site.index_title = _("Sitio administrativo")
