![djangocms-darksky-api](https://user-images.githubusercontent.com/45763865/72326603-c0338500-36af-11ea-9c74-e3f07b4a79bb.png)

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

 * Small template:
 ![small template raw](https://user-images.githubusercontent.com/45763865/72332449-5b315c80-36ba-11ea-915e-5b374f402f39.png)
 * Medium template:
 ![medium template raw](https://user-images.githubusercontent.com/45763865/72332761-e6aaed80-36ba-11ea-9edc-44d7d4e492eb.png)

### Examples of rendered views

 * Small template:
 ![small template rendered](https://user-images.githubusercontent.com/45763865/72326793-2ae4c080-36b0-11ea-9e51-614c845b382d.png)
 * Medium template:
 ![medium template rendered](https://user-images.githubusercontent.com/45763865/72326898-5d8eb900-36b0-11ea-90b5-9efa40fb3caf.png)
