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

from .models import Mesa, Producto, Pedido, PedidoDetalle

# from .models import Reserva
# from django.core.mail import send_mail
import json
from .models import Usuario,Producto,GaleriaFoto
from .forms import CustomUserCreationForm, CustomUserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .models import ActividadReciente
from .decorators import group_required
# from .models import Categoria, Producto, Pedido, Mesa
from django.db.models import Sum, Count
import datetime
import calendar
from django.utils.timezone import now
# # import openpyxl
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from django.utils.dateformat import DateFormat
from .decorators import group_required
from django.db.utils import ProgrammingError
from admin_personalizado import templates
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext as _





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
                login(request, user) # Usa la función 'login' de Django para autenticar al usuario en la sesión

                # Captura el parámetro 'next' si existe en la URL o en el POST del formulario
                next_url = request.POST.get('next') or request.GET.get('next')

                # Redireccionar según el rol del usuario
                if user.is_superuser or (user.rol.lower() == 'administrador' and user.is_staff) or user.rol.lower() == 'ombu':
                    # Si el usuario es admin y hay una URL 'next', redirigimos ahí.
                    # Si no hay 'next', redirigimos al índice del admin.
                    return redirect(next_url or 'admin:index') 
                elif user.rol.lower() == 'mesero':
                    return redirect('mesero_principal') 
                else:
                    return redirect('index') 
            else:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    # Si el usuario ya está autenticado, redirigir según su rol
    if request.user.is_authenticated:
        # Captura el parámetro 'next' si existe, incluso si ya está autenticado
        next_url = request.POST.get('next') or request.GET.get('next')

        if request.user.is_superuser or (request.user.rol.lower() == 'administrador' and request.user.is_staff) or request.user.rol.lower() == 'ombu':
            return redirect(next_url or 'admin:index') 
        elif request.user.rol.lower() == 'mesero':
            return redirect('mesero_principal') 
        else:
            return redirect('index') 

    return render(request, 'pages/Admin/login.html') # Asegúrate que esta sea la ruta correcta a tu plantilla de login personalizada.

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


# @never_cache
# @staff_member_required # Asegura que solo el personal del admin pueda acceder a esta vista
# def dashboard(request): # Renombrado a dashboard_view para consistencia
#     # Obtener las 10 actividades administrativas más recientes
#     recent_activities = LogEntry.objects.order_by('-action_time')[:10]

#     # Formatear las actividades para mostrarlas en el template
#     formatted_activities = []
#     for entry in recent_activities:
#         action_detail_message = ""

#         # Usar get_text_for_log_entry para obtener una descripción más detallada
#         # Si no tienes esta función, puedes usar object_repr
#         object_display_name = str(entry.get_admin_url(entry.content_type_id, entry.object_id, entry.object_repr)) \
#                               if entry.content_type and entry.object_id and entry.object_repr \
#                               else (entry.object_repr if entry.object_repr else _("un objeto desconocido"))

#         # Determinar la acción principal y la descripción inicial
#         if entry.is_addition():
#             action_description = _(f"Añadido '{object_display_name}'")
#         elif entry.is_change():
#             action_description = _(f"Modificado '{object_display_name}'")
#             if entry.change_message:
#                 try:
#                     message_data = json.loads(entry.change_message)

#                     if isinstance(message_data, list):
#                         for msg in message_data:
#                             if 'changed' in msg and 'fields' in msg['changed']:
#                                 changed_fields = ', '.join(msg['changed']['fields'])
#                                 action_detail_message = _(f"Se actualizaron los campos: {changed_fields}.")
#                             elif 'added' in msg and 'name' in msg['added'] and 'object' in msg['added']:
#                                 added_name = msg['added']['name'] # Nombre del campo relacionado (ej. 'permissions')
#                                 added_object = msg['added']['object'] # Representación del objeto añadido (ej. 'can_view_report')
#                                 action_detail_message = _(f"Se añadió '{added_object}' a '{added_name}'.")
#                             elif 'deleted' in msg and 'name' in msg['deleted'] and 'object' in msg['deleted']:
#                                 deleted_name = msg['deleted']['name']
#                                 deleted_object = msg['deleted']['object']
#                                 action_detail_message = _(f"Se eliminó '{deleted_object}' de '{deleted_name}'.")
#                     else:
#                         if entry.change_message.strip():
#                             action_detail_message = _(f"Detalles del cambio: {entry.change_message.strip()}.")

