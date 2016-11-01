# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chm', '0007_quiz_nr_of_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questiononquiz',
            name='question',
        ),
        migrations.AddField(
            model_name='questiononquiz',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chm.Question'),
            preserve_default=False,
        ),
    ]
