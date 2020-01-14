from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.db import models


class DarkskyApi(CMSPlugin):
    latitude = models.DecimalField(
        verbose_name=_("Latitude"),
        max_digits=27,
        decimal_places=25,
        db_index=True,
        help_text=_("e.g.: 44.988208"),
    )
    longitude = models.DecimalField(
        verbose_name=_("Longitude"),
        max_digits=27,
        decimal_places=24,
        db_index=True,
        help_text=_("e.g.: 4.976723"),
    )

    TEMPLATE_CHOICES = [("light", _("Light")), ("full", _("Full"))]

    template = models.CharField(
        verbose_name=_("Template"),
        max_length=5,
        choices=TEMPLATE_CHOICES,
        default="light",
    )
