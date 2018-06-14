from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

from system.models import Condominium, User


class ManagementPages(models.Model):
    condominium = models.ForeignKey(Condominium, db_column='condominium', verbose_name=_('Pages condominium'),
                                    on_delete=models.CASCADE)
    slug = models.CharField(max_length=32, verbose_name=_('Pages slug'))
    title = models.CharField(max_length=128, verbose_name=_('Pages title'))
    content = RichTextUploadingField(verbose_name=_('Pages content'))
    author = models.ForeignKey(User, db_column='author', verbose_name=_('Pages author'),
                               blank=True, null=True, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Datetime'))
    datetime_update = models.DateTimeField(auto_now=True, verbose_name=_('Datetime update'))

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('condominium', 'slug')
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


# class ProxyCondominium(Condominium):
#     class Meta:
#         proxy = True
#         verbose_name = _('Condominium modules')
#         verbose_name_plural = _('Condominium modules')
