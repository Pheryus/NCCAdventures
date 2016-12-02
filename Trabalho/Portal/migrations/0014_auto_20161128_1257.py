# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0013_auto_20161128_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissao',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Usuarios.Usuario'),
        ),
        migrations.AlterField(
            model_name='submissao',
            name='trabalhoKey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, to='Portal.Trabalho'),
        ),
    ]
