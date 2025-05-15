from django.contrib import admin
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = 'admin_personalizado/admin.css'
        return context

# Puedes reemplazar el sitio admin por defecto
admin.site = CustomAdminSite()
