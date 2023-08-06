# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='httprequest',
            name='headers',
            field=jsonfield.fields.JSONField(null=True, default={}, blank=True),
        ),
        migrations.AlterField(
            model_name='httprequest',
            name='params',
            field=jsonfield.fields.JSONField(null=True, default={}, blank=True),
        ),
    ]
