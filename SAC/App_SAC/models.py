from django.db import models
from django.contrib.auth import get_user_model


class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=240)
    email = models.CharField(max_length=120)
    observacao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Atendente(models.Model):
    nome_atend = models.CharField(max_length=120)
    telefone_atend = models.CharField(max_length=240)
    observacao_atend = models.TextField()
    criado_em_atend = models.DateTimeField(auto_now_add=True)
    atualizado_em_atend = models.DateTimeField(auto_now=True)
    ativo_atend = models.BooleanField()
    user_atend = models.ForeignKey(get_user_model(), null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome_atend


class Departamento(models.Model):
    descricao_departamento = models.CharField(max_length=30, null=False)
    info_departamento = models.TextField(null=True)
    ativo_departamento = models.BooleanField()

    def __str__(self):
        return self.descricao_departamento


class Situacao(models.Model):
    descricao_situacao = models.CharField(max_length=30, null=False)
    info_situacao = models.TextField(null=True)
    ativo_situacao = models.BooleanField()

    def __str__(self):
        return self.descricao_situacao
