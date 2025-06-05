from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, PerfilForm
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.http import FileResponse # <--- ¡IMPORTA FileResponse aquí!
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
import datetime

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


import os
import datetime
import subprocess
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

# Nombre del contenedor docker
DOCKER_DB_CONTAINER = 'postgres_ombu'

def lista_backups(request):
    archivos = os.listdir(BACKUP_DIR)
    archivos.sort(reverse=True)
    return render(request, 'admin/backups.html', {'archivos': archivos})


def crear_backup(request):
    fecha = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{fecha}.sql"
    filepath_host = os.path.join(BACKUP_DIR, filename)

    # Comando dentro del contenedor
    comando = (
        f"docker exec {DOCKER_DB_CONTAINER} pg_dump -U ombu ombu"
    )

    try:
        with open(filepath_host, 'w', encoding='utf-8') as f:
            subprocess.run(comando, shell=True, stdout=f, stderr=subprocess.PIPE, check=True)
        messages.success(request, f'Copia de seguridad creada: {filename}')
    except subprocess.CalledProcessError as e:
        messages.error(request, f'Error al crear backup: {e.stderr.decode()}')

    return redirect('admin_panel:lista_backups')


def restaurar_backup(request, nombre):
    filepath_host = os.path.join(BACKUP_DIR, nombre)

    if not os.path.exists(filepath_host):
        messages.error(request, 'El archivo no existe.')
        return redirect('admin_panel:lista_backups')

    comando = (
        f"type \"{filepath_host}\" | docker exec -i {DOCKER_DB_CONTAINER} psql -U ombu ombu"
    )

    try:
        subprocess.run(comando, shell=True, stderr=subprocess.PIPE, check=True)
        messages.success(request, f'Backup {nombre} restaurado correctamente.')
    except subprocess.CalledProcessError as e:
        messages.error(request, f'Error al restaurar backup: {e.stderr.decode()}')

    return redirect('admin_panel:lista_backups')


def eliminar_backup(request, nombre):
    filepath = os.path.join(BACKUP_DIR, nombre)

    if os.path.exists(filepath):
        os.remove(filepath)
        messages.success(request, f'Backup {nombre} eliminado.')
    else:
        messages.error(request, 'El archivo no existe.')

    return redirect('admin_panel:lista_backups')