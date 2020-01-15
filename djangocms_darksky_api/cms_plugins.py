import json
import requests as re

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings

from django.core.cache import cache

from .models import DarkskyApi
from .conf import settings as plugin_settings


@plugin_pool.register_plugin
class DarkskyApiPlugin(CMSPluginBase):
    model = DarkskyApi
    name = _("Dark Sky Weather")
    cache = True

    def render(self, context, instance, placeholder):
        context = super(DarkskyApiPlugin, self).render(context, instance, placeholder)

        lang = get_language()[:2] or settings.LANGUAGE_CODE[:2]

        # key will be in the form "djangocms-darksky-api_fr_latitude_longitude"
        cache_key = (
            "djangocms-darksky-api_"
            + lang
            + "_"
            + str(instance.latitude)
            + "_"
            + str(instance.longitude)
        )

        # get content from cache
        cached_meteo = cache.get(cache_key)

        if not cached_meteo:
            # or get content from api call (& store it to the cache too)
            cached_meteo = self.update_data(
                cache_key, instance.latitude, instance.longitude, lang
            )

        cached_meteo = json.loads(cached_meteo)

        try:
            # from value between 0 - 1 to percentage
            cached_meteo["currently"]["humidity"] = int(
                cached_meteo["currently"]["humidity"] * 100
            )
        except KeyError:
            print(cached_meteo)

        context["meteo"] = cached_meteo

        return context

    def get_render_template(self, context, instance, placeholder):
        # return template name according to instance values
        return "darkskyapi_" + instance.template + ".html"

    def get_cache_expiration(self, request, instance, placeholder):
        return plugin_settings.DJANGOCMS_DARKSKY_API_SETTINGS["cache"]

    def update_data(self, key, lat, lon, lang):
        # Request like https://api.darksky.net/forecast/[key]/[latitude],[longitude]?exclude=minutely,hourly,alerts,flags&units=si&lang=[lang]
        # See https://darksky.net/dev/docs

        apikey = plugin_settings.DJANGOCMS_DARKSKY_API_SETTINGS["api_key"]

        url = "https://api.darksky.net/forecast/{apikey}/{lat},{lon}?exclude=minutely,hourly,alerts,flags&units=si&lang={lang}".format(
            apikey=apikey, lat=lat, lon=lon, lang=lang
        )

        try:
            content = re.get(url).json()

            # raise error & darksky error msg
            try:
                content["code"]
                if content["code"] == 400:
                    raise ValueError(content["error"])
                if content["code"] == 403 or content["code"] == 401:
                    raise ValueError(
                        _(
                            'Received message "{error_msg}" from darksky, maybe your api key is invalid.'.format(
                                error_msg=content["error"]
                            )
                        )
                    )
            # if no error then its all good
            except KeyError:
                pass

        except json.decoder.JSONDecodeError:
            raise ValueError(
                _("The api didn't return a json file as expected.\nURL: " + url)
            )

        txt_content = json.dumps(content)

        # set cache duration according to settings value
        cache.set(
            key, txt_content, plugin_settings.DJANGOCMS_DARKSKY_API_SETTINGS["cache"],
        )

        return txt_content
