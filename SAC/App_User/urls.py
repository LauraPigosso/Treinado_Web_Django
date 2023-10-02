from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_novo_user, name='cad_user'),
    path('salvar_usuario', views.cadastrar_usuario, name='salvar_usuario'),
]
