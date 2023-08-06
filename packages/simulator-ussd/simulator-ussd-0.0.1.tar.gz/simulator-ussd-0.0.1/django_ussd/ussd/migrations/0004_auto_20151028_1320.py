# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import python_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0003_widget'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widget',
            name='name',
        ),
        migrations.AddField(
            model_name='widget',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='widget',
            name='logic',
            field=python_field.fields.PythonCodeField(),
        ),
    ]
