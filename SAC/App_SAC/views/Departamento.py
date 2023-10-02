from django.shortcuts import render, get_object_or_404, redirect
from ..models import Departamento
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def cad_depto(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Depto.html', {'usuario_logado': usuario_logado})

@login_required
def salvar_depto_novo(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
       descricao_departamento = request.POST.get('depto')
       info_departamento = request.POST.get('informacao')

       grava_depto = Departamento(
           descricao_departamento=descricao_departamento,
           info_departamento=info_departamento,
           ativo_departamento=1
       )
       grava_depto.save()
       messages.info(request, 'Departamento ' + descricao_departamento + ' cadastrado com sucesso.')
       return render(request, 'Cad_Depto.html', {'usuario_logado': usuario_logado})

@login_required
def cons_depto(request):

    dado_pesquisa_depto = request.POST.get('departamento')
    usuario_logado = request.user.username

    if dado_pesquisa_depto != '' and dado_pesquisa_depto != None:
        todos_departamentos = Departamento.objects.filter(descricao_departamento__icontains=dado_pesquisa_depto)
        return render(request, 'Cons_Depto.html', {'todos_departamentos': todos_departamentos, 'dado_pesquisa': dado_pesquisa_depto, 'usuario_logado': usuario_logado})
    else:
        todos_departamentos = Departamento.objects.all()
        return render(request, 'Cons_Depto.html', {'todos_departamentos': todos_departamentos, 'dado_pesquisa': dado_pesquisa_depto, 'usuario_logado': usuario_logado})

@login_required
def edit_depto(request, id):
    dados_depto_editar = get_object_or_404(Departamento, pk=id)
    usuario_logado = request.user.username
    return render(request, 'Edit_Depto.html', {'dados_do_depto': dados_depto_editar, 'usuario_logado': usuario_logado})



@login_required
def salvar_depto_editado(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_depto = request.POST.get('id_depto')
        descricao_departamento = request.POST.get('depto')
        info_departamento = request.POST.get('informacao')

        print("="*30)
        print(request.__dict__)
        print("="*30)

        Departamento_Editado = Departamento.objects.get(id=id_depto)

        Departamento_Editado.descricao_departamento = descricao_departamento
        Departamento_Editado.info_departamento = info_departamento

        Departamento_Editado.save()

        messages.info(request, 'Departamento ' + descricao_departamento + ' editado com sucesso.')
        return render(request, 'Cons_Depto.html', {'usuario_logado': usuario_logado})
