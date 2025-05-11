from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .decorators import group_required
from .models import Categoria, Producto, Pedido, Mesa
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .decorators import group_required

# PRINCIPAL
def index(request):
    return render(request, 'pages/principal/index.html')

# CATEGORIA
def listar_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'pages/categoria/listar_categoria.html', {'categorias': categorias})

# PRODUCTOS MENU
def bebida_caliente(request):
    return render(request, 'pages/productos_menu/bebida_caliente.html')

def bebida_fria(request):
    return render(request, 'pages/productos_menu/Bebida_fria.html')

def cerveza(request):
    return render(request, 'pages/productos_menu/Cerveza.html')

def cigarrillo(request):
    return render(request, 'pages/productos_menu/Cigarrillo.html')

def coctel(request):
    return render(request, 'pages/productos_menu/Coctel.html')

def picar(request):
    return render(request, 'pages/productos_menu/Picar.html')

# ADMIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
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
def dashboard(request):
    # Totales
    total_pedidos = Pedido.objects.count()
    ingresos = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0

    # Top productos
    top_productos = Producto.objects.annotate(veces_vendido=Count('pedido')).order_by('-veces_vendido')[:5]

    # Mesas más usadas
    mesas_top = Pedido.objects.values('mesa__numero').annotate(usos=Count('id')).order_by('-usos')[:5]

    # Ventas por mes últimos 6 meses
    qs = Pedido.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total_mes=Sum('total')).order_by('mes')[:6]
    labels = [item['mes'].strftime('%b') for item in qs]
    data   = [item['total_mes'] for item in qs]

    context = {
        'total_pedidos': total_pedidos,
        'ingresos': ingresos,
        'top_productos': top_productos,
        'mesas_top': mesas_top,
        'ventas_por_mes_labels': labels,
        'ventas_por_mes_data': data,
    }
    return render(request, 'pages/Admin/dashboard.html', context)

def admin_login_page(request):
    return render(request, 'pages/Admin/login.html')

@never_cache
@login_required
def mesas(request):
    return render(request, 'pages/Admin/mesas.html')

@never_cache
@group_required('ombu')
def reserva(request):
    return render(request, 'pages/Admin/reserva.html')

@never_cache
@login_required
def usuarios(request):
    return render(request, 'pages/Admin/usuarios.html')

# MENU MESERO
@never_cache
@login_required
def bebidas_calientes(request):
    return render(request, 'pages/menu_mesero/bebidas_calientes.html')

@never_cache
@login_required
def bebidas_frias(request):
    return render(request, 'pages/menu_mesero/bebidas_frias.html')

@never_cache
@login_required
def cervezas(request):
    return render(request, 'pages/menu_mesero/Cervezas.html')

@never_cache
@login_required
def cigarrillos(request):
    return render(request, 'pages/menu_mesero/Cigarrillos.html')

@never_cache
@login_required
def cocteles(request):
    return render(request, 'pages/menu_mesero/Cocteles.html')

@never_cache
@login_required
def para_picar(request):
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