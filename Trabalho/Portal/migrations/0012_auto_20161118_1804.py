# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0011_auto_20161118_1731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submissao',
            old_name='passwordsend',
            new_name='correctPassword',
        ),
        migrations.AlterField(
            model_name='submissao',
            name='trabalhoKey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Portal.Trabalho'),
        ),
    ]
