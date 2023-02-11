from django.shortcuts import render

from .models import DataFile


def index(request):
    files = DataFile.objects.all()
    return render(request, "characters/index.html", context={'files': files})
