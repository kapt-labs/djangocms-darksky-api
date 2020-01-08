import json
import random

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from django.core.cache import cache

from .models import DarkskyApi


@plugin_pool.register_plugin
class DarkskyApiPlugin(CMSPluginBase):
    model = DarkskyApi
    name = _("Dark Sky Weather")
    render_template = "darkskyapi.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(DarkskyApiPlugin, self).render(context, instance, placeholder)

        # key will be in the form "djangocms-darksky-api_fr_latitude_longitude"
        cache_key = (
            "djangocms-darksky-api_"
            + translation.get_language()
            + "_"
            + str(instance.latitude)
            + "_"
            + str(instance.longitude)
        )

        cached_meteo = cache.get(cache_key)

        if not cached_meteo:
            t = random.randint(1, 50)
            cache.set(cache_key, json.dumps({"temperature": t}), 60 * 60)  # one hour
            cached_meteo = json.dumps({"temperature": t})

        cached_meteo = json.loads(cached_meteo)

        context["meteo"] = cached_meteo

        DarkskyApiPlugin.render_template = "darkskyapi_" + instance.template + ".html"

        return context
