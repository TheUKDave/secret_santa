# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='santalist',
            name='email_template',
        ),
        migrations.AddField(
            model_name='santalist',
            name='email_content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='santalist',
            name='email_subject',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='santalist',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='santalist',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='EmailTemplate',
        ),
    ]
