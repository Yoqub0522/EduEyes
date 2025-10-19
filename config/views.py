from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from threading import Lock
import json, os
file_lock = Lock()

def welcome(request):
    return HttpResponse("<h1>EduEyes api portali!</h1>")


@api_view(['GET'])
def get_logged_errors(request):
    log_file = getattr(settings, "UNHANDLED_ERROR_LOG_FILE", "unhandled_errors.json")


    if not log_file.exists():
        return Response({"success": True, "data": []}, status=200)

    try:
        with file_lock, log_file.open("r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return Response({"success": True, "data": []}, status=200)

            data = json.loads(content)
            if not isinstance(data, list):
                data = []

        return Response({"success": True, "data": data}, status=200)

    except json.JSONDecodeError:
        return Response(
            {"success": False, "message": "Log fayl formati noto‘g‘ri."},
            status=500
        )
    except Exception as e:
        return Response(
            {"success": False, "message": f"Xatolik yuz berdi: {str(e)}"},
            status=500
        )
