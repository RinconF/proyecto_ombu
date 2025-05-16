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
# from .models import Reserva
# from django.core.mail import send_mail
import json
from .models import Usuario
from .forms import customusuario_crear, customusuario_change, PasswordChangeForm
from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required

from .decorators import group_required
# from .models import Categoria, Producto, Pedido, Mesa
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
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        
        print(f"Intento de inicio de sesión: username='{username}', password='{password}'")  # Para depurar

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redireccionar según el rol del usuario
                print(f"Inicio de sesión exitoso para: {user.username}, rol: {user.rol}")  # Para depurar
                if user.is_superuser:
                    return redirect('admin:index')  
                elif user.rol == 'ombu':
                    return redirect('dashboard')  # Corregido a 'dashboard' (ver urls.py)
                elif user.rol == 'mesero':  # Nueva condición para mesero
                    return redirect('bebidas_calientes')  # Redirige a la vista de mesero
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
        elif request.user.rol == 'ombu':
            return redirect('dashboard')  # Corregido a 'dashboard'
        elif request.user.rol == 'mesero':  # Nueva condición para mesero
            return redirect('bebidas_calientes')  # Redirige a la vista de mesero
        else:
            return redirect('index')  # Redirige a la página principal por defecto

    return render(request, 'pages/Admin/login.html')

def logout_view(request):
    logout(request)
    return redirect('pages/Admin/login.html') 

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

