![djangocms-darksky-api](https://user-images.githubusercontent.com/45763865/72337621-2bd31d80-36c3-11ea-9508-80885453639e.png)

The weather plugin that links djangocms and [Dark Sky](https://darksky.net/).

## Installation


 1. Install module:
 ```
 pipenv install -e git+https://github.com/kapt-labs/djangocms-darksky-api.git#egg=djangocms-darksky-api
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
 ```
 DJANGOCMS_DARKSKY_API_SETTINGS = {"api_key": "your key here"}
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

Css classes for the icons (e.g. `<div class="darksky-icon-rain"></div>`) are of the form `darksky-icon-[name]`.

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

The language is searched using `django.utils.translation.get_language()`. If the result is `None` (language not set), the custom summaries are in English.

Languages supported by the Dark Sky api can be found on [their documentation](https://darksky.net/dev/docs#request-parameters).
