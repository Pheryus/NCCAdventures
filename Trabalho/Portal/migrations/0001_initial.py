# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-22 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Usuarios', '0002_auto_20161022_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trabalho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('descricao', models.CharField(max_length=500)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.Usuario')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.Turma')),
            ],
        ),
    ]
