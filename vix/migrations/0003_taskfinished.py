# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-25 02:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vix', '0002_auto_20160718_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskFinished',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vix.Task')),
            ],
            bases=('vix.task',),
        ),
    ]
