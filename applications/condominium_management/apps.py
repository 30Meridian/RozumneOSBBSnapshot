from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class ManagementAppConfig(AppConfig):
    name = 'condominium_management'
    verbose_name = _('Condominium management')