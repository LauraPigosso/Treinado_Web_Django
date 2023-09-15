from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('Cad_Cliente.html', views.cad_cliente, name='Cad_Cliente'),
    path('Cons_Cliente.html', views.cons_cliente, name='cons_cliente'),
    path('salvar_cliente_novo', views.salvar_cliente_novo, name='salvar_cliente_novo'),
    path('edit_cliente/<int:id>', views.edit_cliente, name='edit_cliente'),
    path('salvar_cliente_editado', views.salvar_cliente_editado, name='salvar_cliente_editado'),
    path('excluir_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),
    path('cad_atend', views.cad_atend, name='cad_atend'),
    path('salvar_atend_novo', views.salvar_atend_novo, name='salvar_atend_novo'),
    path('Cons_Atendente.html', views.cons_atend, name='Cons_Atendente'),

]


