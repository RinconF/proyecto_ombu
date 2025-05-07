from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from .decorators import group_required







# PRINCIPAL

def index(request):
    return render(request, 'pages/principal/index.html')


#productos_menu

def bebida_caliente(request):
    return render(request, 'pages/productos_menu/bebida_caliente.html')

def Bebida_fria (request):
    return render(request, 'pages/productos_menu/Bebida_fria.html')

def Cerveza (request):
    return render(request, 'pages/productos_menu/Cerveza.html')

def Cigarrillo (request):
    return render(request, 'pages/productos_menu/Cigarrillo.html')

def Coctel (request):
    return render(request, 'pages/productos_menu/Coctel.html')

def Picar (request):
    return render(request, 'pages/productos_menu/Picar.html')

# ADMIN

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')  # O la vista que tú desees
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'pages/Admin/login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

@never_cache
@login_required
def admin_principal(request):
    return render(request, 'pages/Admin/admin_principal.html')

@never_cache
@group_required('ombu')
def dashboard (request):
    return render(request, 'pages/Admin/dashboard.html')

def admin_login_page(request):
    return render(request, 'pages/Admin/login.html')

@never_cache
@login_required
def mesas (request):
    return render(request, 'pages/Admin/mesas.html')

@never_cache
@group_required('ombu')
def reserva (request):
    return render(request, 'pages/Admin/reserva.html')

@never_cache
@login_required
def usuarios (request):
    return render(request, 'pages/Admin/usuarios.html')

# menu mesero
@never_cache
@login_required
def bebidas_calientes (request):
    return render(request, 'pages/menu_mesero/bebidas_calientes.html')

@never_cache
@login_required
def bebidas_frias (request):
    return render(request, 'pages/menu_mesero/bebidas_frias.html')

def Cervezas (request):
    return render(request, 'pages/menu_mesero/Cervezas.html')

@never_cache
@login_required
def Cigarrillos (request):
    return render(request, 'pages/menu_mesero/Cigarrillos.html')

@never_cache
@login_required
def Cocteles (request):
    return render(request, 'pages/menu_mesero/Cocteles.html')

@never_cache
@login_required
def Para_picar (request):
    return render(request, 'pages/menu_mesero/Para_picar.html')


# #EMAIL RESERVA

# @login_required
# def generar_reserva (request):
#     if request.method == 'POST':
#         nombre = request.POST['nombre']
#         email = request.POST['email']
#         fecha = request.POST['fecha']
#         hora = request.POST['hora']
#         cantidad = request.POST['cantidad']
        
#         reserva.Reserva.objects.create(
#             nombreperReserva=nombre,
#             fecha=fecha, 
#             hora=hora,
#             cantidadPersonas=cantidad,
#             Usuario=request.user
#         )
        
    #     send_mail(
    #         subject='Confirmación de la reserva',
    #         message=f'Hola {nombre}, tu reserva fue realizada para el {fecha} a las {hora}.',
    #         from_email='correo@gmail.com',  # Remplaza con tu email configurado en settings.py
    #         recipient_list=[email],
    #         fail_silently=False,
        
    #     )
    
    #     return JsonResponse({'Success': True})
    # return render(request,'reserva.html')