from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, PerfilForm
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.http import FileResponse # <--- ¡IMPORTA FileResponse aquí!

# Si el modelo 'Perfil' está en 'inicio/models.py', impórtalo así:
from inicio.models import Perfil




@login_required
def descargar_manual(request):
    file_path = os.path.join('manual de usuario.docx')
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


@login_required
def perfil_view(request):
    user = request.user
    perfil, creado = Perfil.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            return redirect('perfil')
    else:
        user_form = UsuarioForm(instance=user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'admin/perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })


# @never_cache
# @group_required('ombu')
# def dashboard(request):
# # --- NO SE REALIZA NINGÚN CÁLCULO RELACIONADO CON PEDIDOS AQUÍ ---
#     # Elimina todas las líneas que hacían consultas o agregaciones sobre el modelo Pedido.
#     # Por ejemplo, las variables como total_ventas_hoy, num_pedidos_hoy,
#     # ventas_semanales_data_qs, top_mesas, etc.

#     # Obtener las 10 últimas actividades de TU modelo ActividadReciente
#     actividades_recientes = ActividadReciente.objects.order_by('-fecha_hora')[:10]

#     context = {
#         # --- Solo pasamos la actividad reciente y cualquier otra variable NO relacionada con Pedidos ---
#         'actividades_recientes': actividades_recientes,
#         # Si tienes otras métricas o datos que NO provienen de Pedidos y quieres mostrar, agrégalas aquí.
#         # Por ejemplo: 'total_usuarios': Usuario.objects.count(),
#         # 'total_productos': Producto.objects.count(),
#     }

#     # Esta vista renderiza la plantilla que está en admin_personalizado/templates/
#     return render(request, 'admin/dashboard.html', context)    
    
    
    
    
#     # # Ventas por mes
#     # hoy = datetime.date.today()
#     # ventas_mensuales = []
#     # ventas_mensuales_labels = []
#     # ventas_mensuales_data = []

#     # for i in range(1, 13):
#     #     total = Pedido.objects.filter(fecha__month=i).aggregate(Sum('total'))['total__sum'] or 0
#     #     ventas_mensuales.append({'month': calendar.month_name[i], 'total': float(total)})
#     #     ventas_mensuales_labels.append(calendar.month_name[i])
#     #     ventas_mensuales_data.append(float(total))

#     # # Top mesas más usadas
#     # mesas_usadas = (
#     #     Pedido.objects.values('mesa__numero')
#     #     .annotate(total=Count('id'))
#     #     .order_by('-total')[:5]
#     # )

#     # # Top productos más vendidos
#     # productos_vendidos = (
#     #     Producto.objects.annotate(total=Count('pedido'))
#     #     .order_by('-total')[:5]
#     # )

#     # # Cálculos simples para los 4 recuadros:
#     # ventas_totales = Pedido.objects.aggregate(Sum('total'))['total__sum'] or 0
#     # hoy = datetime.date.today()
#     # ventas_dia = Pedido.objects.filter(fecha__date=hoy).aggregate(Sum('total'))['total__sum'] or 0
#     # ventas_mes = Pedido.objects.filter(fecha__month=hoy.month).aggregate(Sum('total'))['total__sum'] or 0
#     # ventas_anio = Pedido.objects.filter(fecha__year=hoy.year).aggregate(Sum('total'))['total__sum'] or 0

#     # return render(request, 'dashboard.html', {
#     #     'ventas_mensuales_labels': ventas_mensuales_labels,
#     #     'ventas_mensuales_data': ventas_mensuales_data,
#     #     'mesas_usadas': mesas_usadas,
#     #     'productos_vendidos': productos_vendidos,
#     #     'ventas_totales': ventas_totales,
#     #     'ventas_dia': ventas_dia,
#     #     'ventas_mes': ventas_mes,
#     #     'productos_top': productos_top,
#     #     'mesas_top': mesas_top,
#     #     'ventas_labels': ventas_labels,
#     #     'ventas_data': ventas_data,
#     # })

#     # return render(request, 'pages/Admin/dashboard.html', context)
