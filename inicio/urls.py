from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import dashboard
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView

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
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('mesas/', views.mesas, name='mesas'),
    path('reserva/', views.reserva, name='reserva'),
    path('usuarios/', views.usuarios, name = 'usuarios'),
    path('logout/', views.logout_view, name='logout'),


    # MENU MESERO
    path('bebidas_calientes/', views.bebidas_calientes, name='bebidas_calientes'),
    path('bebidas_frias/', views.bebidas_frias, name='bebidas_frias'),
    path('cervezas/', views.cervezas, name='cervezas'),
    path('cigarrillos/', views.cigarrillos, name='cigarrillos'),
    path('cocteles/', views.cocteles, name='cocteles'),
    path('Para_picar/', views.para_picar, name='Para_picar'),
    
    
    # # RECUPERAR CONTRASEÑA
        path('password_reset/', PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        # email_template_name='registration/password_reset_email.txt',
        html_email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

#dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/exportar/', views.exportar_dashboard, name='exportar_dashboard'),
]