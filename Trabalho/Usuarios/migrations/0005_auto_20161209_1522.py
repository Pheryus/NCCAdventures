# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-09 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0004_auto_20161025_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=30, verbose_name='Nome'),
        ),
    ]