import time
import json
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from django.http import Http404, HttpResponseForbidden
from .utils import log


class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        user = request.user.username if request.user.is_authenticated else "Anonim"
        ip = request.META.get("REMOTE_ADDR", "Nieznany IP")
        user_agent = request.META.get("HTTP_USER_AGENT", "Brak user-agenta")
        method = request.method
        path = request.path
        duration = round((time.time() - getattr(request, "_start_time", time.time())) * 1000, 2)

        # Dane GET / POST (ograniczamy długość i ukrywamy hasła)
        params = dict(request.GET or request.POST)
        sanitized_data = {
            k: ("[UKRYTO]" if "password" in k.lower() else str(v)[:100])
            for k, v in params.items()
        }

        # Loguj odpowiedź
        log(
            f"Odpowiedź {response.status_code} | {method} {path} | Użytkownik: {user} | IP: {ip} | Czas: {duration}ms | Dane: {sanitized_data}",
            lvl="response"
        )

        # Logowanie błędów 403/404/500
        if response.status_code in [403, 404, 500]:
            log(
                f"Błąd {response.status_code} | {method} {path} | Użytkownik: {user} | IP: {ip}",
                lvl="error"
            )

        return response

    def process_exception(self, request, exception):
        user = request.user.username if request.user.is_authenticated else "Anonim"
        ip = request.META.get("REMOTE_ADDR", "Nieznany IP")
        path = request.path
        method = request.method

        if isinstance(exception, Http404):
            status = 404
        elif isinstance(exception, PermissionError) or isinstance(exception, HttpResponseForbidden):
            status = 403
        else:
            status = 500

        log(
            f"Wyjątek {status} | {method} {path} | {type(exception).__name__}: {exception} | Użytkownik: {user} | IP: {ip}",
            lvl="error"
        )
        return None
