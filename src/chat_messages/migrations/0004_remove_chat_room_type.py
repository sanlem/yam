# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-25 20:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_messages', '0003_auto_20171224_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='room_type',
        ),
    ]
