from django.db import models

# Create your models here.
class LOCATIONDETAIL(models.Model):
    LOCATIONID = models.IntegerField(default=0)
    FILEID = models.IntegerField(default=0)
    LOCATION = models.CharField(max_length=200)
