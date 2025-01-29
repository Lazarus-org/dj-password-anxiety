from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PasswordAnxietyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "password_anxiety"
    verbose_name = _("Django Password Anxiety")
    
