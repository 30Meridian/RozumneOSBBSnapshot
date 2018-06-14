# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import stdimage.models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20161011_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='image',
            field=stdimage.models.StdImageField(upload_to=polls.models.get_file_path, verbose_name='idea image', blank=True),
        ),
    ]
