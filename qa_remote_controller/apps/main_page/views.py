from django.shortcuts import render


def index(request):
    return render(request, "main_page.html")


def index_admin(request):
    return render(request, "main_page_admin.html")
