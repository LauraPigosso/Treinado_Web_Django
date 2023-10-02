from django.urls import path
from .views import index, Atendente, Cliente, Departamento, Situacao, Atendimento

urlpatterns = [
    path('', index.abre_index, name='abre_index'),
    
    path('cad_cliente', Cliente.cad_cliente, name='cad_cliente'),
    path('cons_cliente', Cliente.cons_cliente, name='cons_cliente'),
    path('edit_cliente/<int:id>', Cliente.edit_cliente, name='edit_cliente'),
    path('excluir_cliente/<int:id>', Cliente.delete_cliente, name='excluir_cliente'),
    path('salvar_cliente_novo', Cliente.salvar_cliente_novo, name='salvar_cliente_novo'),
    path('salvar_cliente_editado', Cliente.salvar_cliente_editado, name='salvar_cliente_editado'),

    path('cad_atend', Atendente.cad_atend, name='cad_atend'),
    path('cons_atend', Atendente.cons_atend, name='cons_atend'),
    path('edit_atend/<int:id>', Atendente.edit_atend, name='edit_atend'),
    path('salvar_atend_novo', Atendente.salvar_atend_novo, name='salvar_atend_novo'),
    path('salvar_atend_editado', Atendente.salvar_atend_editado, name='salvar_atend_editado'),

    path('cad_depto', Departamento.cad_depto, name='cad_depto'),
    path('cons_depto', Departamento.cons_depto, name='cons_depto'),
    path('edit_depto/<int:id>', Departamento.edit_depto, name='edit_depto'),
    path('salvar_depto_novo', Departamento.salvar_depto_novo, name='salvar_depto_novo'),
    path('salvar_depto_editado', Departamento.salvar_depto_editado, name='salvar_depto_editado'),

    path('cad_situacao', Situacao.cad_situacao, name='cad_situacao'),
    path('cons_situacao', Situacao.cons_situacao, name='cons_situacao'),
    path('edit_situacao/<int:id>', Situacao.edit_situacao, name='edit_situacao'),
    path('salvar_situacao_nova', Situacao.salvar_situacao_nova, name='salvar_situacao_nova'),
    path('salvar_situacao_editada', Situacao.salvar_situacao_editada, name='salvar_situacao_editada'),

    path('reg_atend_busca_cliente', Atendimento.reg_atend_busca_cliente, name="reg_atend_busca_cliente" ),
    path('sel_cliente/<int:id>', Atendimento.sel_cliente , name="sel_cliente" ),
    path('salvar_atendimento_novo', Atendimento.salvar_atendimento_novo , name="salvar_atendimento_novo" ),

    # path('reg_atendimento', Atendimento.reg_atendimento, name='reg_atendimento')
    # path('salvar_atendimento_novo', Atendimento., name='salvar_atendimento_novo')
]
