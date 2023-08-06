from django.apps import AppConfig
from django.apps import apps
from django.conf import settings


class DjangoEveOnlineDoctrineManagerConfig(AppConfig):
    name = 'django_eveonline_doctrine_manager'
    package_name = __import__(name).__package_name__
    version = __import__(name).__version__
    verbose_name = "EVE Doctrine Manager"
    url_slug = 'eveonline'
    install_requires = ['crispy_forms', 'django_eveonline_connector']

    def ready(self):
        from django.db.models.signals import post_save
        from .models import EveFitting
        from .signals import populate_low_priority_fitting_fields

        for requirement in self.install_requires:
            if requirement not in settings.INSTALLED_APPS:
                raise Exception(f"Missing '{requirement}' in INSTALLED_APPS")

        post_save.connect(
            populate_low_priority_fitting_fields, sender=EveFitting)


        if apps.is_installed('packagebinder'):
            from .bindings import create_bindings
            create_bindings()