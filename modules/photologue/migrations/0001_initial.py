# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sortedm2m.fields
import photologue.models
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_added', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('title', models.CharField(verbose_name='title', unique=True, max_length=250)),
                ('slug', models.SlugField(verbose_name='title slug', unique=True, help_text='A "slug" is a unique URL-friendly title for an object.', max_length=250)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('is_public', models.BooleanField(verbose_name='is public', help_text='Public galleries will be displayed in the default views.', default=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'ordering': ['-date_added'],
                'verbose_name_plural': 'galleries',
                'get_latest_by': 'date_added',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(verbose_name='image', upload_to=photologue.models.get_storage_path)),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, help_text='Date image was taken; is obtained from the image EXIF data.', blank=True)),
                ('view_count', models.PositiveIntegerField(verbose_name='view count', editable=False, default=0)),
                ('crop_from', models.CharField(verbose_name='crop from', max_length=10, default='center', blank=True, choices=[('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left'), ('center', 'Center (Default)')])),
                ('title', models.CharField(verbose_name='title', unique=True, max_length=250)),
                ('slug', models.SlugField(verbose_name='slug', unique=True, help_text='A "slug" is a unique URL-friendly title for an object.', max_length=250)),
                ('caption', models.TextField(verbose_name='caption', blank=True)),
                ('date_added', models.DateTimeField(verbose_name='date added', default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(verbose_name='is public', help_text='Public photographs will be displayed in the default views.', default=True)),
            ],
            options={
                'verbose_name': 'photo',
                'ordering': ['-date_added'],
                'verbose_name_plural': 'photos',
                'get_latest_by': 'date_added',
            },
        ),
        migrations.CreateModel(
            name='PhotoEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', unique=True, max_length=30)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('transpose_method', models.CharField(verbose_name='rotate or flip', max_length=15, blank=True, choices=[('FLIP_LEFT_RIGHT', 'Flip left to right'), ('FLIP_TOP_BOTTOM', 'Flip top to bottom'), ('ROTATE_90', 'Rotate 90 degrees counter-clockwise'), ('ROTATE_270', 'Rotate 90 degrees clockwise'), ('ROTATE_180', 'Rotate 180 degrees')])),
                ('color', models.FloatField(verbose_name='color', help_text='A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.', default=1.0)),
                ('brightness', models.FloatField(verbose_name='brightness', help_text='A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.', default=1.0)),
                ('contrast', models.FloatField(verbose_name='contrast', help_text='A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.', default=1.0)),
                ('sharpness', models.FloatField(verbose_name='sharpness', help_text='A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.', default=1.0)),
                ('filters', models.CharField(verbose_name='filters', max_length=200, help_text='Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". Image filters will be applied in order. The following filters are available: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE.', blank=True)),
                ('reflection_size', models.FloatField(verbose_name='size', help_text='The height of the reflection as a percentage of the orignal image. A factor of 0.0 adds no reflection, a factor of 1.0 adds a reflection equal to the height of the orignal image.', default=0)),
                ('reflection_strength', models.FloatField(verbose_name='strength', help_text='The initial opacity of the reflection gradient.', default=0.6)),
                ('background_color', models.CharField(verbose_name='color', max_length=7, help_text='The background color of the reflection gradient. Set this to match the background color of your page.', default='#FFFFFF')),
            ],
            options={
                'verbose_name': 'photo effect',
                'verbose_name_plural': 'photo effects',
            },
        ),
        migrations.CreateModel(
            name='PhotoSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', unique=True, max_length=40, help_text='Photo size name should contain only letters, numbers and underscores. Examples: "thumbnail", "display", "small", "main_page_widget".', validators=[django.core.validators.RegexValidator(regex='^[a-z0-9_]+$', message='Use only plain lowercase letters (ASCII), numbers and underscores.')])),
                ('width', models.PositiveIntegerField(verbose_name='width', help_text='If width is set to "0" the image will be scaled to the supplied height.', default=0)),
                ('height', models.PositiveIntegerField(verbose_name='height', help_text='If height is set to "0" the image will be scaled to the supplied width', default=0)),
                ('quality', models.PositiveIntegerField(verbose_name='quality', help_text='JPEG image quality.', default=70, choices=[(30, 'Very Low'), (40, 'Low'), (50, 'Medium-Low'), (60, 'Medium'), (70, 'Medium-High'), (80, 'High'), (90, 'Very High')])),
                ('upscale', models.BooleanField(verbose_name='upscale images?', help_text='If selected the image will be scaled up if necessary to fit the supplied dimensions. Cropped sizes will be upscaled regardless of this setting.', default=False)),
                ('crop', models.BooleanField(verbose_name='crop to fit?', help_text='If selected the image will be scaled and cropped to fit the supplied dimensions.', default=False)),
                ('pre_cache', models.BooleanField(verbose_name='pre-cache?', help_text='If selected this photo size will be pre-cached as photos are added.', default=False)),
                ('increment_count', models.BooleanField(verbose_name='increment view count?', help_text='If selected the image\'s "view_count" will be incremented when this photo size is displayed.', default=False)),
                ('effect', models.ForeignKey(verbose_name='photo effect', null=True, blank=True, related_name='photo_sizes', to='photologue.PhotoEffect')),
            ],
            options={
                'verbose_name': 'photo size',
                'ordering': ['width', 'height'],
                'verbose_name_plural': 'photo sizes',
            },
        ),
        migrations.CreateModel(
            name='Watermark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', unique=True, max_length=30)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('image', models.ImageField(verbose_name='image', upload_to='photologue/watermarks')),
                ('style', models.CharField(verbose_name='style', max_length=5, default='scale', choices=[('tile', 'Tile'), ('scale', 'Scale')])),
                ('opacity', models.FloatField(verbose_name='opacity', help_text='The opacity of the overlay.', default=1)),
            ],
            options={
                'verbose_name': 'watermark',
                'verbose_name_plural': 'watermarks',
            },
        ),
        migrations.AddField(
            model_name='photosize',
            name='watermark',
            field=models.ForeignKey(verbose_name='watermark image', null=True, blank=True, related_name='photo_sizes', to='photologue.Watermark'),
        ),
        migrations.AddField(
            model_name='photo',
            name='effect',
            field=models.ForeignKey(verbose_name='effect', null=True, blank=True, related_name='photo_related', to='photologue.PhotoEffect'),
        ),
        migrations.AddField(
            model_name='photo',
            name='sites',
            field=models.ManyToManyField(verbose_name='sites', to='sites.Site', blank=True),
        ),
        migrations.AddField(
            model_name='gallery',
            name='photos',
            field=sortedm2m.fields.SortedManyToManyField(verbose_name='photos', to='photologue.Photo', help_text=None, blank=True, related_name='galleries'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='sites',
            field=models.ManyToManyField(verbose_name='sites', to='sites.Site', blank=True),
        ),
    ]
