from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class NewsletterAppConfig(AppConfig):
    name = 'newsletter'
    verbose_name = _("Our newsletter")