# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_condominium_problem_days'),
        ('newsletter', '0003_auto_20161111_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='condominium',
            field=models.ForeignKey(null=True, to='system.Condominium', blank=True, verbose_name='Condominium'),
        ),
    ]
