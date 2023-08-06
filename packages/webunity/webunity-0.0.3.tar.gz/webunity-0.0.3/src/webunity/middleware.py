from django.conf import settings


class ConfigMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, 'version', settings.VERSION)
        setattr(request, 'version_webunity', settings.VERSION_WEBUNITY)
        response = self.get_response(request)
        return response
