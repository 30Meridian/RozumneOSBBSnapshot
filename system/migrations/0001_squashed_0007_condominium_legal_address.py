# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.contrib.auth.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    replaces = [('system', '0001_initial'), ('system', '0002_modules_parent'), ('system', '0003_condominium_modules'), ('system', '0004_city'), ('system', '0005_condomonium_registration'), ('system', '0006_remove_condominium_address'), ('system', '0007_condominium_legal_address')]

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(unique=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=64, null=True, verbose_name='user phone')),
                ('middle_name', models.CharField(max_length=64, verbose_name='middle name')),
                ('address', models.CharField(max_length=128, blank=True, default='', verbose_name='user adress')),
            ],
            options={
                'db_table': 'auth_user',
                'abstract': False,
                'managed': True,
                'verbose_name_plural': 'auth user',
                'verbose_name': 'auth user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('index', models.IntegerField(verbose_name='address index')),
                ('street_type', models.CharField(max_length=32, verbose_name='address street_type')),
                ('street_name', models.CharField(max_length=64, verbose_name='address street_name')),
                ('number', models.IntegerField(verbose_name='address number')),
                ('symbol', models.CharField(max_length=2, blank=True, null=True, verbose_name='address symbol')),
                ('pavilion', models.CharField(max_length=16, blank=True, null=True, verbose_name='address pavilion')),
            ],
            options={
                'db_table': 'address',
                'verbose_name_plural': 'addresses',
                'verbose_name': 'address',
            },
        ),
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('removed', models.DateTimeField(editable=False, blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=64, blank=True, default='Condominium', verbose_name='name condominium')),
                ('slug', models.CharField(unique=True, max_length=64, verbose_name='slug condominium')),
                ('description', models.CharField(max_length=256, blank=True, null=True, verbose_name='description condominium')),
                ('votes', models.IntegerField(default=10, verbose_name='votes condominium')),
                ('ideas_days', models.IntegerField(default=30, verbose_name='ideas_days condominium')),
                ('ideas_number_templ', models.CharField(max_length=64, verbose_name='ideas number condominium', blank=True, default='10/%s', null=True)),
                ('address', models.ForeignKey(db_column='address', to='system.Address', verbose_name='address condominium', blank=True, null=True)),
            ],
            options={
                'db_table': 'condominium',
                'verbose_name_plural': 'condominiums',
                'verbose_name': 'condominium',
            },
        ),
        migrations.CreateModel(
            name='CondominiumCommonArea',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('area', models.FloatField(verbose_name='common area-area')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='common area description')),
            ],
            options={
                'db_table': 'condominium_common_area',
                'verbose_name_plural': 'Common Areas',
                'verbose_name': 'Common area',
            },
        ),
        migrations.CreateModel(
            name='CondominiumConnectedUtiliteLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('current_value', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'condominium_connected_utilities_log',
                'verbose_name_plural': 'utility logs',
                'verbose_name': 'utility log',
            },
        ),
        migrations.CreateModel(
            name='CondominiumConnectedUtility',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('subsidy', models.FloatField(default=0.0)),
                ('start_value', models.FloatField()),
            ],
            options={
                'db_table': 'condominium_connected_utilities',
                'verbose_name_plural': 'utilities',
                'verbose_name': 'utilities',
            },
        ),
        migrations.CreateModel(
            name='CondominiumFloor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32, blank=True, null=True, verbose_name='floor name')),
                ('residential_count', models.IntegerField(verbose_name='floor residential_count')),
                ('non_residential_count', models.IntegerField(default=0, verbose_name='floor non_residential_count')),
                ('lighting_points', models.IntegerField(default=1, verbose_name='floor lighting_points')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='floor description')),
            ],
            options={
                'db_table': 'condominium_floor',
                'verbose_name_plural': 'floors',
                'verbose_name': 'floor',
            },
        ),
        migrations.CreateModel(
            name='CondominiumHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, blank=True, null=True, verbose_name='house name ')),
                ('area', models.FloatField(verbose_name='house area ')),
                ('residential_area', models.FloatField(verbose_name='house residential area ')),
                ('entrance_count', models.IntegerField(verbose_name='house entrance count ')),
                ('min_floors', models.IntegerField(verbose_name='house min floors ')),
                ('max_floors', models.IntegerField(verbose_name='house max floors ')),
                ('residential_count', models.IntegerField(verbose_name='house residential count ')),
                ('elevators_count', models.IntegerField(verbose_name='house elevators count ')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='house description ')),
                ('address', models.ForeignKey(db_column='address', to='system.Address', verbose_name='house address ')),
                ('condominium', models.ForeignKey(db_column='condominium', to='system.Condominium', verbose_name='house condominium ')),
            ],
            options={
                'db_table': 'condominium_house',
                'verbose_name_plural': 'houses',
                'verbose_name': 'house',
            },
        ),
        migrations.CreateModel(
            name='CondominiumInfrastructure',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('area', models.FloatField(verbose_name='infrastructure area')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='infrastructure description')),
            ],
            options={
                'db_table': 'condominium_infrastructure',
                'verbose_name_plural': 'infrastructures',
                'verbose_name': 'infrastructure',
            },
        ),
        migrations.CreateModel(
            name='CondominiumNonResidentialPremise',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='non residental number')),
                ('area', models.FloatField(verbose_name='non residental area')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='non residental description')),
                ('floor', models.ForeignKey(db_column='floor', to='system.CondominiumFloor', verbose_name='non residental floor')),
            ],
            options={
                'db_table': 'condominium_non_residential_premise',
                'verbose_name_plural': 'condominium non residential premises',
                'verbose_name': 'condominium non residential premise',
            },
        ),
        migrations.CreateModel(
            name='CondominiumPorch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('number', models.IntegerField(verbose_name='porch number')),
                ('name', models.CharField(max_length=64, blank=True, null=True, verbose_name='porch name')),
                ('floors_count', models.IntegerField(verbose_name='porch floors_count')),
                ('residential_count', models.IntegerField(verbose_name='porch residential_count')),
                ('non_residential_count', models.IntegerField(default=0, verbose_name='porch non_residential_count')),
                ('lighting_points', models.IntegerField(verbose_name='porch lighting_points')),
                ('elevators_count', models.IntegerField(verbose_name='porch elevators_count')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='porch description')),
                ('house', models.ForeignKey(db_column='house', to='system.CondominiumHouse', verbose_name='porch house')),
            ],
            options={
                'db_table': 'condominium_porch',
                'verbose_name_plural': 'porches',
                'verbose_name': 'porch',
            },
        ),
        migrations.CreateModel(
            name='CondominiumResidentialPremise',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('number', models.IntegerField(verbose_name='residental number ')),
                ('area', models.FloatField(verbose_name='residental area ')),
                ('residential_area', models.FloatField(verbose_name='residental residential area ')),
                ('heating_area', models.FloatField(verbose_name='residental heating area ')),
                ('rooms_count', models.IntegerField(verbose_name='residental rooms count ')),
                ('residents_count', models.IntegerField(verbose_name='residental residents_count ')),
                ('pets_count', models.IntegerField(verbose_name='residental pets count ')),
                ('description', models.CharField(max_length=255, blank=True, null=True, verbose_name='residental description ')),
                ('floor', models.ForeignKey(db_column='floor', to='system.CondominiumFloor', verbose_name='residental floor')),
            ],
            options={
                'db_table': 'condominium_residential_premise',
                'verbose_name_plural': 'condominium residential premises',
                'verbose_name': 'condominium residential premise',
            },
        ),
        migrations.CreateModel(
            name='EngineeringService',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('subsidy', models.BooleanField(default=False)),
                ('value', models.FloatField()),
                ('measurement_units', models.CharField(max_length=64)),
                ('determine', models.CharField(max_length=128)),
                ('datetime_crated', models.DateTimeField(auto_now_add=True)),
                ('datetime_changed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('condominium', models.ForeignKey(db_column='condominium', to='system.Condominium')),
            ],
            options={
                'db_table': 'engineering_service',
                'verbose_name_plural': 'services',
                'verbose_name': 'service',
            },
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32, blank=True, null=True)),
                ('slug', models.CharField(max_length=32, blank=True, null=True)),
                ('icon', models.CharField(max_length=64, blank=True, default='fa fa-plus', null=True)),
                ('parent', models.ForeignKey(to='system.Modules', null=True)),
            ],
            options={
                'db_table': 'modules',
                'verbose_name_plural': 'modules',
                'verbose_name': 'module',
            },
        ),
        migrations.CreateModel(
            name='ObjectRegistry',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=64, blank=True, default='', null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_changed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('condominium', models.ForeignKey(to='system.Condominium')),
            ],
            options={
                'db_table': 'object_registry',
                'verbose_name_plural': 'objects registry',
                'verbose_name': 'object registry',
            },
        ),
        migrations.CreateModel(
            name='ObjectTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('category', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(max_length=256, blank=True, null=True)),
            ],
            options={
                'db_table': 'object_types',
                'verbose_name_plural': 'object types',
                'verbose_name': 'object type',
            },
        ),
        migrations.AlterUniqueTogether(
            name='objecttypes',
            unique_together=set([('title', 'category')]),
        ),
        migrations.AddField(
            model_name='objectregistry',
            name='type',
            field=models.ForeignKey(db_column='type', to='system.ObjectTypes'),
        ),
        migrations.AddField(
            model_name='objectregistry',
            name='user_changed',
            field=models.ForeignKey(db_column='user_changed', to=settings.AUTH_USER_MODEL, related_name='changed'),
        ),
        migrations.AddField(
            model_name='objectregistry',
            name='user_created',
            field=models.ForeignKey(db_column='user_created', to=settings.AUTH_USER_MODEL, related_name='created'),
        ),
        migrations.AddField(
            model_name='condominiumresidentialpremise',
            name='object_registry',
            field=models.ForeignKey(to='system.ObjectRegistry', null=True),
        ),
        migrations.AddField(
            model_name='condominiumresidentialpremise',
            name='type',
            field=models.ForeignKey(db_column='type', to='system.ObjectTypes', verbose_name='residental type '),
        ),
        migrations.AddField(
            model_name='condominiumporch',
            name='object_registry',
            field=models.ForeignKey(to='system.ObjectRegistry', null=True),
        ),
        migrations.AddField(
            model_name='condominiumnonresidentialpremise',
            name='object_registry',
            field=models.ForeignKey(to='system.ObjectRegistry', null=True),
        ),
        migrations.AddField(
            model_name='condominiumnonresidentialpremise',
            name='type',
            field=models.ForeignKey(db_column='type', to='system.ObjectTypes', verbose_name='non residental type'),
        ),
        migrations.AddField(
            model_name='condominiuminfrastructure',
            name='object_registry',
            field=models.ForeignKey(db_column='object_registry', to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='condominiuminfrastructure',
            name='type',
            field=models.ForeignKey(db_column='type', to='system.ObjectTypes', verbose_name='infrastructure type'),
        ),
        migrations.AddField(
            model_name='condominiumhouse',
            name='object_registry',
            field=models.ForeignKey(to='system.ObjectRegistry', null=True),
        ),
        migrations.AddField(
            model_name='condominiumfloor',
            name='object_registry',
            field=models.ForeignKey(to='system.ObjectRegistry', null=True),
        ),
        migrations.AddField(
            model_name='condominiumfloor',
            name='porch',
            field=models.ForeignKey(db_column='porch', to='system.CondominiumPorch', verbose_name='floor porch'),
        ),
        migrations.AddField(
            model_name='condominiumfloor',
            name='type',
            field=models.ForeignKey(db_column='type', to='system.ObjectTypes', verbose_name='floor type'),
        ),
        migrations.AddField(
            model_name='condominiumconnectedutility',
            name='object_registry',
            field=models.ForeignKey(db_column='object_registry', to='system.ObjectRegistry', verbose_name='object registry'),
        ),
        migrations.AddField(
            model_name='condominiumconnectedutility',
            name='service',
            field=models.ForeignKey(db_column='service', to='system.EngineeringService', verbose_name='service'),
        ),
        migrations.AddField(
            model_name='condominiumconnectedutilitelog',
            name='utility',
            field=models.ForeignKey(db_column='utilite', to='system.CondominiumConnectedUtility'),
        ),
        migrations.AddField(
            model_name='condominiumcommonarea',
            name='object_registry',
            field=models.ForeignKey(db_column='object_registry', to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='condominiumcommonarea',
            name='type',
            field=models.ForeignKey(db_column='type', to='system.ObjectTypes', verbose_name='common area type'),
        ),
        migrations.AddField(
            model_name='condominium',
            name='allowed_modules',
            field=models.ManyToManyField(to='system.Modules', verbose_name='modulles condominium'),
        ),
        migrations.AddField(
            model_name='condominium',
            name='manager',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='manager condominium'),
        ),
        migrations.AddField(
            model_name='user',
            name='condominiums',
            field=models.ManyToManyField(to='system.Condominium', verbose_name='user condominium'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', related_query_name='user', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='owned',
            field=models.ManyToManyField(to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', related_query_name='user', related_name='user_set', help_text='Specific permissions for this user.', verbose_name='user permissions', blank=True),
        ),
        migrations.CreateModel(
            name='CondominiumModules',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('condominium', models.ForeignKey(to='system.Condominium')),
                ('module', models.ForeignKey(to='system.Modules')),
                ('use', models.BooleanField()),
                ('weight', models.IntegerField()),
            ],
            options={
                'db_table': 'condominium_modules',
                'verbose_name_plural': 'condominium modules',
                'verbose_name': 'condominium module',
            },
        ),
        migrations.AlterField(
            model_name='condominiumconnectedutility',
            name='start_value',
            field=models.FloatField(verbose_name='start value'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('type', models.CharField(max_length=2)),
                ('prefix', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=256)),
                ('specialized_name', models.CharField(max_length=256)),
                ('is_residential', models.BooleanField()),
                ('parent', models.ForeignKey(db_column='parent', to='system.City', null=True)),
            ],
            options={
                'db_table': 'city',
                'verbose_name_plural': 'cities',
                'verbose_name': 'city',
            },
        ),
        migrations.RemoveField(
            model_name='condominium',
            name='allowed_modules',
        ),
        migrations.CreateModel(
            name='CondominiumPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('position', models.CharField(max_length=16, choices=[('chairman', 'Сhairman'), ('vice-chairman', 'Vice-Chairman'), ('secretary', 'Secretary'), ('trustee', 'Trustee'), ('member', 'Member')], verbose_name='position')),
            ],
            options={
                'db_table': 'condominium_position',
            },
        ),
        migrations.AddField(
            model_name='condominium',
            name='city',
            field=models.ForeignKey(db_column='city', to='system.City', default=1, verbose_name='city'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='condominium',
            name='document',
            field=models.FileField(upload_to='', default='', verbose_name='document'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='condominiumposition',
            name='condominium',
            field=models.ForeignKey(db_column='condominium', to='system.Condominium', verbose_name='condominium'),
        ),
        migrations.AddField(
            model_name='condominiumposition',
            name='user',
            field=models.ForeignKey(db_column='user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.RemoveField(
            model_name='condominium',
            name='address',
        ),
        migrations.AddField(
            model_name='condominium',
            name='legal_address',
            field=models.CharField(max_length=128, default=' ', verbose_name='legal address'),
            preserve_default=False,
        ),
    ]
