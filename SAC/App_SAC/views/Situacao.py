from django.shortcuts import render, get_object_or_404, redirect
from ..models import Situacao
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def cad_situacao(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Situacao.html', {'usuario_logado': usuario_logado})

@login_required
def salvar_situacao_nova(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
       descricao_situacao = request.POST.get('situacao')
       info_situacao = request.POST.get('informacao')

       grava_situacao = Situacao(
           descricao_situacao=descricao_situacao,
           info_situacao=info_situacao,
           ativo_situacao=1
       )
       grava_situacao.save()
       messages.info(request, 'SItuação ' + descricao_situacao + ' cadastrada com sucesso !!!')
       return render(request, 'Cad_Situacao.html', {'usuario_logado': usuario_logado})

@login_required
def cons_situacao(request):

    dado_pesquisa_situacao = request.POST.get('situacao')
    dado_pesquisa_todos = request.POST.get('seleciona_todos')

    usuario_logado = request.user.username

    page = request.GET.get('page')

    if page :
       #page = request.GET.get('page')
       dado_pesquisa =  request.GET.get('dado_pesquisa')

       if dado_pesquisa != None :
          situacoes_lista = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa)
       else :
          situacoes_lista = Situacao.objects.all()

       paginas = Paginator(situacoes_lista, 3)  # 3 representa o número de atendentes por página
       situacoes = paginas.get_page(page)
       return render(request, 'Cons_Situacao.html', {'todas_situacoes': situacoes, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})


    if dado_pesquisa_todos == 'N' and dado_pesquisa_situacao != None :
       todas_situacoes = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa_situacao)

    elif dado_pesquisa_todos == 'S' and dado_pesquisa_situacao != None :
       todas_situacoes = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa_situacao, ativo_situacao=1)

    elif dado_pesquisa_todos == 'N' and dado_pesquisa_situacao == None :
       todas_situacoes = Situacao.objects.all()

    else:
       todas_situacoes  = Situacao.objects.filter(ativo_situacao=1)

    paginas = Paginator(todas_situacoes, 3)  # 3 representa o número de atendentes por página
    page = request.GET.get('page')
    situacoes = paginas.get_page(page)


    if dado_pesquisa_situacao != None :
       return render(request, 'Cons_Situacao.html', {'todas_situacoes': situacoes, 'dado_pesquisa': dado_pesquisa_situacao, 'usuario_logado': usuario_logado})
    else :
       return render(request, 'Cons_Situacao.html', {'todas_situacoes': situacoes, 'dado_pesquisa': '', 'usuario_logado': usuario_logado})

@login_required
def edit_situacao(request, id):
    dados_situacao_editar = get_object_or_404(Situacao, pk=id)
    usuario_logado = request.user.username

    return render(request, 'Edit_Situacao.html', {'dados_da_situacao': dados_situacao_editar, 'usuario_logado': usuario_logado})


@login_required
def salvar_situacao_editada(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_situacao = request.POST.get('id_situacao')
        descricao_situacao = request.POST.get('descricao_situacao')
        info_situacao = request.POST.get('informacao')
        ativo_situacao = request.POST.get('ativo_situacao')


        Situacao_Editado = Situacao.objects.get(id=id_situacao)

        Situacao_Editado.descricao_situacao = descricao_situacao
        Situacao_Editado.info_situacao = info_situacao


        if ativo_situacao:
            Situacao_Editado.ativo_situacao = 1
        else:
            Situacao_Editado.ativo_situacao = 0

        Situacao_Editado.save()



        messages.info(request, 'Situação ' + descricao_situacao + ' editado com sucesso !!!')
        return render(request, 'Cons_Situacao.html', {'usuario_logado': usuario_logado})
    