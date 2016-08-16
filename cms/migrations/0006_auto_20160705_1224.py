# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20160626_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=128)),
                ('condition', models.CharField(max_length=128)),
                ('edition', models.CharField(blank=True, max_length=128)),
                ('series', models.CharField(blank=True, max_length=128)),
                ('note', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('return_date', models.DateField(blank=True)),
                ('owner', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Exit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exit_date', models.DateField(blank=True)),
                ('exit_destination', models.CharField(blank=True, max_length=128)),
                ('exit_note', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=128, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('stock', models.IntegerField(default=0)),
                ('item_description', models.CharField(max_length=300)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('category', models.ManyToManyField(to='cms.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=128)),
                ('location_date', models.DateField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_date', models.DateField()),
                ('artist', models.CharField(max_length=128)),
                ('place', models.CharField(max_length=128)),
                ('technique', models.CharField(max_length=128)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Item')),
            ],
        ),
        migrations.AddField(
            model_name='exit',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Item'),
        ),
        migrations.AddField(
            model_name='entry',
            name='entry_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cms.Item'),
        ),
        migrations.AddField(
            model_name='description',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Item'),
        ),
    ]