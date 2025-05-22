from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST, require_http_methods
from django.urls import reverse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .decorators import role_required

# from .models import Reserva
# from django.core.mail import send_mail
import json
from .models import Usuario
from .forms import CustomUserCreationForm, CustomUserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Producto
from django.contrib.admin.views.decorators import staff_member_required

from .decorators import group_required
# from .models import Categoria, Producto, Pedido, Mesa
from django.db.models import Sum, Count
import datetime
import calendar
# import openpyxl
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
    productos = Producto.objects.filter(estado='disponible', categoria='bebida_caliente')
    return render(request, 'pages/productos_menu/bebida_caliente.html', {'productos': productos})

def bebida_fria(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Bebida_fria')
    return render(request, 'pages/productos_menu/Bebida_fria.html', {'productos': productos})

def cerveza(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Cerveza')
    return render(request, 'pages/productos_menu/Cerveza.html', {'productos': productos})

def cigarrillo(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Cigarrillo')
    return render(request, 'pages/productos_menu/Cigarrillo.html', {'productos': productos})

def coctel(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Coctel')
    return render(request, 'pages/productos_menu/Coctel.html', {'productos': productos})

def picar(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Picar')
    return render(request, 'pages/productos_menu/Picar.html', {'productos': productos})


# ADMIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redireccionar según el rol del usuario
                print(f"Inicio de sesión exitoso para: {user.username}, rol: {user.rol}")  # Para depurar
                if user.is_superuser:
                    return redirect('admin:index')  
                elif user.rol.lower() == 'ombu':
                    return redirect('dashboard')  # Corregido a 'dashboard' (ver urls.py)
                elif user.rol.lower() == 'mesero':  # Nueva condición para mesero
                    return redirect('mesero_principal')  # Redirige a la vista de mesero
                else:
                    return redirect('index')  # Redirige a la página principal por defecto
            else:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    # Si el usuario ya está autenticado, redirigir según su rol
    if request.user.is_authenticated:
        print(f"Usuario ya autenticado: {request.user.username}, rol: {request.user.rol}") 
        if request.user.is_superuser:
            return redirect('admin:index')  # Redirige al panel de administración de Django
        elif request.user.rol.lower() == 'ombu':
            return redirect('dashboard')  # Corregido a 'dashboard'
        elif request.user.rol.lower() == 'mesero':  # Nueva condición para mesero
            return redirect('mesero_principal')  # Redirige a la vista de mesero
        else:
            return redirect('index')  # Redirige a la página principal por defecto

    return render(request, 'pages/Admin/login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

@never_cache
@login_required
def admin_principal(request):
    return render(request, 'pages/Admin/admin_principal.html')


# NUEVA VISTA PARA MESEROS
@never_cache
@login_required
@user_passes_test(lambda u: u.rol == 'mesero' or u.rol == 'administrador') # Permite a administradores también acceder si es necesario
def mesero_principal(request):
    """Panel principal para usuarios con rol 'Mesero'"""
    return render(request, 'pages/menu_mesero/mesero_principal.html') # Renderiza el nuevo HTM



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
def usuarios (request):
    return render(request, 'pages/Admin/usuarios.html')




#FUNCION QUE SE USA PARA SABER SI ES ADMINISTRADOR
def es_administrador(user):
    return user.is_authenticated and user.rol == 'Administrador'


@login_required
@user_passes_test(es_administrador)
def usuarios_view(request):
    """Vista principal de la administración de usuarios"""
    usuarios = Usuario.objects.all().order_by('id')
    return render(request, 'pages/Admin/usuarios.html', {'usuarios': usuarios})




#CREACION DE USUARIOS
@login_required
@user_passes_test(es_administrador)
@require_POST
def crear_usuario(request):
    """Crea un nuevo usuario"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            with transaction.atomic():
                # Verificar si el usuario o email ya existen
                if Usuario.objects.filter(username=data['usuario']).exists():
                    return JsonResponse({'success': False, 'message': 'El nombre de usuario ya existe'}, status=400)
                
                if Usuario.objects.filter(email=data['email']).exists():
                    return JsonResponse({'success': False, 'message': 'El email ya existe'}, status=400)
                
                # Verificar que las contraseñas coincidan
                if data['password'] != data['confirm_password']:
                    return JsonResponse({'success': False, 'message': 'Las contraseñas no coinciden'}, status=400)
                
                # Crear usuario
                usuario = Usuario.objects.create_user(
                    username=data['usuario'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['nombre'],
                    last_name=data['apellido'],
                    rol=data['rol']
                )
                
                # Devolver datos para actualizar la tabla
                return JsonResponse({
                    'success': True,
                    'message': 'Usuario creado exitosamente',
                    'user': {
                        'id': usuario.id,
                        'first_name': usuario.first_name,
                        'last_name': usuario.last_name,
                        'username': usuario.username,
                        'email': usuario.email,
                        'rol': usuario.rol,
                        'is_active': usuario.is_active
                    }
                })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear usuario: {str(e)}'}, status=500)


print("Vista usuarios_view llamada")  # O "Vista usuarios llamada"



#EDICION DE USUARIOS
@login_required
@user_passes_test(es_administrador)
@require_POST
def actualizar_usuario(request):
    """Actualiza la información de un usuario existente"""
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            with transaction.atomic():
                usuario = get_object_or_404(Usuario, id=data['id'])
              
                # Verificar si el usuario o email ya existen para otro usuario
                if Usuario.objects.filter(username=data['usuario']).exclude(id=data['id']).exists():
                    return JsonResponse({'success': False, 'message': 'El nombre de usuario ya existe'}, status=400)
              
                if Usuario.objects.filter(email=data['email']).exclude(id=data['id']).exists():
                    return JsonResponse({'success': False, 'message': 'El email ya existe'}, status=400)
              
                # Actualizar datos del usuario
                usuario.username = data['usuario']
                usuario.email = data['email']
                usuario.first_name = data['nombre']
                usuario.last_name = data['apellido']
                usuario.rol = data['rol']
              
                # Si se proporciona una nueva contraseña
                if data.get('password') and data.get('password').strip():
                    usuario.set_password(data.get('password'))
              
                usuario.save()
              
                return JsonResponse({
                    'success': True,
                    'message': 'Usuario actualizado exitosamente',
                    'user': {
                        'id': usuario.id,
                        'first_name': usuario.first_name,
                        'last_name': usuario.last_name,
                        'username': usuario.username,
                        'email': usuario.email,
                        'rol': usuario.rol,
                        'is_active': usuario.is_active
                    }
                })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar usuario: {str(e)}'}, status=500)



#EDITAR ESTADO DE UN USUARIO
@login_required
@user_passes_test(es_administrador)
@require_POST
def actualizar_estado_usuario(request, user_id):
    """Actualiza el estado de un usuario (activo/inactivo)"""
    try:
        usuario = get_object_or_404(Usuario, id=user_id)
        data = json.loads(request.body)
        
        # Evitar que se desactive a sí mismo
        if usuario == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'No puedes cambiar tu propio estado'
            }, status=400)
        
        usuario.is_active = data['estado']
        usuario.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario {"activado" if usuario.is_active else "desactivado"} exitosamente'
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error al actualizar estado: {str(e)}'}, status=500)





#ELIMINACION DE USUARIO
@login_required
@user_passes_test(es_administrador)
@require_http_methods(["DELETE"])
def eliminar_usuario(request, user_id):
    """Elimina un usuario del sistema"""
    try:
        usuario = get_object_or_404(Usuario, id=user_id)
        
        # Evitar que se elimine a sí mismo
        if usuario == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'No puedes eliminar tu propia cuenta'
            }, status=400)
        
        nombre_usuario = f"{usuario.first_name} {usuario.last_name}"
        usuario.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario {nombre_usuario} eliminado exitosamente'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error al eliminar usuario: {str(e)}'}, status=500)


# Vista adicional para obtener los detalles de un usuario
@login_required
@user_passes_test(es_administrador)
def obtener_usuario(request, user_id):
    """Obtiene los detalles de un usuario específico"""
    try:
        usuario = get_object_or_404(Usuario, id=user_id)
        return JsonResponse({
            'id': usuario.id,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol,
            'is_active': usuario.is_active
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error al obtener usuario: {str(e)}'}, status=500)


# menu mesero

@never_cache
@login_required
@role_required(['mesero'])
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


def productos_por_categoria(request, categoria):
    productos = Producto.objects.filter(estado='disponible', categoria=categoria)

    try:
        
        template_name = f'pages/productos_menu/{categoria}.html'
        return render(request, template_name, {'productos': productos})
    except:
        return render(request, 'pages/productos_menu/no_encontrado.html', {'categoria': categoria})



#NUMERO DE MESAS
def mesas(request):
    # Puedes definir cuántas mesas quieres aquí
    num_mesas = 12
    # Creamos una lista de números del 1 al num_mesas
    mesas_list = list(range(1, num_mesas + 1)) 
    
    context = {
        'mesas': mesas_list,
    }
    return render(request, 'pages/Admin/mesas.html', context)


# PRODUCTOS

# def productos_disponibles(request):
#     productos = Producto.objects.filter(estado='disponible')
#     return render(request, 'principal/index.html', {'productos': productos})

#EMAIL RESERVA

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
        
#         send_mail(
#             subject='Confirmación de la reserva',
#             message=f'Hola {nombre}, tu reserva fue realizada para el {fecha} a las {hora}.',
#             from_email='correo@gmail.com',  # Remplaza con tu email configurado en settings.py
#             recipient_list=[email],
#             fail_silently=False,
        
#         )
    
#         return JsonResponse({'Success': True})
#     return render(request,'reserva.html')

