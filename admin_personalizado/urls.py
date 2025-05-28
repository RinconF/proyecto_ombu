
from django.urls import path
from . import views
from .views import descargar_manual

app_name = 'admin_panel'

urlpatterns = [
    path('perfil/', views.perfil_view, name='perfil'),
    path('descargar-manual/', descargar_manual, name='descargar_manual'),
]