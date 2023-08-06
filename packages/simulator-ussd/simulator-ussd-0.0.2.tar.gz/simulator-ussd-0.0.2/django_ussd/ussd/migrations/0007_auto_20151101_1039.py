# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0006_auto_20151030_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuoptions',
            name='text',
            field=models.ManyToManyField(to='ussd.Translation', related_name='menu_text'),
        ),
        migrations.AlterField(
            model_name='ussdhandler',
            name='text',
            field=models.ManyToManyField(to='ussd.Translation', related_name='screen_text', blank=True),
        ),
    ]
