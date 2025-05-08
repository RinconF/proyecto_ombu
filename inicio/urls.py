from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('admin', views.admin_principal, name='admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('mesas/', views.mesas, name='mesas'),
    path('reserva/', views.reserva, name='reserva'),
    path('logout/', views.logout_view, name='logout'),



    # MENU MESERO
    path('bebidas_calientes/', views.bebidas_calientes, name='bebidas_calientes'),
    path('bebidas_frias/', views.bebidas_frias, name='bebidas_frias'),
    path('cervezas/', views.Cervezas, name='cervezas'),
    path('cigarrillos/', views.Cigarrillos, name='cigarrillos'),
    path('cocteles/', views.Cocteles, name='cocteles'),
    path('Para_picar/', views.Para_picar, name='Para_picar'),
    
    
    # # RECUPERAR CONTRASEÑA
    path('password_reset/',
            auth_views.PasswordResetView.as_view(
                template_name='registration/password_reset_form.html'
            ),
            name='password_reset'),

    # 2. Mensaje de "correo enviado"
    path('password_reset/done/',
            auth_views.PasswordResetDoneView.as_view(
                template_name='registration/password_reset_done.html'
            ),
            name='password_reset_done'),

    # 3. URL con token para cambiar contraseña
    path('reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='registration/password_reset_confirm.html'
            ),
            name='password_reset_confirm'),

    # 4. Confirmación de cambio exitoso
    path('reset/done/',
            auth_views.PasswordResetCompleteView.as_view(
                template_name='registration/password_reset_complete.html'
            ),
            name='password_reset_complete'),
]

