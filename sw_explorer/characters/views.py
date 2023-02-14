import csv
from datetime import datetime
import io
import petl as etl

from django.http import HttpResponseRedirect, FileResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import DataFile
from .utils import SWAPIConnector, format_people_table, get_buffer


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
    buffer, filename = get_buffer(file_id)
    if buffer is None:
        return HttpResponseRedirect(reverse("index"))
    response = FileResponse(buffer, as_attachment=True, filename=filename)
    return response


def file_rows(request):
    # Collecting input params
    file_id = int(request.GET.get("file_id"))
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    # Reading file content
    buffer, filename = get_buffer(file_id)
    if buffer is None:
        return JsonResponse({"rows": []})
    reader = csv.reader(io.TextIOWrapper(buffer, encoding="utf-8"))
    rows = [row for row in reader]
    # Returning sliced rows
    return JsonResponse({"rows": rows[start:end + 1]})


def file_content(request, file_id):
    try:
        data_file = DataFile.objects.get(id=file_id)
    except DataFile.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "characters/file_content.html", context={'file_id': file_id, 'filename': data_file.filename})


def value_count(request, file_id):
    try:
        data_file = DataFile.objects.get(id=file_id)
    except DataFile.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "characters/value_count.html", context={'file_id': file_id, 'filename': data_file.filename})
