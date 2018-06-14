import datetime
import uuid

from django.db import models
from system.models import Condominium, User
from django.utils.translation import ugettext_lazy as _
from stdimage.models import StdImageField

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'problems/%s' % filename


class Items(models.Model):
    title = models.CharField(max_length=255,verbose_name=_('Item Title'), null=False)
    description = models.CharField(max_length=3000, verbose_name=_('Item Description'), blank=True, null=True)
    photo = StdImageField(blank=True,verbose_name=_('Item Photo'), null=True,upload_to=get_file_path, variations={
        'large': (600, 400),
        'thumbnail': {"width": 100, "height": 100, "crop": True}
    })

    user_ref = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name=_('user'), related_name="problems_user_ref")
    condominium_ref = models.ForeignKey(Condominium, verbose_name=_('Condominium'), related_name="problems_condominium",on_delete= models.CASCADE)
    create = models.DateTimeField(auto_now_add=True, verbose_name=_('create'))
    last_update = models.DateTimeField(auto_now_add=True, verbose_name=_('last_update'))
    public = models.BooleanField(verbose_name=_('Public'), default=True,
                                 help_text=_('Allows to view problem for users from other condominiums'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    @property
    def status(self):
        return Statuses.objects.all().filter(item_ref_id = self.id).status

    @property
    def days_left(self):
        return (self.create + datetime.timedelta(days=self.condominium_ref.problem_days) - datetime.datetime.now()).days


class Statuses(models.Model):
    '''Class implements an support ticket item'''
    STATUSES = {
        ('pedding', _('pedding')),
        ('inwork', _('inwork')),
        ('waiting_board_decision', _('waiting_board_decision')),
        ('waiting_general_meeting', _('waiting_general_meeting')),
        ('done', _('done')),
        ('reject',_('reject')),
    }
    item_ref = models.ForeignKey(Items, verbose_name=_('Item'), on_delete=models.CASCADE, related_name="problems_items")
    status = models.CharField(max_length=64, choices=STATUSES, verbose_name=_('status'))
    create = models.DateTimeField(auto_now_add=True, verbose_name=_('create'))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_('deadline'))
    resolution = models.CharField(max_length=3000,blank=True, verbose_name=_('resolution'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="status_owner", verbose_name=_('owner'))

    def __str__(self):
        return '{}'.format(_(self.status))

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _("Statuses")

class Files(models.Model):
    filename = models.CharField(max_length=255)
    create = models.DateTimeField(auto_now_add=True)
    item_ref =  models.ForeignKey(Items, verbose_name=_('Item'), related_name="problems_files_items")
