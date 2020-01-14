# Third party
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# define basic settings
DJANGOCMS_DARKSKY_API_SETTINGS = {
    "api_key": False,
    "cache": 60 * 60,
}


project_settings = getattr(settings, "DJANGOCMS_DARKSKY_API_SETTINGS", {})
if not project_settings:
    raise ImproperlyConfigured(
        "DJANGOCMS_DARKSKY_API_SETTINGS must be defined in your settings."
    )

try:
    # check if api_key is defined
    project_settings["api_key"]
except KeyError:
    raise ImproperlyConfigured(
        "DJANGOCMS_DARKSKY_API_SETTINGS['api_key'] must be defined in your settings."
    )

# update settings with values from projectname/settings.py
DJANGOCMS_DARKSKY_API_SETTINGS.update(
    getattr(settings, "DJANGOCMS_DARKSKY_API_SETTINGS", {})
)
