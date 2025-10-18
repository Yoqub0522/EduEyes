from django.utils import translation

class LanguageFromHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.headers.get("Accept-Language", "uz")[:2]
        if lang not in ["uz", "ru", "en"]:
            lang = lang
        translation.activate('uz')
        request.LANGUAGE_CODE = 'uz'
        response = self.get_response(request)
        translation.deactivate()
        return response
