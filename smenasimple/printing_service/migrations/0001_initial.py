# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-09 06:23
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_type', models.CharField(choices=[('kitchen', 'Kitchen'), ('client', 'Client')], max_length=7, verbose_name='Тип чека')),
                ('order', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Информация о заказе')),
                ('status', models.CharField(choices=[('new', 'New'), ('render', 'Render'), ('printed', 'Printed')], max_length=7, verbose_name='Статус чека')),
                ('pdf_file', models.FileField(blank=True, upload_to='pdf', verbose_name='Ссылка на созданный PDF-файл')),
            ],
            options={
                'verbose_name': 'Чек',
                'verbose_name_plural': 'Чеки',
            },
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название принтера')),
                ('api_key', models.CharField(max_length=50, unique=True, verbose_name='Ключ доступа к API')),
                ('check_type', models.CharField(choices=[('kitchen', 'Kitchen'), ('client', 'Client')], max_length=7, verbose_name='Тип чека, который печатает принтер')),
                ('point_id', models.IntegerField(verbose_name='Точка, к которой привязан принтер')),
            ],
            options={
                'verbose_name': 'Принтер',
                'verbose_name_plural': 'Принтеры',
            },
        ),
        migrations.AddField(
            model_name='check',
            name='printer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='printing_service.Printer', verbose_name='ID принтера'),
        ),
    ]
