# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20160709_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.SlugField(blank=True),
            preserve_default=False,
        ),
    ]