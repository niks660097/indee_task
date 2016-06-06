# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('secure_documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdocument',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 5, 16, 40, 1, 97000)),
            preserve_default=False,
        ),
    ]
