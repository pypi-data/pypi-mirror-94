# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0005_auto_20151029_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuoptions',
            old_name='name',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='ussdhandler',
            old_name='title',
            new_name='text',
        ),
    ]
