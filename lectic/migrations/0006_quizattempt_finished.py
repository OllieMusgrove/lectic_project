# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-06 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectic', '0005_quizattempt_qes_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]