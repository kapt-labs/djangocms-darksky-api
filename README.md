![djangocms-darksky-api](https://user-images.githubusercontent.com/45763865/72344245-0c42f180-36d1-11ea-9240-d9be9c81ddfb.png)

The weather plugin that links djangocms and [Dark Sky](https://darksky.net/).

## Installation


 1. Install module using pipenv:
 ```
 pipenv install -e git+https://github.com/kapt-labs/djangocms-darksky-api.git#egg=djangocms-darksky-api
 ```
 * *Or pip:*
 ```
 pip install git+https://github.com/kapt-labs/djangocms-darksky-api.git
 ```
 2. Add it to your installed apps:
 ```
     "djangocms_darksky_api",
 ```
 3. Apply migrations
 ```
 py manage.py migrate djangocms_darksky_api
 ```
 4. Include your api key in your settings (get one on [darksky](https://darksky.net/dev) website)
 ```python
 DJANGOCMS_DARKSKY_API_SETTINGS = {"api_key": "your key here"}
 ```
 * *Or load it using an environment var:*
 ```python
 import os
 DJANGOCMS_DARKSKY_API_SETTINGS = {"api_key": os.getenv("DARKSKY_API_KEY", None)}
 ```
 5. Include weather plugin on your pages using djangocms
 ![Add dark sky api plugin](https://user-images.githubusercontent.com/45763865/72329144-83b65800-36b4-11ea-832a-f87c32ba95e1.png)
 6. ![That's all folks!](https://i.imgur.com/o2Tcd2E.png)

## Examples

### Raw results

#### Small template (view & src)

![small template raw](https://user-images.githubusercontent.com/45763865/72333114-92ecd400-36bb-11ea-86ff-60bbdf21db9c.png)

#### Medium template (view & src)

![medium template raw](https://user-images.githubusercontent.com/45763865/72333144-a13af000-36bb-11ea-9890-27eb37636145.png)

### Examples of rendered views

#### Small template

![small template rendered](https://user-images.githubusercontent.com/45763865/72326793-2ae4c080-36b0-11ea-9e51-614c845b382d.png)

#### Medium template:

![medium template rendered](https://user-images.githubusercontent.com/45763865/72326898-5d8eb900-36b0-11ea-90b5-9efa40fb3caf.png)

## Miscellaneous

### Css

Css classes for the icons (e.g. `<div class="darksky-icon darksky-rain"></div>`) are of the form `darksky-icon darksky-[name]`.

`[name]` can be any of the following values (see [darksky doc](https://darksky.net/dev/docs#data-point)):
 * clear-day
 * clear-night
 * rain
 * snow
 * sleet
 * wind
 * fog
 * cloudy
 * partly-cloudy-day
 * partly-cloudy-night

----

### Units

All values are returned using the International System (°C, km/h, ...) and are hard-coded in templates files.

----

### Language

The language is searched using `django.utils.translation.get_language()` & `django.conf.LANGUAGE_CODE`.

Languages supported by the Dark Sky api can be found on [their documentation](https://darksky.net/dev/docs#request-parameters).

### Cache

#### Plugin

The plugin is cached (with the same duration as the json content).

#### Json

The values are cached for one hour (which avoids hundreds of thousands of queries per day on the darksky api site).

If you want to change the cache duration, add a `cache` entry in your `DJANGOCMS_DARKSKY_API_SETTINGS` dict, in your settings.py:

```python
DJANGOCMS_DARKSKY_API_SETTINGS = {
    "api_key": "mysuperapikey",
    "cache": 60 * 60, # one hour
}
```

*Or load it using an environment var:*
```python
import os
DJANGOCMS_DARKSKY_API_SETTINGS = {
    "api_key": os.getenv("DARKSKY_API_KEY", None),
    "cache": os.getenv("DARKSKY_CACHE_DURATION", 60 * 60), # return content of DARKSKY_CACHE_DURATION if it exists, or one hour if it doesn't
}
```

As stated in [Django docs](https://docs.djangoproject.com/en/3.0/topics/cache/#basic-usage); "*[The timeout is] the number of seconds the value should be stored in the cache. Passing in None for timeout will cache the value forever. A timeout of 0 won’t cache the value.*"
