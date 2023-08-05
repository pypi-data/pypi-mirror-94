import os.path

from django.apps import apps
from django.conf import settings
from django.http import HttpRequest, HttpResponseNotFound, FileResponse


class StaticMediaMiddleware:
    def __init__(self, get_response):
        self.__get_response = get_response
        self.__static_url = getattr(settings, 'STATIC_URL', '/static/')
        self.__static_app_dir = getattr(settings, 'STATIC_APP_DIR', 'static')
        self.__media_url = getattr(settings, 'MEDIA_URL', '/media/')
        self.__media_root = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))

    def __call__(self, request: HttpRequest):
        if request.path.startswith(self.__static_url):
            return self.__process_static_request(request)

        if request.path.startswith(self.__media_url):
            return self.__process_media_request(request)

        return self.__get_response(request)

    def __process_static_request(self, request: HttpRequest):
        requested_file = request.path[len(self.__static_url):].replace('/', os.path.sep)

        if '..' in requested_file:
            return HttpResponseNotFound()

        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_path = app_config.path
            requested_file_path = os.path.join(app_path, self.__static_app_dir, requested_file)

            if os.path.isfile(requested_file_path):
                return FileResponse(open(requested_file_path, 'rb'))

        return HttpResponseNotFound()

    def __process_media_request(self, request: HttpRequest):
        requested_file = request.path[len(self.__media_url):].replace('/', os.path.sep)

        if '..' in requested_file:
            return HttpResponseNotFound()

        requested_file_path = os.path.join(self.__media_root, requested_file)
        if not os.path.isfile(requested_file_path):
            return HttpResponseNotFound()

        return FileResponse(open(requested_file_path, 'rb'))
