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
    path('bebida_fria/', views.bebida_fria, name='Bebida_fria'),
    path('cerveza/', views.cerveza, name='cerveza'),
    path('cigarrillo/', views.cigarrillo, name='cigarrillo'),
    path('coctel/', views.coctel, name='coctel'),
    path('picar/', views.picar, name='picar'),

    # ADMIN
    path('admin', views.admin_principal, name='admin'),
    path('admin/', admin.site.urls),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('mesas/', views.mesas, name='mesas'),
    # path('reserva/', views.reserva, name='reserva'),
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
    path('cigarrillos/', views.cigarrillos, name='cigarrillos'),
    path('cocteles/', views.cocteles, name='cocteles'),
    path('Para_picar/', views.para_picar, name='Para_picar'),
    
    
    # # RECUPERAR CONTRASEÑA
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]