# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20160709_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exit',
            name='exit_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanin',
            name='loan_in_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanin',
            name='return_out_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanout',
            name='loan_out_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanout',
            name='return_in_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
