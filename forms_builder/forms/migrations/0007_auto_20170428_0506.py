# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 05:06
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_auto_20170428_0449'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formslist',
            options={'verbose_name': 'Forms list', 'verbose_name_plural': 'Forms lists'},
        ),
        migrations.RemoveField(
            model_name='formslist',
            name='banner',
        ),
        migrations.AddField(
            model_name='form',
            name='banner',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='form_banners', verbose_name='Banner'),
        ),
    ]
