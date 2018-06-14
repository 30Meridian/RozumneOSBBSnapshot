# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominium_management', '0005_auto_20161121_1557'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyCondominium',
        ),
    ]
