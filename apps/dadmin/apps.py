# from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.utils.module_loading import autodiscover_modules


class DmallAdminConfig(AdminConfig):
    name = 'dadmin'
    default_site = 'dadmin.admin.DadminSite'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        autodiscover_modules("byadmin")
