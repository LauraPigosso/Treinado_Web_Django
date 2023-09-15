from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
@login_required
def formulario_novo_user(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_user.html', {'usuario_logado': usuario_logado})


@login_required
def cadastrar_usuario(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    usuario_logado = request.user.username

    if usuario != None and usuario != '' and email != None and email != '' and senha != None and senha != '':

        try:
            tem_usuario = User.objects.get(username = usuario)

            if tem_usuario:
                messages.info(request, 'Usuario' + 'já existe no sistema. Tente outro nome')
                return render(request, 'Cad_user.html', {'usuario_logado': usuario_logado})

        except User.DoesNotExist:

            dados_usuario = User.objects.create_user(username=usuario, email=email, password=senha)
            dados_usuario.save()
            messages.info(request, 'Usuario ' + 'cadastrado com sucesso')
            return render(request, 'Cad_user.html', {'usuario_logado': usuario_logado})



