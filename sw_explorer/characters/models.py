from django.db import models


class DataFile(models.Model):
    file = models.BinaryField()
    filename = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
