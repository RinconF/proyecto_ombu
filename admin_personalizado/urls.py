
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('perfil/', views.perfil_view, name='perfil'),

]