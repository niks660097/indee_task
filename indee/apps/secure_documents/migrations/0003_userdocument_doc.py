# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.secure_documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('secure_documents', '0002_userdocument_date_uploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdocument',
            name='doc',
            field=models.FileField(default='', upload_to=apps.secure_documents.models.decide_file_path),
            preserve_default=False,
        ),
    ]
