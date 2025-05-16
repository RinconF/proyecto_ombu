from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .decorators import group_required
from .models import Categoria, Producto, Pedido, Mesa
from django.db.models import Sum, Count
import datetime
import calendar
import openpyxl
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from .decorators import group_required
from django.db.utils import ProgrammingError

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
    # Ventas por mes
    hoy = datetime.date.today()
    ventas_mensuales = []
    ventas_mensuales_labels = []
    ventas_mensuales_data = []

    for i in range(1, 13):
        total = Pedido.objects.filter(fecha__month=i).aggregate(Sum('total'))['total__sum'] or 0
        ventas_mensuales.append({'month': calendar.month_name[i], 'total': float(total)})
        ventas_mensuales_labels.append(calendar.month_name[i])
        ventas_mensuales_data.append(float(total))

    # Top mesas más usadas
    mesas_usadas = (
        Pedido.objects.values('mesa__numero')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # Top productos más vendidos
    productos_vendidos = (
        Producto.objects.annotate(total=Count('pedido'))
        .order_by('-total')[:5]
    )

    # Cálculos simples para los 4 recuadros:
    ventas_totales = Pedido.objects.aggregate(Sum('total'))['total__sum'] or 0
    hoy = datetime.date.today()
    ventas_dia = Pedido.objects.filter(fecha__date=hoy).aggregate(Sum('total'))['total__sum'] or 0
    ventas_mes = Pedido.objects.filter(fecha__month=hoy.month).aggregate(Sum('total'))['total__sum'] or 0
    ventas_anio = Pedido.objects.filter(fecha__year=hoy.year).aggregate(Sum('total'))['total__sum'] or 0

    return render(request, 'dashboard.html', {
        'ventas_mensuales_labels': ventas_mensuales_labels,
        'ventas_mensuales_data': ventas_mensuales_data,
        'mesas_usadas': mesas_usadas,
        'productos_vendidos': productos_vendidos,
        'ventas_totales': ventas_totales,
        'ventas_dia': ventas_dia,
        'ventas_mes': ventas_mes,
        'ventas_anio': ventas_anio
    })

def exportar_dashboard(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Dashboard Ventas"

    sheet.append(["Mes", "Total Ventas"])
    for i in range(1, 13):
        total = Pedido.objects.filter(fecha__month=i).aggregate(Sum('total'))['total__sum'] or 0
        sheet.append([calendar.month_name[i], float(total)])

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="dashboard_ventas.xlsx"'
    workbook.save(response)
    return response

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