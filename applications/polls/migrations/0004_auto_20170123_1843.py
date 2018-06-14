# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import stdimage.models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_choice_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='public',
            field=models.BooleanField(verbose_name='Public', help_text='Allows to view polls for users from other condominiums', default=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice',
            field=models.CharField(verbose_name='user choice', blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='choice',
            name='image',
            field=stdimage.models.StdImageField(verbose_name='poll image', upload_to=polls.models.get_file_path, blank=True),
        ),
    ]
