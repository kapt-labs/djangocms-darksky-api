# Third party
from django.conf import settings


# define basic settings
DJANGOCMS_DARKSKY_API_SETTINGS = {
    "api_key": False,
    "cache": 60 * 60,
}

# update settings with values from projectname/settings.py
DJANGOCMS_DARKSKY_API_SETTINGS.update(
    getattr(settings, "DJANGOCMS_DARKSKY_API_SETTINGS", {})
)
