# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import newsletter.utils


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_auto_20150416_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='site',
            field=models.ManyToManyField(verbose_name='site', to='sites.Site', default=newsletter.utils.get_default_sites),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]
