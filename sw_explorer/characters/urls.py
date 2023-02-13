from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fetch/", views.fetch, name="fetch"),
    path("download_file/<int:file_id>/", views.download_file, name="download_file")
]
