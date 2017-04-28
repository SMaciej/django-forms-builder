# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_auto_20160418_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='terms',
            field=models.CharField(default=1, max_length=1020, verbose_name='Terms'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='field',
            name='choices',
            field=models.CharField(blank=True, help_text='Comma separated options where applicable. If an option itself contains commas, surround the option starting with the `character and ending with the ` character.', max_length=2000, verbose_name='Choices'),
        ),
        migrations.AlterField(
            model_name='field',
            name='field_type',
            field=models.IntegerField(choices=[(1, 'Single line text'), (2, 'Multi line text'), (3, 'Email'), (13, 'Number'), (14, 'URL'), (4, 'Check box'), (5, 'Check boxes'), (6, 'Drop down'), (7, 'Multi select'), (8, 'Radio buttons'), (9, 'File upload'), (10, 'Date'), (11, 'Date/time'), (15, 'Date of birth'), (12, 'Hidden'), (100, 'My cool checkbox')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='field',
            name='help_text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Help text'),
        ),
        migrations.AlterField(
            model_name='field',
            name='label',
            field=models.CharField(max_length=2000, verbose_name='Label'),
        ),
    ]