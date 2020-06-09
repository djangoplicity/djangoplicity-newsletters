# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-30 12:05
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0006_auto_20160421_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='feed_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]