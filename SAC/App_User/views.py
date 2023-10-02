from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def formulario_novo_user(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_User.html', {'usuario_logado': usuario_logado})


@login_required
def cadastrar_usuario(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('password')
    usuario_logado = request.user.username

    if usuario is not None and usuario != '' and email is not None and email != '' and senha is not None and senha != '':

        try:
            tem_usuario = User.objects.get(username=usuario)

            if tem_usuario:
                messages.info(request, 'Usuário ' + usuario + ' já existe no sistema. Tente outro nome.')
                return render(request, 'Cad_User.html', {'usuario_logado': usuario_logado})

        except User.DoesNotExist:

            dado_usuario = User.objects.create_user(username=usuario, email=email, password=senha)
            dado_usuario.save()
            messages.info(request, 'Usuário ' + usuario + ' cadastrado com sucesso')
            return render(request, 'Cad_User.html', {'usuario_logado': usuario_logado})

    return render(request, 'Cad_User.html', {'usuario_logado': usuario_logado})