#                 except json.JSONDecodeError:
#                     if entry.change_message.strip():
#                         action_detail_message = _(f"Detalles del cambio: {entry.change_message.strip()}.")
#                     else:
#                         action_detail_message = _("No se especificaron detalles del cambio.")
#         elif entry.is_deletion():
#             action_description = _(f"Eliminado '{object_display_name}'")
#         else:
#             action_description = _(f"Acción desconocida sobre '{object_display_name}'")


#         final_action_text = action_description
#         if action_detail_message:
#             final_action_text += f": {action_detail_message}"

#         # Añadir quién realizó la acción
#         final_action_text += f" por {entry.user.username}"

#         formatted_activities.append({
#             'accion': final_action_text,
#             'fecha_hora': entry.action_time,
#         })

#     context = {
#         'title': 'Dashboard Administrativo OMBÚ', # Título que aparecerá en el breadcrumbs
#         'actividades_recientes': formatted_activities,
#     }
#     # LA RUTA DE LA PLANTILLA ES CLAVE AQUÍ: APUNTA A LA APP admin_personalizado
#     return render(request, 'admin/dashboard.html', context)
    
    
    
    
    # # Ventas por mes
    # hoy = datetime.date.today()
    # ventas_mensuales = []
    # ventas_mensuales_labels = []
    # ventas_mensuales_data = []

    # for i in range(1, 13):
    #     total = Pedido.objects.filter(fecha__month=i).aggregate(Sum('total'))['total__sum'] or 0
    #     ventas_mensuales.append({'month': calendar.month_name[i], 'total': float(total)})
    #     ventas_mensuales_labels.append(calendar.month_name[i])
    #     ventas_mensuales_data.append(float(total))

    # # Top mesas más usadas
    # mesas_usadas = (
    #     Pedido.objects.values('mesa__numero')
    #     .annotate(total=Count('id'))
    #     .order_by('-total')[:5]
    # )

    # # Top productos más vendidos
    # productos_vendidos = (
    #     Producto.objects.annotate(total=Count('pedido'))
    #     .order_by('-total')[:5]
    # )

    # # Cálculos simples para los 4 recuadros:
    # ventas_totales = Pedido.objects.aggregate(Sum('total'))['total__sum'] or 0
    # hoy = datetime.date.today()
    # ventas_dia = Pedido.objects.filter(fecha__date=hoy).aggregate(Sum('total'))['total__sum'] or 0
    # ventas_mes = Pedido.objects.filter(fecha__month=hoy.month).aggregate(Sum('total'))['total__sum'] or 0
    # ventas_anio = Pedido.objects.filter(fecha__year=hoy.year).aggregate(Sum('total'))['total__sum'] or 0

    # return render(request, 'dashboard.html', {
    #     'ventas_mensuales_labels': ventas_mensuales_labels,
    #     'ventas_mensuales_data': ventas_mensuales_data,
    #     'mesas_usadas': mesas_usadas,
    #     'productos_vendidos': productos_vendidos,
    #     'ventas_totales': ventas_totales,
    #     'ventas_dia': ventas_dia,
    #     'ventas_mes': ventas_mes,
    #     'productos_top': productos_top,
    #     'mesas_top': mesas_top,
    #     'ventas_labels': ventas_labels,
    #     'ventas_data': ventas_data,
    # })

    # return render(request, 'pages/Admin/dashboard.html', context)






def admin_login_page(request):
    return render(request, 'pages/Admin/login.html')


# mesas----------------------------------------------------------------------------------------------
@never_cache
@login_required
def mesas(request):
    # **** CAMBIO CLAVE AQUI ****
    # Solo recuperamos las mesas que están activas
    mesas_activas = Mesa.objects.filter(is_active=True).order_by('numero')
    context = {
        'mesas': mesas_activas,
        'selected_page': 'mesas'
    }
    return render(request, 'mesas.html', context)


