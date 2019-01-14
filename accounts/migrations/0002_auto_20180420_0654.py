# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-20 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snaplink',
            options={'verbose_name_plural': 'Snap Links'},
        ),
        migrations.AlterField(
            model_name='snaplink',
            name='snap_link',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]
