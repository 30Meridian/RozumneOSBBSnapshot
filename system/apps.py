from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SystemAppConfig(AppConfig):
    name = "system"
    verbose_name = _("systems")