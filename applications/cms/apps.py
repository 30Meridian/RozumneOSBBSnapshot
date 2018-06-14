from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class CMSAppConfig(AppConfig):
    name = 'cms'
    verbose_name = _('Additional materials')