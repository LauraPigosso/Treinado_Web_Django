from django.shortcuts import render, get_object_or_404, redirect
from ..models import Atendente
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def cad_atend(request):
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})


@login_required
def salvar_atend_novo(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
       nome_atend = request.POST.get('nome_atend')
       telefone_atend = request.POST.get('telefone_atend')
       user_atend = request.POST.get('user_atend')
       observacao_atend = request.POST.get('observacao_atend')
       if user_atend:
          user_atend=User.objects.get(username=user_atend)
       else:
          user_atend = None # Define a variável como Null

       grava_atend = Atendente(
           nome_atend=nome_atend,
           telefone_atend=telefone_atend,
           observacao_atend=observacao_atend,
           ativo_atend=1,
           user_atend=user_atend
           #user_atend = User.objects.get(username=user_atend)  # must be a "User" instance
       )
       grava_atend.save()
       messages.info(request, 'Atendente ' + nome_atend + ' cadastrado com sucesso.')
       cons_users = User.objects.all()
       return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})

@login_required
def cons_atend(request):

    dado_pesquisa_atendente = request.POST.get('atendente')
    dado_pesquisa_todos = request.POST.get('seleciona_todos')

    usuario_logado = request.user.username

    if dado_pesquisa_todos == 'N' and dado_pesquisa_atendente != None :
       todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)

    elif dado_pesquisa_todos == 'S' and dado_pesquisa_atendente != None :
       todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente , ativo_atend=1)

    elif dado_pesquisa_todos == 'N' and dado_pesquisa_atendente == None :
       todos_atendentes = Atendente.objects.all()

    else:
       todos_atendentes  = Atendente.objects.filter(ativo_atend=1)

    page = request.GET.get('page')

    if page :
       #page = request.GET.get('page')
       dado_pesquisa =  request.GET.get('dado_pesquisa')
       atendentes_lista = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa)
       paginas = Paginator(atendentes_lista, 3)  # 3 representa o número de atendentes por página
       atendentes = paginas.get_page(page)
       return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})

    if dado_pesquisa_atendente != None and dado_pesquisa_atendente != '':
       todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)
       paginas = Paginator(todos_atendentes, 3) # 3 representa o número de atendentes por página
       page = request.GET.get('page')
       atendentes = paginas.get_page(page)
       return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente, 'usuario_logado': usuario_logado})

    paginas = Paginator(todos_atendentes, 3)  # 3 representa o número de atendentes por página
    page = request.GET.get('page')
    atendentes = paginas.get_page(page)

    if dado_pesquisa_atendente != None:
        return render(request, 'Cons_Atendente.html',
                      {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente, 'usuario_logado': usuario_logado})
    else:
        return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': '', 'usuario_logado': usuario_logado})


@login_required
def edit_atend(request, id):
    dados_editar = get_object_or_404(Atendente, pk=id)
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    return render(request, 'Edit_Atendente.html', {'dados_do_atendente': dados_editar, 'cons_users': cons_users , 'usuario_logado': usuario_logado})

@login_required
def salvar_atend_editado(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_atend = request.POST.get('id_atend')
        nome_atend = request.POST.get('nome_atend')
        telefone_atend = request.POST.get('telefone_atend')
        user_atend = request.POST.get('user_atend')
        observacao_atend = request.POST.get('observacao_atend')
        ativo_atend = request.POST.get('ativo_atend')

        if user_atend:
            user_atend = User.objects.get(username=user_atend)
        else:
            user_atend = None  # Define a variável como Null

        Atende_Editado = Atendente.objects.get(id=id_atend)
        Atende_Editado.nome_atend = nome_atend
        Atende_Editado.telefone_atend = telefone_atend
        Atende_Editado.observacao_atend = observacao_atend
        Atende_Editado.user_atend = user_atend

        if ativo_atend:
            Atende_Editado.ativo_atend = 1
        else:
            Atende_Editado.ativo_atend = 0

        Atende_Editado.save()

        messages.info(request, 'Atendente ' + nome_atend + ' editado com sucesso.')
        return render(request, 'Cons_Atendente.html', {'usuario_logado': usuario_logado})
