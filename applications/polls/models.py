from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from stdimage.models import StdImageField
import uuid

from system.models import Condominium, User
from django.utils.translation import ugettext_lazy as _

# генерируем псевдоуникальный файлнейм для загружаемых изображений
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'polls/%s' % filename


class Poll(models.Model):
    question = models.CharField(max_length=255, verbose_name = _('Question'))
    description = models.TextField(blank=True, verbose_name = _('Description'))
    condominium = models.ForeignKey(Condominium, db_column='condominium_ref', verbose_name = _('Poll condominium'))
    date_start = models.DateField(verbose_name = _('date start'))
    date_end = models.DateField(verbose_name = _('date end'))
    active = models.BooleanField(default=True, verbose_name = _('Active'))
    public = models.BooleanField(verbose_name=_('Public'), default=True,
                                 help_text=_('Allows to view polls for users from other condominiums'))
    archive = models.BooleanField(default=False, verbose_name = _('Archive'))

    class Meta:
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')

    def count_choices(self):
        return self.choice_set.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    def can_vote(self, user):
        if user:
            if(self.vote_set.filter(user=user).exists() or self.active == False or self.archive == True or (self.condominium not in user.condominiums.all())):
                return False
            else:
                return True
        else:
            return False

    def has_image(self):
        if self.choice_set.all().exclude(image=''):
            return True
        else:
            return False

    count_choices.short_description = _('count choices')
    count_total_votes.short_description = _('count total votes')
    can_vote.short_description = _('can vote')
    def __str__(self):
        return self.question

    def clean(self):
        if not self.question:
            super(Poll, self).clean()
        elif self.date_start and self.date_end :
            if self.date_start >= self.date_end:
                raise ValidationError(
                    _('A date of start can not be more than date end or equal '))


class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name = _('Choice of poll'))
    choice = models.CharField(max_length=255, verbose_name = _('user choice'),blank=True)
    image = StdImageField(blank=True, upload_to=get_file_path, variations={
        'large': (600, 400),
        'thumbnail': {"width": 300, "height": 300, "crop": True}
    }, verbose_name=_('poll image'))

    def count_votes(self):
        return self.vote_set.count()

    class Meta:
        ordering = ['choice']
        verbose_name = _('Choice of poll')
        verbose_name_plural = _('Choices of poll')

    def __str__(self):
        return self.choice



class Vote(models.Model):
    user = models.ForeignKey(User, verbose_name = _('vote of user'))
    poll = models.ForeignKey(Poll, verbose_name = _('vote of poll'))
    choice = models.ForeignKey(Choice, verbose_name = _('vote of choice'))

    # def __unicode__(self):
    #     return u'Vote for %s' % (self.choice)

    def __str__(self):
        return "{}".format(_("Vote"))

    class Meta:
        unique_together = (('user', 'poll'))
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
