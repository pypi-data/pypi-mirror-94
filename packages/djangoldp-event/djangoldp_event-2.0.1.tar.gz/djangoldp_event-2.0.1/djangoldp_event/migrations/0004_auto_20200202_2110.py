# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-02 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_event', '0003_auto_20200202_1644'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locationevent',
            options={},
        ),
        migrations.AlterModelOptions(
            name='typeevent',
            options={},
        ),
        migrations.AlterField(
            model_name='typeevent',
            name='name',
            field=models.CharField(max_length=50, verbose_name="Type d'évènement"),
        ),
    ]
