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

#############
#  apps.py  #
#############
def test_apps_py():
    from djangocms_darksky_api import apps

    instance = apps.DjangocmsDarkskyApiConfig

    assert instance.name == "djangocms_darksky_api"


####################
#  cms_plugins.py  #
####################

# everything should be okay with this one
def test_get_render_template_okay(give_me_a_plugin_instance_please):
    instance = Instance

    my_render_template = give_me_a_plugin_instance_please.get_render_template(
        None, None, instance, None
    )
    assert my_render_template == "darkskyapi_my_template_name.html"


# TypeError
def test_get_render_template_not_okay(give_me_a_plugin_instance_please):
    instance = Instance
    instance.template = None

    with pytest.raises(TypeError):
        my_render_template = give_me_a_plugin_instance_please.get_render_template(
            None, None, instance, None
        )


# 1 hour of cache by default
def test_get_cache_expiration_from_instance(give_me_a_plugin_instance_please):
    cache = give_me_a_plugin_instance_please.get_cache_expiration(
        None, None, None, None
    )
    assert cache == 3600


# mock requests to ensure json are good
def test_update_data(give_me_a_plugin_instance_please, monkeypatch):
    import requests

    class MockRequests:
        @staticmethod
        def json():
            return {"key": "answer"}

    def mock_get(*args, **kwargs):
        return MockRequests()

    monkeypatch.setattr(requests, "get", mock_get)

    instance = give_me_a_plugin_instance_please()
    txt_content = instance.update_data("key", "lat", "lon", "lang")

    assert txt_content == '{"key": "answer"}'


# mock requests to ensure error handling when content contains "code" 400
# thx https://docs.pytest.org/en/latest/monkeypatch.html
def test_update_data_error_code_400(give_me_a_plugin_instance_please, monkeypatch):
    import requests

    class MockRequests:
        @staticmethod
        def json():
            return {"code": 400, "error": "error msg"}

    def mock_get(*args, **kwargs):
        return MockRequests()

    monkeypatch.setattr(requests, "get", mock_get)

    instance = give_me_a_plugin_instance_please()

    with pytest.raises(ValueError):
        txt_content = instance.update_data("key", "lat", "lon", "lang")
        assert txt_content["error"] == "error msg"


# mock requests to ensure error handling when content contains "code" 403
def test_update_data_error_code_403(give_me_a_plugin_instance_please, monkeypatch):
    import requests

    class MockRequests:
        @staticmethod
        def json():
            return {
                "code": 403,
                "error": "hey it's darksky we don't recognize your api key",
            }

    def mock_get(*args, **kwargs):
        return MockRequests()

    monkeypatch.setattr(requests, "get", mock_get)

    instance = give_me_a_plugin_instance_please()

    with pytest.raises(
        ValueError,
        match=r"Received message \"hey it's darksky we don't recognize your api key\" from darksky, maybe your api key is invalid.",
    ):
        txt_content = instance.update_data("key", "lat", "lon", "lang")


# mock requests to ensure JSONDecodeError handling
def test_update_data_jsondecodeerror(give_me_a_plugin_instance_please, monkeypatch):
    import requests
    import json.decoder

    class MockRequests:
        @staticmethod
        def json():
            raise json.decoder.JSONDecodeError("", "", 0)

    def mock_get(*args, **kwargs):
        return MockRequests()

    monkeypatch.setattr(requests, "get", mock_get)

    instance = give_me_a_plugin_instance_please()

    with pytest.raises(
        ValueError, match=r"The api didn't return a json file as expected.*"
    ):
        txt_content = instance.update_data("key", "lat", "lon", "lang")


# mock requests to ensure ConnectionError handling
def test_update_data_connexionerror(give_me_a_plugin_instance_please, monkeypatch):
    import requests

    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, "get", mock_get)

    instance = give_me_a_plugin_instance_please()

    txt_content = instance.update_data("key", "lat", "lon", "lang")
    assert txt_content == '{"error": "Data is currently unavailable."}'


# mock function render
def test_render_function(give_me_a_plugin_instance_please, mocker, monkeypatch):
    # updating this function because we only need some json and do not care about requests and other calls
    mock_update = mocker.Mock(
        return_value='{"meteo": "it\'s raining developers hallelujah"}'
    )
    cms_plugins.DarkskyApiPlugin.update_data = mock_update

    # faking a dict-like object
    class MockedInstance:
        def __init__(self):
            self.longitude = "lon"
            self.latitude = "lat"

        def __getitem__(self, key):
            return getattr(self, key)

        def __setitem__(self, key, value):
            return setattr(self, key, value)

    instance = give_me_a_plugin_instance_please()
    context = MockedInstance()  # we need a dict-like context

    # render() returns "context", so we need to check this too
    returned_context = instance.render(context, MockedInstance(), {})

    # check context (arg & returned)
    assert context["meteo"] == returned_context["meteo"]
    assert returned_context["meteo"] == {"meteo": "it's raining developers hallelujah"}
    # ensure that update_data only was called once, because why not
    mock_update.assert_called_once()


#################
#  settings.py  #
#################

# 1 hour of cache by default
def test_get_settings_cache_expiration():
    from djangocms_darksky_api.conf import settings

    assert settings.DJANGOCMS_DARKSKY_API_SETTINGS["cache"] == 3600


# see tests_settings.py
def test_get_settings_api_key():
    from djangocms_darksky_api.conf import settings

    assert settings.DJANGOCMS_DARKSKY_API_SETTINGS["api_key"] == "key"


# settings.py:14 - goal is to remove django settings DJANGOCMS_DARKSKY_API_SETTINGS
# but it's not working
# I even tried https://pytest-django.readthedocs.io/en/latest/helpers.html#id4
#
#
# def test_raise_exception_if_settings_are_not_set():
#     import tests_settings

#     tests_settings.DJANGOCMS_DARKSKY_API_SETTINGS = None

#     from django.conf import settings

#     settings.DJANGOCMS_DARKSKY_API_SETTINGS = None

#     from djangocms_darksky_api.conf import settings as s

#     print(s.project_settings)
