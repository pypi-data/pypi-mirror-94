# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import python_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0002_auto_20151016_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('logic', python_field.fields.PythonCodeField(null=True, blank=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
