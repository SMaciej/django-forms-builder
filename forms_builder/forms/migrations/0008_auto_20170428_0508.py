# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 04:21
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields
import tinymce_ex.models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_auto_20170428_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='intro',
            field=tinymce_ex.models.HTMLField(blank=True, null=True, verbose_name='Intro'),
        ),
    ]
