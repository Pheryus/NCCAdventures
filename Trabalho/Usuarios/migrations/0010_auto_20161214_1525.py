# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0009_auto_20161214_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='professor',
            field=models.CharField(max_length=30),
        ),
    ]