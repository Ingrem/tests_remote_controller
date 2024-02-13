from django.shortcuts import render
from django.core.cache import cache


def index(request):
    return render(request, "simple_web_socket.html", {"cached": ""})


def saved_text(request, cache_hash):
    a = cache.get(cache_hash)
    if not a:
        a = 'wrong link'
    return render(request, "simple_web_socket.html", {"cached": a})