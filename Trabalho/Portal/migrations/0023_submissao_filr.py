# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0022_auto_20161208_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissao',
            name='filr',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
