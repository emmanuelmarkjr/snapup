# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-20 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180420_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='snaplink',
            name='currency',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='snaplink',
            name='date_added',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='snaplink',
            name='img_url',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='snaplink',
            name='price',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='snaplink',
            name='time_added',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='snaplink',
            name='title',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
