from django.db import models

# Create your models here.
class Release(models.Model):
    version = models.CharField(max_length=5)
    changes = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.version
    