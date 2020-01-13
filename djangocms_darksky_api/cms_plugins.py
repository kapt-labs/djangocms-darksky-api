import json
import requests as re

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from django.core.cache import cache

from .models import DarkskyApi
from .conf import settings


@plugin_pool.register_plugin
class DarkskyApiPlugin(CMSPluginBase):
    model = DarkskyApi
    name = _("Dark Sky Weather")
    render_template = "darkskyapi.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(DarkskyApiPlugin, self).render(context, instance, placeholder)

        if get_language():
            lang = get_language()
        else:
            # default language. bad?
            lang = "fr"

        # key will be in the form "djangocms-darksky-api_fr_latitude_longitude"
        cache_key = (
            "djangocms-darksky-api_"
            + lang
            + "_"
            + str(instance.latitude)
            + "_"
            + str(instance.longitude)
        )

        cached_meteo = cache.get(cache_key)

        if not cached_meteo:
            cached_meteo = self.update_data(
                cache_key, instance.latitude, instance.longitude, lang
            )

        cached_meteo = json.loads(cached_meteo)

        cached_meteo["currently"]["humidity"] = int(
            cached_meteo["currently"]["humidity"] * 100
        )

        context["meteo"] = cached_meteo

        return context

    def get_render_template(self, context, instance, placeholder):
        return "darkskyapi_" + instance.template_size + ".html"

    def update_data(self, key, lat, lon, lang):
        # Request like https://api.darksky.net/forecast/[key]/[latitude],[longitude]?exclude=minutely,hourly,alerts&units=auto&lang=fr
        # See https://darksky.net/dev/docs

        apikey = settings.DJANGOCMS_DARKSKY_API_SETTINGS["api_key"]
        if not apikey:
            raise ValueError(
                _(
                    "DJANGOCMS_DARKSKY_API_SETTINGS['api_key'] is not set in your app's settings.py file."
                )
            )

        url = (
            "https://api.darksky.net/forecast/"
            + apikey
            + "/"
            + str(lat)
            + ","
            + str(lon)
            + "?exclude=minutely,hourly,alerts&units=auto&lang="
            + lang
        )

        try:
            content = re.get(url).json()
        except json.decoder.JSONDecodeError:
            raise ValueError(
                _("The api didn't return a json file as expected.\nURL: " + url)
            )

        cache.set(key, json.dumps(content), 60 * 60)

        return json.dumps(content)
