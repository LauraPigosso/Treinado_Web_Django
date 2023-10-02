from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages  # biblioteca de messagens do django
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from ..models import Atendimento, Departamento, Cliente, Situacao, Atendente
from django.contrib.auth.models import User
from datetime import datetime


@login_required
def reg_atend_busca_cliente(request):
    usuario_logado = request.user.username

    dado_pesquisa_nome = request.POST.get("sel_cliente")
    cons_depto = Departamento.objects.all()
    data_e_hora = datetime.now()
    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    page = request.GET.get("page")

    if page:
        print("a")

        dado_pesquisa = request.GET.get("dado_pesquisa")
        print(dado_pesquisa)
        cliente_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa)
        paginas = Paginator(cliente_lista, 3)
        clientes = paginas.get_page(page)
        return render(
            request,
            "Reg_Atendimento_busca.html",
            {
                "dados_clientes": clientes,
                "dado_pesquisa": dado_pesquisa,
                "usuario_logado": usuario_logado,
                "cons_depto": cons_depto,
                "data_e_hora": data_e_hora,
            },
        )

    if dado_pesquisa_nome != None and dado_pesquisa_nome != "":
        cliente_lista = Cliente.objects.filter(
            nome__icontains=dado_pesquisa_nome)

        paginas = Paginator(cliente_lista, 2)

        page = request.GET.get("page")

        clientes = paginas.get_page(page)

        return render(
            request,
            "Reg_Atendimento_busca.html",
            {
                "dados_clientes": clientes,
                "dado_pesquisa": dado_pesquisa_nome,
                "usuario_logado": usuario_logado,
                "cons_depto": cons_depto,
                "data_e_hora": data_e_hora,
            },
        )

    else:
        return render(
            request,
            "Reg_Atendimento_busca.html",
            {
                "usuario_logado": usuario_logado,
                "cons_depto": cons_depto,
                "data_e_hora": data_e_hora,
            },
        )


@login_required
def sel_cliente(request, id):
    usuario_logado = request.user.username
    cons_depto = Departamento.objects.all()
    data_e_hora = datetime.now()
    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    dados_clientes = get_object_or_404(Cliente, pk=id)

    return render(
        request,
        "Reg_Atendimento_Busca.html",
        {
            "cliente_sel": dados_clientes,
            "usuario_logado": usuario_logado,
            "cons_depto": cons_depto,
            "data_e_hora": data_e_hora,
        },
    )


@login_required
def salvar_atendimento_novo(request):
    usuario_logado = request.user.username
    id_atendente = request.user.id

    if (request.method == "POST"):
        solicitacao = request.POST.get('solicitacao')
        cliente = request.POST.get('id_cliente')
        departamento = request.POST.get('encaminhar')

        cliente = Cliente.objects.get(id=cliente)

        if departamento:
            departamento = Departamento.objects.get(id=departamento)
        else:
            departamento = None

        situacao = Situacao.objects.get(id=1)

        atendente = Atendente.objects.filter(user_atend_id=id_atendente).last()

        grava_atendimento = Atendimento(
            solicitacao=solicitacao,
            cliente=cliente,
            departamento=departamento,
            atendente=atendente,
            criado_em=datetime.now(),
            encerrado=0
        )
        grava_atendimento.save()
        cons_ultimo = Atendimento.objects.last()

        comentario = "Registro automatico ao criar o chamado"

        atendimento = Atendimento.objects.get(id=cons_ultimo.id)

        # messages.info(request, f'Atendimento {str(cons_ultimo.id)} registrado com sucesso!')
        messages.info(request, f'Atendimento registrado com sucesso!')
        return redirect('reg_atend_busca_cliente')
