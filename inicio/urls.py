from django.urls import path
from . import views

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
    path('admin', views.admin_principal, name='admin_principal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('mesas/', views.mesas, name='mesas'),
    path('reserva/', views.reserva, name='reserva'),

    # MENU MESERO
    path('bebidas_calientes/', views.bebidas_calientes, name='bebidas_calientes'),
    path('bebidas_frias/', views.bebidas_frias, name='bebidas_frias'),
    path('cervezas/', views.Cervezas, name='cervezas'),
    path('cigarrillos/', views.Cigarrillos, name='cigarrillos'),
    path('cocteles/', views.Cocteles, name='cocteles'),
    path('Para_picar/', views.Para_picar, name='Para_picar'),
    
    
    # MESAS
    path('mesas/',views.mesas, name='mesas'),
    
    path('productos/bebidas_calientes/<int:mesa_id>/', views.bebidas_calientes, name='bebidas_calientes'),
    path('productos/bebidas_frias/<int:mesa_id>/', views.bebidas_frias, name='bebidas_frias'),
    path('pedido/agregar/', views.agregar_pedido, name='agregar_pedido'),
]
