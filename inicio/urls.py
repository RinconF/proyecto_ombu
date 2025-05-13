from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import usuarios_view    
from django.contrib import admin

urlpatterns = [
    # PRINCIPAL
    path('', views.index, name='index'),

    # PRODUCTOS MENU
    path('bebida_caliente/', views.bebida_caliente, name='bebida_caliente'),
    path('Bebida_fria/', views.Bebida_fria, name='Bebida_fria'),
    path('cerveza/', views.Cerveza, name='cerveza'),
    path('cigarrillo/', views.Cigarrillo, name='cigarrillo'),
    path('coctel/', views.Coctel, name='coctel'),
    path('picar/', views.Picar, name='picar'),

    # ADMIN
    # path('admin', views.admin_principal, name='admin'),
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('mesas/', views.mesas, name='mesas'),
    path('reserva/', views.reserva, name='reserva'),
    path('usuarios/', views.usuarios, name = 'usuarios'),
    path('logout/', views.logout_view, name='logout'),

    # API de usuarios
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('actualizar-usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    path('actualizar-estado-usuario/<int:user_id>/', views.actualizar_estado_usuario, name='actualizar_estado_usuario'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/obtener/<int:user_id>/', views.obtener_usuario, name='obtener_usuario'),  # Nueva ruta
    path('admin/usuarios/', usuarios_view, name='usuarios'),



    # MENU MESERO
    path('bebidas_calientes/', views.bebidas_calientes, name='bebidas_calientes'),
    path('bebidas_frias/', views.bebidas_frias, name='bebidas_frias'),
    path('cervezas/', views.Cervezas, name='cervezas'),
    path('cigarrillos/', views.Cigarrillos, name='cigarrillos'),
    path('cocteles/', views.Cocteles, name='cocteles'),
    path('Para_picar/', views.Para_picar, name='Para_picar'),
]
