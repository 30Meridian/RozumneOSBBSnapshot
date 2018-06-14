from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class IdeasAppConfig(AppConfig):
    name = "ideas"
    verbose_name = _("Ideas")