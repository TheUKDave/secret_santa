# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0004_santalist_secure_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='santalist',
            name='organiser_email',
            field=models.EmailField(default='', max_length=200, verbose_name='Your email'),
            preserve_default=False,
        ),
    ]