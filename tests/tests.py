import pytest
from djangocms_darksky_api import cms_plugins


@pytest.fixture()
def give_me_a_plugin_instance_please():
    return cms_plugins.DarkskyApiPlugin


class Instance:
    template = "my_template_name"


#       ████████╗███████╗███████╗████████╗███████╗
#       ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
#          ██║   █████╗  ███████╗   ██║   ███████╗
#          ██║   ██╔══╝  ╚════██║   ██║   ╚════██║
#          ██║   ███████╗███████║   ██║   ███████║
#          ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝


def test_get_render_template(give_me_a_plugin_instance_please):
    instance = Instance

    my_render_template = give_me_a_plugin_instance_please.get_render_template(
        None, None, instance, None
    )

    assert my_render_template == "darkskyapi_my_template_name.html"
