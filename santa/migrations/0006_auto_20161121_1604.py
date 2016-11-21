# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0005_santalist_organiser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='santalist',
            old_name='secure_hash',
            new_name='secure_hash_review',
        ),
        migrations.AddField(
            model_name='santalist',
            name='secure_hash_signup',
            field=models.CharField(max_length=12, null=True, unique=True),
        ),
    ]