from django.db import models

# Create your models here

class LOCATION(models.Model):
    LOCATIONID = models.IntegerField(default=0)
    FILEID = models.IntegerField(default=0)
    LOCATIONNAME = models.CharField(max_length=200)
    LOCATIONCOUNT = models.IntegerField(default=0)

class PERSON(models.Model):
     PERSONID = models.IntegerField(default=0)
     FILEID = models.IntegerField(default=0)
     PERSONNAME = models.CharField(max_length=200)
     PERSONCOUNT = models.IntegerField(default=0)

class ORGANIZATION(models.Model):
     ORGANIZATIONID = models.IntegerField(default=0)
     FILEID = models.IntegerField(default=0)
     ORGANIZATIONNAME = models.IntegerField(default=0)
     ORGANIZATIONCOUNT = models.IntegerField(default=0)

class FILE(models.Model):
      FILEID = models.IntegerField(default=0)
      FILENAME = models.CharField(max_length=200)
      PATHFILE = models.CharField(max_length=200)
      PUBLISHEDDATE= models.CharField(max_length=200)
