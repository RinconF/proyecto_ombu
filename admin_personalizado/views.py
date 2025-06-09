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
import subprocess
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib import messages

# Constantes reutilizables
BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backups')
POSTGRES_CONTAINER = 'postgres_ombu'
DB_NAME = 'ombu'
DB_USER = 'ombu'

# Asegurar que el directorio existe
os.makedirs(BACKUP_DIR, exist_ok=True)

def crear_backup(request):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{timestamp}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)

    try:
        with open(filepath, 'w') as f:
            subprocess.run([
                'docker', 'exec', POSTGRES_CONTAINER,
                'pg_dump', '-U', DB_USER, '-d', DB_NAME
            ], stdout=f, check=True)
        messages.success(request, f"Backup creado: {filename}")
    except Exception as e:
        messages.error(request, f"Error al crear backup: {str(e)}")

    return redirect('admin_panel:lista_backups')


def restaurar_backup(request, nombre):
    filepath = os.path.join(BACKUP_DIR, nombre)

    if not nombre.endswith('.sql') or not os.path.exists(filepath):
        messages.error(request, "Archivo de backup no válido.")
        return redirect('admin_panel:lista_backups')

    try:
        with open(filepath, 'rb') as f:
            subprocess.run([
                'docker', 'exec', '-i', POSTGRES_CONTAINER,
                'psql', '-U', DB_USER, '-d', DB_NAME
            ], stdin=f, check=True)

        # Reiniciar secuencias después de la restauración
        comando_reset = """
        DO $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN
                SELECT c.oid::regclass AS seqname,
                       (pg_get_serial_sequence(t.relname, a.attname)) AS fullseq,
                       t.relname AS tablename,
                       a.attname AS colname
                FROM pg_class c
                JOIN pg_depend d ON d.objid = c.oid
                JOIN pg_class t ON d.refobjid = t.oid
                JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = d.refobjsubid
                WHERE c.relkind = 'S'
            LOOP
                EXECUTE 'SELECT setval(''' || r.fullseq || ''', COALESCE((SELECT MAX(' || r.colname || ') FROM ' || r.tablename || '), 1), true)';
            END LOOP;
        END;
        $$;
        """

        subprocess.run([
            'docker', 'exec', '-i', POSTGRES_CONTAINER,
            'psql', '-U', DB_USER, '-d', DB_NAME
        ], input=comando_reset.encode(), check=True)

        messages.success(request, f"Backup restaurado: {nombre}")
    except Exception as e:
        messages.error(request, f"Error al restaurar backup: {str(e)}")
    
    return redirect('admin_panel:lista_backups')


def lista_backups(request):
    archivos = sorted(
        [f for f in os.listdir(BACKUP_DIR) if f.endswith('.sql')],
        reverse=True
    )
    return render(request, 'admin/backups.html', {'archivos': archivos})


def eliminar_backup(request, nombre):
    filepath = os.path.join(BACKUP_DIR, nombre)

    if not os.path.exists(filepath):
        messages.error(request, "Archivo no encontrado.")
        return redirect('admin_panel:lista_backups')

    try:
        os.remove(filepath)
        messages.success(request, f"Backup eliminado: {nombre}")
    except Exception as e:
        messages.error(request, f"Error al eliminar backup: {str(e)}")
    
    return redirect('admin_panel:lista_backups')