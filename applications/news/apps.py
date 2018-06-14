from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class NewsAppConfig(AppConfig):
    name = "news"
    verbose_name = _("Our news")