# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_server_background_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='is_success',
        ),
        migrations.AddField(
            model_name='host',
            name='age',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
