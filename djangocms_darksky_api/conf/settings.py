# Third party
from django.conf import settings


# define basic SEO settings
DJANGOCMS_DARKSKY_API_SETTINGS = {
    "api_key": False,
}

# update SEO settings with values from projectname/settings.py
DJANGOCMS_DARKSKY_API_SETTINGS.update(
    getattr(settings, "DJANGOCMS_DARKSKY_API_SETTINGS", {})
)
