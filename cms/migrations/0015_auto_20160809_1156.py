# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20160805_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='production_year',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
