from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.abre_index, name='abre_index'),
    path('Cad_Cliente.html', views.cad_cliente, name='cad_cliente'),
    path('Cons_Cliente.html', views.cons_cliente, name='cons_cliente'),
    path('salvar_cliente_novo', views.salvar_cliente_novo, name='salvar_cliente_novo'),
    path('edit_cliente/<int:id>', views.edit_cliente, name='edit_cliente'),
    path('salvar_cliente_editado', views.salvar_cliente_editado, name='salvar_cliente_editado'),
    path('excluir_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),

    path('Cad_Atendente.html', views.cad_atend, name='cad_atend'),
    path('Cons_Atendente.html', views.cons_atend, name='cons_atend'),
    path('edit_atend/<int:id>', views.edit_atend, name='edit_atend'),
    path('salvar_atend_editado', views.salvar_atend_editado, name='salvar_atend_editado'),
    path('salvar_atend_novo', views.salvar_atend_novo, name='salvar_atend_novo'),

    path('Cad_Depto.html', views.cad_depto, name='cad_depto'),
    path('cons_depto', views.cons_depto, name='cons_depto'),
    path('edit_depto/<int:id>', views.edit_depto, name='edit_depto'),
    path('salvar_depto_novo', views.salvar_depto_novo, name='salvar_depto_novo'),
    path('salvar_depto_editado', views.salvar_depto_editado, name='salvar_depto_editado'),

]




