from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fetch/", views.fetch, name="fetch"),
    path("download_file/<int:file_id>/", views.download_file, name="download_file"),
    path("file_content/<int:file_id>/", views.file_content, name="file_content"),
    path("value_count/<int:file_id>", views.value_count, name="value_count"),
    path("file_rows/", views.file_rows, name="file_rows"),
    path("value_count_table/", views.value_count_table, name="value_count_table")
]
