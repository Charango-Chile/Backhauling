# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 07:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OptDemoNov', '0004_auto_20171119_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='OwnerName',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='OptDemoNov.SysUsers'),
        ),
    ]