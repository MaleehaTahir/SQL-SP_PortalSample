# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='start_date',
            field=models.DateField(),
        ),
    ]