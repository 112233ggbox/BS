from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok", "database": "reachable"})
