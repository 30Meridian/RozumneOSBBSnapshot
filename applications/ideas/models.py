from system.models import User, Condominium
import uuid
from stdimage.models import StdImageField
from django.db import models
from django.utils.translation import ugettext_lazy as _


# генерируем псевдоуникальный файлнейм для загружаемых изображений
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'ideas/%s' % filename


class Ideas(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('idea title'))
    image = StdImageField(blank=True, upload_to=get_file_path, variations={
        'large': (600, 400),
        'thumbnail': {"width": 100, "height": 100, "crop": True}
    }, verbose_name=_('idea image'))
    text = models.CharField(max_length=1000, verbose_name=_('idea text'))
    status = models.ForeignKey('IdeasStatuses', db_column='status', verbose_name=_('idea status'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('idea create_date'))
    owner_user = models.ForeignKey(User,blank=True, null=True, db_column='owner_user', verbose_name=_('idea owner_user'))
    resolution = models.CharField(max_length=3000, blank=True, null=True, verbose_name=_('idea resolution'))
    condominium = models.ForeignKey(Condominium, db_column='condominium', verbose_name=_('idea condominium'))
    when_approve = models.DateTimeField(verbose_name=_('idea when_approve'),blank=True, null=True)
    anonymous = models.BooleanField(verbose_name=_('idea anonymous'))
    public = models.BooleanField(verbose_name=_('Public'), default=True,
                                 help_text=_('Allows to view idea for users from other condominiums'))

    class Meta:
        managed = True
        db_table = 'ideas'
        verbose_name = _('Idea')
        verbose_name_plural = _('Ideas')

    #проверочка для того что бы вывести в списке петиций голосовал ли пользователь или нет за петициию
    def voters(self):
        return [v.user for v in self.ideasvoices_set.all()]

    #проверочка что бы вывести количество голосов для петиций без заблокированых
    def vote_count(self):
        return self.ideasvoices_set.exclude(block = 1).all().count()

    def __str__(self):
        return self.title


class IdeasActivity(models.Model):
    datatime = models.DateTimeField(auto_now_add=True, verbose_name=_('activity datatime'))
    activity = models.CharField(max_length=500, verbose_name=_('activity activity'))
    user = models.ForeignKey(User, db_column='user', verbose_name=_('activity user'))
    ip = models.CharField(max_length=500, verbose_name=_('activity ip'))
    idea = models.ForeignKey(Ideas, db_column='idea', verbose_name=_('activity idea'))

    class Meta:
        managed = True
        db_table = 'ideas_activity'
        verbose_name = _('Activity')
        verbose_name_plural = _("Activities")

    def __str__(self):
        return self.activity

class IdeasStatuses(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('status title'))

    class Meta:
        managed = True
        db_table = 'ideas_statuses'
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def __str__(self):
        return self.title


class IdeasVoices(models.Model):
    idea = models.ForeignKey(Ideas, db_column='idea', blank=True, null=True, verbose_name=_('Voice idea'))
    user = models.ForeignKey(User, db_column='user', blank=True, null=True, verbose_name=_('Voice user'))
    block = models.CharField(max_length=1, blank=True, null=True, verbose_name=_('Voice block'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Voice created'))
    ip = models.CharField(max_length=50, verbose_name=_('Voice ip'))

    class Meta:
        managed = True
        db_table = 'ideas_voices'
        verbose_name = _('Voice')
        verbose_name_plural = _('Voices')
        ordering = ('idea',)
    def __str__(self):
        return '{} ({})'.format(self.idea, self.user)