from django.db import models
from system.models import User, Condominium
from ckeditor_uploader.fields import RichTextUploadingField
from stdimage.models import StdImageField
import uuid
from django.utils.translation import ugettext_lazy as _

# генерируем псевдоуникальный файлнейм для загружаемых изображений
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'news/%s' % filename

class News(models.Model):
    condominium = models.ForeignKey(Condominium, db_column='condominium', verbose_name = _('Your cond'))
    author = models.ForeignKey(User, db_column='author', verbose_name = _('Author'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name = _('Datetime'))
    datetime_publish = models.DateTimeField(verbose_name = _('Datetime_publish'))
    title = models.CharField(max_length=150, verbose_name = _('Title'))
    shortdesc = models.CharField(max_length=300, verbose_name = _('Short description'))
    text = RichTextUploadingField(verbose_name = _('News text'))
    mainimg = StdImageField(upload_to=get_file_path, variations={
        'large': (600, 400),
        'thumbnail': {"width": 100, "height": 100, "crop": True}
    }, verbose_name = _('Main img'))
    publish = models.BooleanField(verbose_name = _('Publish'))
    public = models.BooleanField(verbose_name=_('Public'), default=True,
                                 help_text=_('Allows to view article for users from other condominiums'))

    class Meta:
        managed = True
        db_table = 'news'
        verbose_name = _('News')
        verbose_name_plural = _('your news')

    def __str__(self):
        return self.title