import csv
from datetime import datetime
import io

from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.urls import reverse

from .models import DataFile
from .utils import SWAPIConnector, format_people_table


def index(request):
    files = DataFile.objects.all().order_by('-date_created')
    return render(request, "characters/index.html", context={'files': files})


def fetch(request):
    connector = SWAPIConnector()
    table = connector.get_as_table('people')
    table = format_people_table(table, connector)
    if table:
        str_buffer = io.StringIO()
        writer = csv.writer(str_buffer)
        writer.writerows(table)
        bytes_buffer = io.BytesIO(str_buffer.getvalue().encode('utf-8'))
        DataFile.objects.create(
            file=bytes_buffer.read(),
            filename=f'{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv',
        )
    return HttpResponseRedirect(reverse("index"))


def download_file(request, file_id):
    try:
        data_file = DataFile.objects.get(id=file_id)
    except DataFile.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    buffer = io.BytesIO(data_file.file)
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename=data_file.filename)
    return response
