# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-14 02:24
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0010_auto_20170609_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalformentry',
            name='expiry_date',
            field=models.DateTimeField(blank=True, help_text="With published selected, won't be shown after this time", null=True, verbose_name='Expires on'),
        ),
        migrations.AddField(
            model_name='externalformentry',
            name='publish_date',
            field=models.DateTimeField(blank=True, help_text="With published selected, won't be shown until this time", null=True, verbose_name='Published from'),
        ),
        migrations.AddField(
            model_name='externalformentry',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2, verbose_name='Status'),
        ),
    ]
