import os
from django.db import models
from datetime import datetime

def upload_to_unique(instance, filename):
    ext = filename.split('.')[-1]  # pobierz rozszerzenie
    new_filename = f"{datetime.now()}.{ext}"  # np. 7f9d0c9e-6d6e-42b4-939e-a7f957ebf5e9.jpg
    return os.path.join("uploads", new_filename)  # zapisze się w media/uploads/

class Dokument(models.Model):
    plik = models.FileField(upload_to=upload_to_unique)
