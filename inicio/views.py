from django.shortcuts import render
from django.http import JsonResponse
import json


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
    return render(request, 'pages/Admin/dasboard.html')

def login (request):
    return render(request, 'pages/Admin/login.html')

def mesas (request):
    return render(request, 'pages/Admin/mesas.html')

def reserva (request):
    return render(request, 'pages/Admin/reserva.html')

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

#Productos y mesa id para toma de pedidos

def bebidas_calientes(request, mesa_id):
    context = {'mesa_id': mesa_id}
    return render(request, 'pages/menu_mesero/bebidas_calientes.html', context)

def bebidas_frias(request, mesa_id):
    context = {'mesa_id': mesa_id}
    return render(request, 'pages/menu_mesero/bebidas_frias.html', context)

def Cervezas(request, mesa_id):
    context = {'mesa_id': mesa_id}
    return render(request, 'pages/menu_mesero/Cervezas.html', context)

def Cigarrillos(request, mesa_id):
    context = {'mesa_id': mesa_id}
    return render(request, 'pages/menu_mesero/Cigarrillos.html', context)

def Cocteles(request, mesa_id):
    context = {'mesa_id': mesa_id}
    return render(request, 'pages/menu_mesero/Cocteles.html', context)

def Para_picar(request, mesa_id):
    context = {'mesa_id': mesa_id}
    return render(request, 'pages/menu_mesero/Para_picar.html', context)


# Vista para recibir los pedidos
def agregar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mesa_id = data.get('mesa_id')
            productos = data.get('productos')  # Suponemos que envías una lista de productos con cantidades

            # Aquí podrías realizar la lógica para guardar el pedido en la base de datos
            # utilizando tus modelos (por ejemplo, crear un modelo Pedido, y luego
            # para cada producto en la lista, crear un modelo ItemPedido relacionado).

            # Por ahora, vamos a simular que el pedido se recibió correctamente
            print(f"Pedido recibido para la mesa {mesa_id}: {productos}")

            # En una implementación real, aquí guardarías los datos en la base de datos

            return JsonResponse({'status': 'success', 'message': 'Pedido recibido correctamente.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al decodificar el JSON del pedido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)