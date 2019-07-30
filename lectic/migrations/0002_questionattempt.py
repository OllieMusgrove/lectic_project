# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-29 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lectic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attempt', models.CharField(max_length=100)),
                ('result', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectic.Question')),
            ],
        ),
    ]