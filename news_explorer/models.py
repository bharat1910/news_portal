from django.db import models

# create your models here

class Location(models.Model):
    id = models.IntegerField(primary_key=True,default=0)
    article_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

class Person(models.Model):
     id = models.IntegerField(primary_key=True,default=0)
     article_id = models.IntegerField(default=0)
     name = models.CharField(max_length=200)
     count = models.IntegerField(default=0)

class Organization(models.Model):
     id = models.IntegerField(primary_key=True,default=0)
     article_id = models.Integerfield(default=0)
     name = models.IntegerField(default=0)
     count = models.IntegerField(default=0)

class File(models.Model):
      id = models.IntegerField(primary_key=True, default=0)
      name = models.CharField(max_length=200)
      path_file = models.CharField(max_length=200)
      published_date= models.CharField(max_length=200)
      source= models.CharField(max_length=200)
      published_location = models.CharField(max_length=20)

class Article(models.Model):
      id = models.IntegerField(primary_key=True, default=0)
      file_id = models.IntegerField(default=0)
      headline = models.CharField(max_length=300)
      content = models.TextField(max_length=10000,widget=forms.textarea)
      number = models.IntegerField(default=0)