@login_required
@group_required(['Administrador'])
@require_POST
def eliminar_mesa_logicamente(request, mesa_id):
    """
    Vista para marcar una mesa como inactiva (eliminación lógica).
    """
    try:
        mesa = get_object_or_404(Mesa, pk=mesa_id)
        mesa.is_active = False # Marcar como inactiva
        mesa.save()
        # Registrar actividad
        ActividadReciente.objects.create(
            usuario=request.user,
            accion=f'Desactivó la Mesa {mesa.numero} (ID: {mesa.id})'
        )
        messages.success(request, f'Mesa {mesa.numero} desactivada correctamente.')
    except Exception as e:
        messages.error(request, f'Error al desactivar la mesa: {e}')
    return redirect('mesas') # Redirige a la vista principal de mesas


@login_required
@group_required(['Administrador'])
@require_http_methods(["GET", "POST"]) # Permitimos GET para mostrar el formulario y POST para procesarlo
def gestionar_mesa(request):
    """
    Vista para agregar una nueva mesa o reactivar una existente.
    """
    if request.method == 'POST':
        numero_mesa = request.POST.get('numero')
        capacidad_mesa = request.POST.get('capacidad')
        
        if not numero_mesa or not capacidad_mesa:
            messages.error(request, 'El número y la capacidad de la mesa son obligatorios.')
            return redirect('gestionar_mesa') # Redirige de nuevo a la página de gestión si faltan datos

        try:
            numero_mesa = int(numero_mesa)
            capacidad_mesa = int(capacidad_mesa)

            # Intentar encontrar una mesa existente (activa o inactiva) con ese número
            mesa_existente = Mesa.objects.filter(numero=numero_mesa).first()

            if mesa_existente:
                if not mesa_existente.is_active:
                    # Si existe pero está inactiva, la reactivamos
                    mesa_existente.is_active = True
                    mesa_existente.capacidad = capacidad_mesa
                    mesa_existente.estado = 'disponible' # Asegurar que esté disponible al reactivar
                    mesa_existente.save()
                    messages.success(request, f'Mesa {numero_mesa} reactivada correctamente (ID: {mesa_existente.id}).')
                    # Registrar actividad
                    ActividadReciente.objects.create(
                        usuario=request.user,
                        accion=f'Reactivó la Mesa {mesa_existente.numero} (ID: {mesa_existente.id})'
                    )
                else:
                    # Si existe y ya está activa, es una advertencia o error
                    messages.warning(request, f'Ya existe una Mesa {numero_mesa} activa.')
                    # Puedes redirigir a una página de edición o simplemente volver
                    return redirect('mesas') # O a la página de gestión
            else:
                # Si no existe ninguna mesa con ese número, creamos una nueva
                nueva_mesa = Mesa.objects.create(
                    numero=numero_mesa,
                    capacidad=capacidad_mesa,
                    is_active=True,
                    estado='disponible'
                )
                messages.success(request, f'Mesa {numero_mesa} agregada correctamente (ID: {nueva_mesa.id}).')
                # Registrar actividad
                ActividadReciente.objects.create(
                    usuario=request.user,
                    accion=f'Agregó una nueva Mesa {nueva_mesa.numero} (ID: {nueva_mesa.id})'
                )
        except ValueError:
            messages.error(request, 'El número y la capacidad de la mesa deben ser números enteros.')
        except Exception as e:
            messages.error(request, f'Error al gestionar la mesa: {e}')

        return redirect('mesas') # Redirige a la vista principal de mesas después de la operación
    else:
        # Si es un GET, renderiza un formulario simple para añadir/reactivar mesas
        # Esto es opcional, si ya lo haces desde el admin puedes omitir esta parte de la vista o hacerla más compleja
        return render(request, 'gestionar_mesa.html', {'selected_page': 'mesas'}) # Necesitarás crear este HTML


# fin mesas-----------------------------------------------------------------------------------------------------------
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
    productos = Producto.objects.filter(estado='disponible', categoria='bebida_caliente')
    return render(request, 'pages/menu_mesero/bebidas_calientes.html', {'productos': productos})


