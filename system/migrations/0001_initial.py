# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('sites', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, max_length=30)),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('phone', models.CharField(verbose_name='user phone', null=True, max_length=64)),
                ('middle_name', models.CharField(verbose_name='middle name', max_length=64)),
                ('address', models.CharField(verbose_name='user adress', default='', blank=True, max_length=128)),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': 'auth user',
                'managed': True,
                'verbose_name_plural': 'auth user',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('index', models.IntegerField(verbose_name='address index')),
                ('street_type', models.CharField(verbose_name='address street_type', max_length=32)),
                ('street_name', models.CharField(verbose_name='address street_name', max_length=64)),
                ('number', models.IntegerField(verbose_name='address number')),
                ('symbol', models.CharField(verbose_name='address symbol', null=True, max_length=2, blank=True)),
                ('pavilion', models.CharField(verbose_name='address pavilion', null=True, max_length=16, blank=True)),
            ],
            options={
                'db_table': 'address',
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('removed', models.DateTimeField(editable=False, default=None, null=True, blank=True)),
                ('name', models.CharField(verbose_name='name condominium', default='Condominium', blank=True, max_length=64)),
                ('slug', models.CharField(unique=True, max_length=64, verbose_name='slug condominium')),
                ('description', models.CharField(verbose_name='description condominium', null=True, max_length=256, blank=True)),
                ('votes', models.IntegerField(verbose_name='votes condominium', default=10)),
                ('ideas_days', models.IntegerField(verbose_name='ideas_days condominium', default=30)),
                ('ideas_number_templ', models.CharField(verbose_name='ideas number condominium', default='10/%s', null=True, max_length=64, blank=True)),
                ('address', models.ForeignKey(to='system.Address', verbose_name='address condominium', db_column='address', blank=True, null=True)),
            ],
            options={
                'db_table': 'condominium',
                'verbose_name': 'condominium',
                'verbose_name_plural': 'condominiums',
            },
        ),
        migrations.CreateModel(
            name='CondominiumCommonArea',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('area', models.FloatField(verbose_name='common area-area')),
                ('description', models.CharField(verbose_name='common area description', null=True, max_length=255, blank=True)),
            ],
            options={
                'db_table': 'condominium_common_area',
                'verbose_name': 'Common area',
                'verbose_name_plural': 'Common Areas',
            },
        ),
        migrations.CreateModel(
            name='CondominiumConnectedUtiliteLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('current_value', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'condominium_connected_utilities_log',
                'verbose_name': 'utility log',
                'verbose_name_plural': 'utility logs',
            },
        ),
        migrations.CreateModel(
            name='CondominiumConnectedUtility',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('subsidy', models.FloatField(default=0.0)),
                ('start_value', models.FloatField()),
            ],
            options={
                'db_table': 'condominium_connected_utilities',
                'verbose_name': 'utilities',
                'verbose_name_plural': 'utilities',
            },
        ),
        migrations.CreateModel(
            name='CondominiumFloor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='floor name', null=True, max_length=32, blank=True)),
                ('residential_count', models.IntegerField(verbose_name='floor residential_count')),
                ('non_residential_count', models.IntegerField(verbose_name='floor non_residential_count', default=0)),
                ('lighting_points', models.IntegerField(verbose_name='floor lighting_points', default=1)),
                ('description', models.CharField(verbose_name='floor description', null=True, max_length=255, blank=True)),
            ],
            options={
                'db_table': 'condominium_floor',
                'verbose_name': 'floor',
                'verbose_name_plural': 'floors',
            },
        ),
        migrations.CreateModel(
            name='CondominiumHouse',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='house name ', null=True, max_length=64, blank=True)),
                ('area', models.FloatField(verbose_name='house area ')),
                ('residential_area', models.FloatField(verbose_name='house residential area ')),
                ('entrance_count', models.IntegerField(verbose_name='house entrance count ')),
                ('min_floors', models.IntegerField(verbose_name='house min floors ')),
                ('max_floors', models.IntegerField(verbose_name='house max floors ')),
                ('residential_count', models.IntegerField(verbose_name='house residential count ')),
                ('elevators_count', models.IntegerField(verbose_name='house elevators count ')),
                ('description', models.CharField(verbose_name='house description ', null=True, max_length=255, blank=True)),
                ('address', models.ForeignKey(verbose_name='house address ', db_column='address', to='system.Address')),
                ('condominium', models.ForeignKey(verbose_name='house condominium ', db_column='condominium', to='system.Condominium')),
            ],
            options={
                'db_table': 'condominium_house',
                'verbose_name': 'house',
                'verbose_name_plural': 'houses',
            },
        ),
        migrations.CreateModel(
            name='CondominiumInfrastructure',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('area', models.FloatField(verbose_name='infrastructure area')),
                ('description', models.CharField(verbose_name='infrastructure description', null=True, max_length=255, blank=True)),
            ],
            options={
                'db_table': 'condominium_infrastructure',
                'verbose_name': 'infrastructure',
                'verbose_name_plural': 'infrastructures',
            },
        ),
        migrations.CreateModel(
            name='CondominiumNonResidentialPremise',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='non residental number', null=True, blank=True)),
                ('area', models.FloatField(verbose_name='non residental area')),
                ('description', models.CharField(verbose_name='non residental description', null=True, max_length=255, blank=True)),
                ('floor', models.ForeignKey(verbose_name='non residental floor', db_column='floor', to='system.CondominiumFloor')),
            ],
            options={
                'db_table': 'condominium_non_residential_premise',
                'verbose_name': 'condominium non residential premise',
                'verbose_name_plural': 'condominium non residential premises',
            },
        ),
        migrations.CreateModel(
            name='CondominiumPorch',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='porch number')),
                ('name', models.CharField(verbose_name='porch name', null=True, max_length=64, blank=True)),
                ('floors_count', models.IntegerField(verbose_name='porch floors_count')),
                ('residential_count', models.IntegerField(verbose_name='porch residential_count')),
                ('non_residential_count', models.IntegerField(verbose_name='porch non_residential_count', default=0)),
                ('lighting_points', models.IntegerField(verbose_name='porch lighting_points')),
                ('elevators_count', models.IntegerField(verbose_name='porch elevators_count')),
                ('description', models.CharField(verbose_name='porch description', null=True, max_length=255, blank=True)),
                ('house', models.ForeignKey(verbose_name='porch house', db_column='house', to='system.CondominiumHouse')),
            ],
            options={
                'db_table': 'condominium_porch',
                'verbose_name': 'porch',
                'verbose_name_plural': 'porches',
            },
        ),
        migrations.CreateModel(
            name='CondominiumResidentialPremise',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='residental number ')),
                ('area', models.FloatField(verbose_name='residental area ')),
                ('residential_area', models.FloatField(verbose_name='residental residential area ')),
                ('heating_area', models.FloatField(verbose_name='residental heating area ')),
                ('rooms_count', models.IntegerField(verbose_name='residental rooms count ')),
                ('residents_count', models.IntegerField(verbose_name='residental residents_count ')),
                ('pets_count', models.IntegerField(verbose_name='residental pets count ')),
                ('description', models.CharField(verbose_name='residental description ', null=True, max_length=255, blank=True)),
                ('floor', models.ForeignKey(verbose_name='residental floor', db_column='floor', to='system.CondominiumFloor')),
            ],
            options={
                'db_table': 'condominium_residential_premise',
                'verbose_name': 'condominium residential premise',
                'verbose_name_plural': 'condominium residential premises',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('te', models.CharField(max_length=10)),
                ('np', models.CharField(max_length=2)),
                ('nu', models.CharField(max_length=256)),
                ('id_reg', models.CharField(max_length=2)),
                ('d_typ', models.CharField(max_length=1)),
                ('id_distr', models.CharField(max_length=2)),
                ('pref', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=256)),
                ('id_distr_un', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'district',
                'verbose_name': 'district',
                'verbose_name_plural': 'districts',
            },
        ),
        migrations.CreateModel(
            name='EngineeringService',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('subsidy', models.BooleanField(default=False)),
                ('value', models.FloatField()),
                ('measurement_units', models.CharField(max_length=64)),
                ('determine', models.CharField(max_length=128)),
                ('datetime_crated', models.DateTimeField(auto_now_add=True)),
                ('datetime_changed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(null=True, max_length=255, blank=True)),
                ('condominium', models.ForeignKey(db_column='condominium', to='system.Condominium')),
            ],
            options={
                'db_table': 'engineering_service',
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(null=True, max_length=32, blank=True)),
                ('slug', models.CharField(null=True, max_length=32, blank=True)),
                ('icon', models.CharField(default='fa fa-plus', null=True, max_length=64, blank=True)),
            ],
            options={
                'db_table': 'modules',
                'verbose_name': 'module',
                'verbose_name_plural': 'modules',
            },
        ),
        migrations.CreateModel(
            name='ObjectRegistry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(default='', null=True, max_length=64, blank=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_changed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(null=True, max_length=255, blank=True)),
                ('condominium', models.ForeignKey(to='system.Condominium')),
            ],
            options={
                'db_table': 'object_registry',
                'verbose_name': 'object registry',
                'verbose_name_plural': 'objects registry',
            },
        ),
        migrations.CreateModel(
            name='ObjectTypes',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('category', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(null=True, max_length=256, blank=True)),
            ],
            options={
                'db_table': 'object_types',
                'verbose_name': 'object type',
                'verbose_name_plural': 'object types',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('te', models.CharField(max_length=10)),
                ('np', models.CharField(null=True, max_length=2, blank=True)),
                ('nu', models.CharField(max_length=256)),
                ('id_reg', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'region',
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('te', models.CharField(max_length=10)),
                ('np', models.CharField(max_length=2)),
                ('nu', models.CharField(max_length=256)),
                ('id_reg', models.CharField(max_length=2)),
                ('d_typ', models.CharField(max_length=1)),
                ('id_distr', models.CharField(max_length=2)),
                ('pref', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=256)),
                ('id_distr_un', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'town',
                'verbose_name': 'town',
                'verbose_name_plural': 'towns',
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column='user_changed', related_name='changed'),
        ),
        migrations.AddField(
            model_name='objectregistry',
            name='user_created',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column='user_created', related_name='created'),
        ),
        migrations.AddField(
            model_name='condominiumresidentialpremise',
            name='object_registry',
            field=models.ForeignKey(to='system.ObjectRegistry', null=True),
        ),
        migrations.AddField(
            model_name='condominiumresidentialpremise',
            name='type',
            field=models.ForeignKey(verbose_name='residental type ', db_column='type', to='system.ObjectTypes'),
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
            field=models.ForeignKey(verbose_name='non residental type', db_column='type', to='system.ObjectTypes'),
        ),
        migrations.AddField(
            model_name='condominiuminfrastructure',
            name='object_registry',
            field=models.ForeignKey(db_column='object_registry', to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='condominiuminfrastructure',
            name='type',
            field=models.ForeignKey(verbose_name='infrastructure type', db_column='type', to='system.ObjectTypes'),
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
            field=models.ForeignKey(verbose_name='floor porch', db_column='porch', to='system.CondominiumPorch'),
        ),
        migrations.AddField(
            model_name='condominiumfloor',
            name='type',
            field=models.ForeignKey(verbose_name='floor type', db_column='type', to='system.ObjectTypes'),
        ),
        migrations.AddField(
            model_name='condominiumconnectedutility',
            name='object_registry',
            field=models.ForeignKey(db_column='object_registry', to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='condominiumconnectedutility',
            name='service',
            field=models.ForeignKey(db_column='service', to='system.EngineeringService'),
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
            field=models.ForeignKey(verbose_name='common area type', db_column='type', to='system.ObjectTypes'),
        ),
        migrations.AddField(
            model_name='condominium',
            name='allowed_modules',
            field=models.ManyToManyField(verbose_name='modulles condominium', to='system.Modules'),
        ),
        migrations.AddField(
            model_name='condominium',
            name='manager',
            field=models.ManyToManyField(verbose_name='manager condominium', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.ForeignKey(verbose_name='address district', db_column='district', to='system.District', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.ForeignKey(verbose_name='address region', db_column='region', to='system.Region'),
        ),
        migrations.AddField(
            model_name='address',
            name='town',
            field=models.ForeignKey(verbose_name='address town', db_column='town', to='system.Town', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='condominiums',
            field=models.ManyToManyField(verbose_name='user condominium', to='system.Condominium'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', verbose_name='groups', related_query_name='user', related_name='user_set', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='owned',
            field=models.ManyToManyField(to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', related_query_name='user', related_name='user_set', blank=True),
        ),
    ]
