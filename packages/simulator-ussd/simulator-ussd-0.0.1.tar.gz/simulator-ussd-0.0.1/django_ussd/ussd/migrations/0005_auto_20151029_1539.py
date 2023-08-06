# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0004_auto_20151028_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('language', models.CharField(max_length=255)),
                ('text', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='listitems',
            name='text',
        ),
        migrations.RemoveField(
            model_name='menuoptions',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ussdhandler',
            name='title',
        ),
        migrations.AddField(
            model_name='listitems',
            name='text',
            field=models.ManyToManyField(to='ussd.Translation'),
        ),
        migrations.AddField(
            model_name='menuoptions',
            name='name',
            field=models.ManyToManyField(to='ussd.Translation'),
        ),
        migrations.AddField(
            model_name='ussdhandler',
            name='title',
            field=models.ManyToManyField(blank=True, to='ussd.Translation'),
        ),
    ]
