# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HttpRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('url', models.CharField(max_length=100)),
                ('params', jsonfield.fields.JSONField(default={})),
                ('method', models.CharField(max_length=100, choices=[('post', 'post'), ('get', 'get')])),
                ('headers', jsonfield.fields.JSONField(default={})),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ListItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField(max_length=100)),
                ('iterable', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'ListItems',
                'verbose_name_plural': 'ListItems',
            },
        ),
        migrations.CreateModel(
            name='MenuOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('index', models.IntegerField()),
                ('in_put', models.CharField(max_length=50, verbose_name='input_to_display', null=True, blank=True)),
                ('in_put_value', models.CharField(max_length=50, verbose_name='input_to_be_selected', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'MenuOptions',
                'verbose_name_plural': 'MenuOptions',
            },
        ),
        migrations.CreateModel(
            name='PluginHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('plugin', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UssdHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('session_key', models.CharField(max_length=50, null=True, blank=True)),
                ('session_state', models.BooleanField(default=True)),
                ('http_request', models.ForeignKey(related_name='http_request', null=True, to='ussd.HttpRequest', blank=True)),
                ('list_items', models.OneToOneField(null=True, to='ussd.ListItems', blank=True)),
                ('next_handler', models.ForeignKey(null=True, to='ussd.UssdHandler', blank=True)),
                ('plugin', models.OneToOneField(null=True, to='ussd.PluginHandler', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UssdHandlerFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('new_feature', models.ForeignKey(related_name='ussd_handler_flag_new_features', to='ussd.UssdHandler')),
                ('ussd_handler', models.ForeignKey(to='ussd.UssdHandler')),
            ],
        ),
        migrations.CreateModel(
            name='UssdRouterHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('expression', models.CharField(max_length=500)),
                ('index', models.IntegerField()),
                ('next_handler', models.ForeignKey(to='ussd.UssdHandler')),
                ('ussd_handler', models.ForeignKey(related_name='ussd_screen', to='ussd.UssdHandler')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.AddField(
            model_name='pluginhandler',
            name='next_handler',
            field=models.ForeignKey(to='ussd.UssdHandler'),
        ),
        migrations.AddField(
            model_name='menuoptions',
            name='next_handler',
            field=models.ForeignKey(related_name='menuoptions_next_handler', null=True, to='ussd.UssdHandler', blank=True),
        ),
        migrations.AddField(
            model_name='menuoptions',
            name='plugin',
            field=models.OneToOneField(null=True, to='ussd.PluginHandler', blank=True),
        ),
        migrations.AddField(
            model_name='menuoptions',
            name='ussd_handler',
            field=models.ForeignKey(to='ussd.UssdHandler'),
        ),
        migrations.AlterUniqueTogether(
            name='menuoptions',
            unique_together=set([('index', 'ussd_handler', 'in_put')]),
        ),
    ]
