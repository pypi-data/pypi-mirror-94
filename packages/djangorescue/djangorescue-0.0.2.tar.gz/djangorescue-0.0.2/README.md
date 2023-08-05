# DJANGORESCUE
* [Русский](#rus)
* [English](#eng)

## <a name="rus"></a> Описание по-русски.
Пакет DJANGORESCUE позволяет обслуживать статику (static, media) через Django (когда нет возможности использовать nginx, apache, и s3 storage), независимо от состояния параметра DEBUG. 

Да, это известно, что так делать не следует, но иногда по-другому нельзя.

### Конфигурация
**settings.py**

```python
DEBUG = False

...

MIDDLEWARE = [
    ...
    'djangorescue.middleware.StaticMediaMiddleware',
	...
]

...

STATIC_URL = '/static/'
STATIC_APP_DIR = 'static' # Имя каталога со статикой внутри каталога приложения.

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```


## <a name="eng"></a> English description.
DJANGORESCUE package allows to serve static files (static, media) through Django (when nginx, apachage and s3 storage options are not available) regardless of DEBUG setting value.

Yes, it is a known thing, that such approach is bad, however sometimes it's the only way.

### Configuration
**settings.py**

```python
DEBUG = False

...

MIDDLEWARE = [
    ...
    'djangorescue.middleware.StaticMediaMiddleware',
	...
]

...

STATIC_URL = '/static/'
STATIC_APP_DIR = 'static' # The name of the folder, that contains static files within the app folder.

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
