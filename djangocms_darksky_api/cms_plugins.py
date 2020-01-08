from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import DarkskyApi


@plugin_pool.register_plugin
class DarkskyApiPlugin(CMSPluginBase):
    model = DarkskyApi
    name = _("Dark Sky Weather")
    render_template = "darkskyapi_small.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(DarkskyApiPlugin, self).render(context, instance, placeholder)
        return context
