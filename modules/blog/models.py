from django.db import models
from system.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from stdimage.models import StdImageField
import uuid
from system.validators import validate_file_extension
from django.utils.translation import ugettext_lazy as _

# генерируем псевдоуникальный файлнейм для загружаемых изображений
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'blog/%s' % filename

def get_document_path(instance, filename):
    ext = filename.split('.')
    filename = "{}_{}.{}".format(ext[0],instance.article.id,ext[-1])
    return 'blog/documents/%s' % filename


class Articles(models.Model):
    author = models.ForeignKey(User, db_column='author', verbose_name=_('Author'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Datetime'))
    datetime_publish = models.DateTimeField(verbose_name=_('Datetime_publish'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    shortdesc = models.CharField(max_length=300, verbose_name=_('Short description'))
    text = RichTextUploadingField(verbose_name=_('News text'))
    mainimg = StdImageField(upload_to=get_file_path, variations={
        'large': (600, 400),
        'thumbnail': {"width": 70, "height": 60, "crop": True},
        'middle': {"width": 300, "height": 200, "crop": True}
    }, verbose_name=_('Main img'))
    publish = models.BooleanField(verbose_name=_('Publish'))
    categories = models.ManyToManyField('Category', blank=True, verbose_name=_('Categories'))


    class Meta:
        managed = True
        verbose_name = _('News')
        verbose_name_plural = _('your news')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    slug = models.CharField(max_length=100, unique=True, verbose_name=_('slug'))

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = ''


class Like(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Articles)

    class Meta:
        unique_together = ('user', 'article')


class Documents(models.Model):
    article = models.ForeignKey(Articles)
    file = models.FileField(upload_to=get_document_path, validators=[validate_file_extension],
                                verbose_name=_('Docs'))

    def filename(self):
        # removed 'blog/documents/'
        return self.file.name[15:]

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class Photo(models.Model):
    image = models.ImageField(max_length=100, verbose_name=_('image'))
    article = models.ForeignKey(Articles, verbose_name=_('article'))

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photo')

    def __str__(self):
        return _('Photo for article: ') + self.article.title