from django.db import models

# Create your models here
class Location(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    field_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

class Person(models.Model):
     id = models.IntegerField(default=0, primary_key=True)
     field_id = models.IntegerField(default=0)
     name = models.CharField(max_length=200)
     count = models.IntegerField(default=0)

class Organization(models.Model):
     id = models.IntegerField(default=0, primary_key=True)
     field_id = models.IntegerField(default=0)
     name = models.IntegerField(default=0)
     count = models.IntegerField(default=0)

class File(models.Model):
      id = models.IntegerField(default=0, primary_key=True)
      name = models.CharField(max_length=200)
      path = models.CharField(max_length=200)
      published_date = models.CharField(max_length=200)
