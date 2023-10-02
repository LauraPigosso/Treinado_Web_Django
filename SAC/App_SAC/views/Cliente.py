from django.shortcuts import render, get_object_or_404, redirect
from ..models import Cliente
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def cad_cliente(request):
    return render(request, 'Cad_cliente.html')


@login_required
def salvar_cliente_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')
        grava_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            email=email,
            observacao=observacao,
        )
        grava_cliente.save()
        messages.info(request, f"Cliente {nome} cadastrado com sucesso")
        return render(request, 'Cad_cliente.html', {})


@login_required
def cons_cliente(request):
    dado_pesquisa_nome = request.POST.get('cliente') if request.POST.get('cliente') else request.GET.get('cliente') if request.GET.get('cliente') else ""
    dado_pesquisa_telefone = request.POST.get('telefone') if request.POST.get('telefone') else request.GET.get('telefone') if request.GET.get('telefone') else ""
    dado_pesquisa_email = request.POST.get('email') if request.POST.get('email') else request.GET.get('email') if request.GET.get('email') else ""

    if dado_pesquisa_nome is not None and dado_pesquisa_nome != '':
        clientes = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente.html', {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    elif dado_pesquisa_telefone is not None and dado_pesquisa_telefone != '':
        clientes = Cliente.objects.filter(telefone__icontains=dado_pesquisa_telefone)
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente.html', {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    elif dado_pesquisa_email is not None and dado_pesquisa_email != '':
        clientes = Cliente.objects.filter(email__icontains=dado_pesquisa_email)
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente.html',  {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})

    else:
        clientes = Cliente.objects.all()
        objetoPaginado = Paginator(clientes, 2)
        page_num = request.GET.get('page')
        paginaFiltrada = objetoPaginado.get_page(page_num)
        return render(request, 'Cons_Cliente.html',  {'dados_clientes': paginaFiltrada, 'cliente': dado_pesquisa_nome, 'telefone': dado_pesquisa_telefone, 'email': dado_pesquisa_email})


@login_required
def edit_cliente(request, id):
    dados_editar = get_object_or_404(Cliente, pk=id)
    return render(request, 'Edit_Cliente.html', {'dados_do_cliente': dados_editar})


@login_required
def salvar_cliente_editado(request):
    if request.method == 'POST':
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

        messages.info(request, f'Cliente {nome} editado com sucesso.')

        return render(request, 'Cons_Cliente.html')


@login_required
def delete_cliente(request, id):
    cliente_deletado = get_object_or_404(Cliente, pk=id)
    nome = cliente_deletado.nome
    cliente_deletado.delete()

    messages.info(request, f'Cliente {nome} excluido com sucesso.')
    return redirect('cons_cliente')