import time
from django.conf import settings
from django.http import HttpResponse
from messages.get_message import get_message


class BlockIPMiddleware:
    requests = {}

    def __init__(self, get_response):
        self.get_response = get_response

        config = getattr(settings, "BLOCK_IP_CONFIG", {})
        self.TIME_WINDOW = config.get("TIME_WINDOW", 60)
        self.DEFAULT_MAX_REQUESTS = config.get("DEFAULT_MAX_REQUESTS", 100)
        self.SPECIAL_URLS = config.get("SPECIAL_URLS", {})

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if not ip:
            return HttpResponse("IP manzilingiz aniqlanmadi.", status=400)

        path = request.path
        max_requests = self.SPECIAL_URLS.get(path, self.DEFAULT_MAX_REQUESTS)

        now = time.time()
        request_times = self.requests.get(ip, [])

        request_times = [t for t in request_times if now - t <= self.TIME_WINDOW]

        if len(request_times) >= max_requests:
            return HttpResponse(
                get_message("429", str(self.TIME_WINDOW)), status=429
            )

        request_times.append(now)
        self.requests[ip] = request_times

        return self.get_response(request)
