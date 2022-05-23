from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CollectorConfig(AppConfig):
    name = "apps.collector"
    verbose_name = _("Collector")
