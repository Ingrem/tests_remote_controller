from django.shortcuts import render


def index(request):
    return render(request, "11_mock.html")