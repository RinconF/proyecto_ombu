from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, PerfilForm

@login_required
def perfil_view(request):
    user = request.user
    perfil = user.perfil

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
