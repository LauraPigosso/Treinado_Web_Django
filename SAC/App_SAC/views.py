from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Atendente, Departamento
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
def salvar_cliente_novo(request):
    if (request.method == 'POST'):
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')  # dados igual do bd
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')
        grava_cliente = Cliente(  # Instância obj cliente
            nome=nome,
            telefone=telefone,
            email=email,
            observacao=observacao
        )

        grava_cliente.save()  # salva no banco de dados
        messages.info(request, 'Cliente ' + nome + ' cadastrado com sucesso!!!')  # mensagem aviso
        usuario_logado = request.user.username

        return render(request, 'Cad_Cliente.html', {'usuario_logado': usuario_logado})


@login_required
def cons_cliente(request):
    dado_pesquisa_nome = request.POST.get('cliente') if request.POST.get('cliente') else request.GET.get(
        'cliente') if request.GET.get('cliente') else ""
    dado_pesquisa_telefone = request.POST.get('telefone') if request.POST.get('telefone') else request.GET.get(
        'telefone') if request.GET.get('telefone') else ""
    dado_pesquisa_email = request.POST.get('email') if request.POST.get('email') else request.GET.get(
        'email') if request.GET.get('email') else ""

    if dado_pesquisa_nome != None and dado_pesquisa_nome != '':
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente_Lista.html',
                      {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome,
                       'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    elif dado_pesquisa_telefone != None and dado_pesquisa_telefone != '':
        clientes = Cliente.objects.filter(telefone__icontains=dado_pesquisa_telefone)
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente_Lista.html',
                      {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome,
                       'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    elif dado_pesquisa_email != None and dado_pesquisa_email != '':
        clientes = Cliente.objects.filter(email__icontains=dado_pesquisa_email)
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente_Lista.html',
                      {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome,
                       'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})
    else:
        usuario_logado = request.user.username
        return render(request, 'Cons_Cliente_Lista.html', {'usuario_logado': usuario_logado})


def listing(request):
    cliente_list = Cliente.objects.all()
    paginator = Paginator(cliente_list, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "Cons_Cliente_Lista2", {"page_obj": page_obj})


@login_required
def edit_cliente(request, id):
    dados_editar = get_object_or_404(Cliente, pk=id)
    return render(request, 'Edit_Cliente.html', {'dados_do_cliente': dados_editar})


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

        messages.info(request, 'Cliente ' + nome + ' editado com sucesso!')
        return render(request, 'Cons_Cliente_Lista.html')


@login_required
def delete_cliente(request, id):
    cliente_deletado = get_object_or_404(Cliente, pk=id)
    nome = cliente_deletado.nome
    cliente_deletado.delete()
    messages.info(request, 'Cliente ' + nome + ' excluído com successo!')
    return redirect('cons_cliente')


# =================================Atendentes==========================================

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
            user_atend = User.objects.get(username=user_atend)
        else:
            user_atend = None

        grava_atend = Atendente(
            nome_atend=nome_atend,
            telefone_atend=telefone_atend,
            observacao_atend=observacao_atend,
            ativo_atend=1,
            user_atend=user_atend
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

    if dado_pesquisa_todos == 'N' and dado_pesquisa_atendente != None:
        todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)

    elif dado_pesquisa_todos == 'S' and dado_pesquisa_atendente != None:
        todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente, ativo_atend=1)

    elif dado_pesquisa_todos == 'N' and dado_pesquisa_atendente == None:
        todos_atendentes = Atendente.objects.all()

    else:
        todos_atendentes = Atendente.objects.filter(ativo_atend=1)

    page = request.GET.get('page')

    if page:
        # page = request.GET.get('page')
        dado_pesquisa = request.GET.get('dado_pesquisa')
        atendentes_lista = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa)
        paginas = Paginator(atendentes_lista, 3)
        atendentes = paginas.get_page(page)
        return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa,
                                                       'usuario_logado': usuario_logado})

    if dado_pesquisa_atendente != None and dado_pesquisa_atendente != '':
        todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)

        paginas = Paginator(todos_atendentes, 3)

        page = request.GET.get('page')

        atendentes = paginas.get_page(page)

        return render(request, 'Cons_Atendente.html',
                      {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente,
                       'usuario_logado': usuario_logado})

    paginas = Paginator(todos_atendentes, 3)  # 3 representa o número de atendentes por página
    page = request.GET.get('page')
    atendentes = paginas.get_page(page)

    if dado_pesquisa_atendente != None:
        return render(request, 'Cons_Atendente.html',
                      {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente,
                       'usuario_logado': usuario_logado})
    else:
        return render(request, 'Cons_Atendente.html',
                      {'todos_atendentes': atendentes, 'dado_pesquisa': '', 'usuario_logado': usuario_logado})


@login_required
def edit_atend(request, id):
    dados_editar = get_object_or_404(Atendente, pk=id)
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    return render(request, 'Edit_Atendente.html',
                  {'dados_do_atendente': dados_editar, 'cons_users': cons_users, 'usuario_logado': usuario_logado})


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

# =================================Departments==========================================

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

        Departamento_Editado = Departamento.objects.get(id=id_depto)

        Departamento_Editado.descricao_departamento = descricao_departamento
        Departamento_Editado.info_departamento = info_departamento

        Departamento_Editado.save()

        messages.info(request, 'Departamento ' + descricao_departamento + ' editado com sucesso.')
        return render(request, 'Cons_Depto.html', {'usuario_logado': usuario_logado})