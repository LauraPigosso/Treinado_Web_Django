from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Atendente
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required
def abre_index(request):
    usuario_logado = request.user.username
    return render(request, 'index.html', {'usuario_logado': usuario_logado})
@login_required
def cad_cliente(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Cliente.html', {'usuario_logado': usuario_logado})
@login_required
def cons_cliente(request):
    dado_pesquisa_nome = request.POST.get('cliente') if request.POST.get('cliente') else request.GET.get('nome') if request.GET.get('nome') else ""
    dado_pesquisa_telefone = request.POST.get('telefone') if request.POST.get('telefone') else request.GET.get('telefone')  if request.GET.get('telefone') else ""
    dado_pesquisa_email = request.POST.get('email') if request.POST.get('email') else request.GET.get('email') if request.GET.get('email') else ""

    if dado_pesquisa_nome != None and dado_pesquisa_nome != "":
        usuario_logado = request.user.username
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        pages = Paginator(clientes, 3)
        page = request.GET.get('page')
        pagina_atual = pages.get_page(page)
        return render(request, 'cons_cliente_lista.html', {'usuario_logado': usuario_logado}, {'dados_clientes': pagina_atual, 'nome': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email} )

    elif dado_pesquisa_telefone != None and dado_pesquisa_telefone != "":
        usuario_logado = request.user.username
        clientes = Cliente.objects.filter(telefone__icontains=dado_pesquisa_telefone)
        pages = Paginator(clientes, 3)
        page = request.GET.get('page')
        pagina_atual = pages.get_page(page)
        return render(request, 'cons_cliente_lista.html', {'usuario_logado': usuario_logado}, {'dados_clientes': pagina_atual, 'nome': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    elif dado_pesquisa_email != None and dado_pesquisa_email != "":
        usuario_logado = request.user.username
        clientes = Cliente.objects.filter(email__icontains=dado_pesquisa_email)
        pages = Paginator(clientes, 3)
        page = request.GET.get('page')
        pagina_atual = pages.get_page(page)
        return render(request, 'cons_cliente_lista.html', {'usuario_logado': usuario_logado}, {'dados_clientes': pagina_atual, 'nome': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    else:
        usuario_logado = request.user.username
        return render(request, 'cons_cliente_lista.html', {'usuario_logado': usuario_logado})

@login_required
def salvar_cliente_novo(request):
    if (request.method == "POST"):
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')
        grava_cliente = Cliente(nome=nome, telefone=telefone, email=email, observacao=observacao)

    grava_cliente.save()
    usuario_logado = request.user.username
    messages.info(request, 'Cliente' + nome + ' cadastrado com sucesso!')
    return render(request, 'Cad_Cliente.html', {'usuario_logado': usuario_logado})


@login_required
def edit_cliente(request, id):
    usuario_logado = request.user.username
    dados_editar = get_object_or_404(Cliente, pk=id)
    return render(request, 'Edit_Cliente.html', {'dados_do_cliente': dados_editar}, {'usuario_logado': usuario_logado})
@login_required
def salvar_cliente_editado(request):

    if (request.method == 'POST'):
        id_cliente = request.POST.get('id_cliente')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')

        Cliente_Editado = Cliente.objects.get(id=id_cliente)

        Cliente_Editado.nome = nome
        Cliente_Editado.telefone = telefone
        Cliente_Editado.email = email
        Cliente_Editado.observacao = observacao

        Cliente_Editado.save()
        usuario_logado = request.user.username
        messages.info(request, 'Cliente' + nome + 'eidtado com sucesso')
        return render(request, 'Cons_Cliente_Lista.html', {'usuario_logado': usuario_logado})
@login_required
def delete_cliente(request, id):
    cliente_deletado = get_object_or_404(Cliente, pk=id)
    nome = cliente_deletado.nome
    cliente_deletado.delete()

    messages.info(request, 'Cliente' + nome + 'excluido com sucesso')
    return redirect('cons_cliente')

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

    else:

       return render(request, 'Cons_Atendente.html', {'todos_atendentes': todos_atendentes, 'usuario_logado': usuario_logado})

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



