# Generated by Django 4.2.4 on 2023-09-01 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_SAC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_atend', models.CharField(max_length=120)),
                ('telefone_atend', models.CharField(max_length=24, null=True)),
                ('observacao_atend', models.TextField(null=True)),
                ('criado_em_atend', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em_atend', models.BooleanField()),
                ('user_atend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
