from django.apps import apps 
from django.urls import reverse
from django.conf import settings
from .models import EveDoctrineSettings
from .forms import EveDoctrineSettingsForm
from packagebinder.bind import PackageBinding, SettingsBinding, TaskBinding, SidebarBinding
import logging 

app_config = apps.get_app_config('django_eveonline_doctrine_manager')

package_binding = PackageBinding(
    package_name=app_config.name, 
    version=app_config.version, 
    url_slug='eveonline', 
)

settings_binding = SettingsBinding(
    package_name=app_config.name, 
    settings_class=EveDoctrineSettings,
    settings_form=EveDoctrineSettingsForm,
)

task_binding = TaskBinding(
    package_name=app_config.name, 
    required_tasks = [
    ],
    optional_tasks = [
        {
            "name": "EVE: Generate Doctrine Reports",
            "task_name": "django_eveonline_doctrine_manager.tasks.update_character_reports",
            "interval": 1,
            "interval_period": "days",
        },
    ]
)

sidebar_binding = SidebarBinding(
    package_name=app_config.name,
    parent_menu_item={
        "fa_icon": 'fa-rocket',
        "name": "Doctrine Menu",
        "url": None, 
    },
    child_menu_items=[
        {
            "fa_icon": "fa-wrench",
            "name": "Fittings",
            "url": reverse("django-eveonline-doctrine-manager-fittings-list"),
        },
        {
            "fa_icon": "fa-shield-alt",
            "name": "Doctrines",
            "url": reverse("django-eveonline-doctrine-manager-doctrines-list"),
        },
        {
            "fa_icon": "fa-book",
            "name": "Skill Plans",
            "url": reverse("django-eveonline-doctrine-manager-skillplans-list"),
        },
        {
            "fa_icon": "fa-shopping-cart",
            "name": "Seeding",
            "url": reverse("django-eveonline-doctrine-manager-fittings-market"),
        },
    ]
)

def create_bindings():
    try:
        package_binding.save()
        settings_binding.save()
        task_binding.save()
        sidebar_binding.save()
    except Exception as e:
        if settings.DEBUG:
            raise(e)
        else:
            logger.error(f"Failed package binding step for {app_config.name}: {e}")
