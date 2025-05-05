from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache



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
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # <--- Aquí pasas el usuario
            return redirect('admin')  # Cambia esto según tu lógica
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'pages/Admin/login.html')  # Tu template de login

def logout_view(request):
    logout(request)
    return redirect('login') 

@never_cache
@login_required
def admin_principal(request):
    return render(request, 'pages/Admin/admin_principal.html')

@never_cache
@login_required
def dashboard (request):
    return render(request, 'pages/Admin/dasboard.html')

def admin_login_page(request):
    return render(request, 'pages/Admin/login.html')

@never_cache
@login_required
def mesas (request):
    return render(request, 'pages/Admin/mesas.html')

@never_cache
@login_required
def reserva (request):
    return render(request, 'pages/Admin/reserva.html')

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

