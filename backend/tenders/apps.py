from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TendersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tenders"
    verbose_name = _("Tenders")