@never_cache
@login_required
def bebidas_frias(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Bebida_fria')
    return render(request, 'pages/menu_mesero/bebidas_frias.html', {'productos': productos})


@never_cache
@login_required
def cervezas(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Cerveza')
    return render(request, 'pages/menu_mesero/Cervezas.html', {'productos': productos})

@never_cache
@login_required
def cigarrillos(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Cigarrillo')
    return render(request, 'pages/menu_mesero/Cigarrillos.html', {'productos': productos})

@never_cache
@login_required
def cocteles(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Coctel')
    return render(request, 'pages/menu_mesero/Cocteles.html', {'productos': productos})

@never_cache
@login_required
def para_picar(request):
    productos = Producto.objects.filter(estado='disponible', categoria='Picar')
    return render(request, 'pages/menu_mesero/Para_picar.html', {'productos': productos})


# def productos_por_categoria(request, categoria):
#     productos = Producto.objects.filter(estado='disponible', categoria=categoria)

#     try:
        
#         template_name = f'pages/menu_mesero/{categoria}.html'
#         return render(request, template_name, {'productos': productos})
#     except:
#         return render(request, 'pages/menu_mesero/no_encontrado.html', {'categoria': categoria})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

template_map = {
    'bebida_caliente': {
        'cliente': 'pages/productos_menu/bebida_caliente.html',
        'mesero': 'pages/menu_mesero/bebidas_calientes.html',
    },
    'Bebida_fria': {
        'cliente': 'pages/productos_menu/bebida_fria.html',
        'mesero': 'pages/menu_mesero/bebidas_frias.html',
    },
    'Coctel': {
        'cliente': 'pages/productos_menu/Coctel.html',
        'mesero': 'pages/menu_mesero/Cocteles.html',
    },
    'Cerveza': {
        'cliente': 'pages/productos_menu/Cervezas.html',
        'mesero': 'pages/menu_mesero/CervezasArtesanales.html',
    },
    'Cigarrillo': {
        'cliente': 'pages/productos_menu/Cigarrillo.html',
        'mesero': 'pages/menu_mesero/Cigarrillos.html',
    },
    'Picar': {
        'cliente': 'pages/productos_menu/Picar.html',
        'mesero': 'pages/menu_mesero/Para_picar.html',
    },
}

def productos_cliente(request, categoria):
    productos = Producto.objects.filter(estado='disponible', categoria=categoria)
    template_path = template_map.get(categoria, {}).get('cliente')
    
    if template_path:
        return render(request, template_path, {'productos': productos})
    
    return render(request, 'pages/productos_menu/no_encontrado.html', {
        'categoria': categoria,
        'tipo': 'cliente',
    })

# Vista para meseros (interfaz interna)
def productos_mesero(request, categoria):
    productos = Producto.objects.filter(estado='disponible', categoria=categoria)
    template_path = template_map.get(categoria, {}).get('mesero')
    
    if template_path:
        return render(request, template_path, {'productos': productos})
    
    return render(request, 'pages/productos_menu/no_encontrado.html', {
        'categoria': categoria,
        'tipo': 'mesero',
    })




# Vista para manejar fotos de index
def index(request):
    
    # Opción 1: Obtener las dos fotos más recientes
    galeria_fotos = GaleriaFoto.objects.all().order_by('-fecha_subida')[:2]

    # Opción 2: Obtener las dos fotos marcadas como principales (si existen)
    # Si tienes más de 2 principales y quieres solo 2, ajusta el orden o la lógica.
    # galeria_fotos = GaleriaFoto.objects.filter(es_principal=True).order_by('-fecha_subida')[:2]

    context = {
        'galeria_fotos': galeria_fotos
    }
    return render(request, 'pages/principal/index.html', context)


#NUMERO DE MESAS
def mesas(request):
    mesas = Mesa.objects.all().order_by('numero')  # Ordenar por número para mostrar ordenadas
    context = {
        'mesas': mesas,
    }
    return render(request, 'pages/Admin/mesas.html', context)










# -----------------------------------------------------------PEDIDOS------------------------------------



@require_POST # Asegura que solo se acepta el método POST
@csrf_exempt # Considera quitar esto en producción y usar el token CSRF apropiadamente
def guardar_pedido(request):
    try:
        data = json.loads(request.body)
        
        mesa_id = data.get('mesa_id')
        items = data.get('items')
        total_recibido = data.get('total')
        medio_pago = data.get('medio_pago')

        if not mesa_id or not items:
            return JsonResponse({'error': 'Faltan datos en el pedido (mesa_id o items).'}, status=400)

        if not isinstance(items, list) or len(items) == 0:
            return JsonResponse({'error': 'El pedido no contiene productos válidos.'}, status=400)

        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            return JsonResponse({'error': 'La mesa seleccionada no existe.'}, status=404)

        # Usar una transacción para asegurar la atomicidad de la operación
        with transaction.atomic():
            # Obtener el mesero actual si el usuario está autenticado y es un mesero
            mesero = None
            if request.user.is_authenticated and hasattr(request.user, 'rol') and request.user.rol == 'mesero':
                mesero = request.user # Asume que request.user es una instancia de tu modelo Usuario

            # Crear el pedido principal
            pedido = Pedido.objects.create(
                mesa=mesa,
                total=total_recibido, # Usar el total calculado desde el frontend, se puede recalcular para validación
                mesero=mesero,
                medio_pago=medio_pago,
                estado='finalizado' # Establecemos el estado a 'finalizado' directamente aquí
            )

            total_calculado_backend = 0
            # Crear los detalles del pedido
            for item_data in items:
                producto_id = item_data.get('producto_id')
                cantidad = item_data.get('cantidad')
                precio_unitario_recibido = item_data.get('precio_unitario')

                if not producto_id or not cantidad or cantidad <= 0:
                    raise ValueError(f"Datos de producto inválidos: {item_data}")

                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    raise ValueError(f"Producto con ID {producto_id} no encontrado.")
                
                # Opcional: Validar que el precio_unitario recibido coincida con el del producto en BD
                # Esto es importante para evitar manipulaciones de precios desde el cliente
                if float(precio_unitario_recibido) != float(producto.precio):
                    # Podrías decidir usar el precio de la BD o lanzar un error
                    # Para este ejemplo, usaremos el de la BD para mayor seguridad
                    precio_para_detalle = producto.precio
                    # print(f"Advertencia: Precio de producto {producto.titulo} difiere. Usando precio de BD: {producto.precio}")
                else:
                    precio_para_detalle = precio_unitario_recibido

                PedidoDetalle.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_para_detalle
                )
                total_calculado_backend += (precio_para_detalle * cantidad)
            
            # Opcional: Validar que el total calculado en el backend coincida con el del frontend
            # Puedes tener una pequeña tolerancia debido a problemas de precisión de flotantes
            if abs(total_calculado_backend - float(total_recibido)) > 0.01:
                print(f"Advertencia: Discrepancia en el total. Frontend: {total_recibido}, Backend: {total_calculado_backend}")
                # return JsonResponse({'error': 'Discrepancia en el total del pedido.'}, status=400)
                # O podrías simplemente actualizar el total del pedido con el calculado en backend
                pedido.total = total_calculado_backend
                pedido.save()


            # Registrar actividad reciente
            accion_log = f'Finalizó pedido #{pedido.id} para la Mesa {mesa.numero} (Total: ${pedido.total:.2f}, Pago: {medio_pago}).'
            ActividadReciente.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                accion=accion_log
            )

            return JsonResponse({'message': f'Pedido #{pedido.id} finalizado y guardado correctamente.'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Solicitud JSON inválida.'}, status=400)
    except ValueError as e: # Captura los errores de validación personalizados
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        # Esto capturará cualquier otro error inesperado
        print(f"Error inesperado al guardar pedido: {e}")
        return JsonResponse({'error': 'Error interno del servidor al procesar el pedido.'}, status=500)




# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt  # temporal para evitar problemas de CSRF
# def guardar_pedido(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print('Datos recibidos:', data)  # para debug en consola
#             # Aquí debes procesar y guardar el pedido en la BD
#             return JsonResponse({'message': 'Pedido guardado correctamente'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)
