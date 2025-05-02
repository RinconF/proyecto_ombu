from django.shortcuts import render



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

def admin_principal(request):
    return render(request, 'pages/Admin/admin_principal.html')

def dashboard (request):
    return render(request, 'pages/Admin/dashboard.html')

def login (request):
    return render(request, 'pages/Admin/login.html')

def mesas (request):
    return render(request, 'pages/Admin/mesas.html')

def reserva (request):
    return render(request, 'pages/Admin/reserva.html')

def usuarios (request):
    return render(request, 'pages/Admin/usuarios.html')

# Igual con los demás...

def bebidas_calientes (request):
    return render(request, 'pages/menu_mesero/bebidas_calientes.html')

def bebidas_frias (request):
    return render(request, 'pages/menu_mesero/bebidas_frias.html')

def Cervezas (request):
    return render(request, 'pages/menu_mesero/Cervezas.html')

def Cigarrillos (request):
    return render(request, 'pages/menu_mesero/Cigarrillos.html')

def Cocteles (request):
    return render(request, 'pages/menu_mesero/Cocteles.html')

def Para_picar (request):
    return render(request, 'pages/menu_mesero/Para_picar.html')

