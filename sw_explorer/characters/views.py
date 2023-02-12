import csv
from datetime import datetime
import io

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import DataFile
from .utils import SWAPIConnector


def index(request):
    files = DataFile.objects.all()
    return render(request, "characters/index.html", context={'files': files})


def fetch(request):
    connector = SWAPIConnector()
    table = connector.get_as_table('people')
    # Saving binary csv in database
    if table:
        str_buffer = io.StringIO()
        writer = csv.writer(str_buffer)
        writer.writerows(table)
        bytes_buffer = io.BytesIO(str_buffer.getvalue().encode('utf-8'))
        DataFile.objects.create(
            file=bytes_buffer.read(),
            filename=f'{datetime.now()}.csv',
        )
    return HttpResponseRedirect(reverse("index"))
