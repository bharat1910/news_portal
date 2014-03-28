from django.db import models

# create your models here

class Location(models.model):
    id = models.integerfield(default=0)
    article_id = models.integerfield(default=0)
    name = models.charfield(max_length=200)
    count = models.integerfield(default=0)

class Person(models.model):
     id = models.integerfield(default=0)
     article_id = models.integerfield(default=0)
     name = models.charfield(max_length=200)
     count = models.integerfield(default=0)

class Organization(models.model):
     id = models.integerfield(default=0)
     article_id = models.integerfield(default=0)
     name = models.integerfield(default=0)
     count = models.integerfield(default=0)

class File(models.model):
      id = models.integerfield(default=0)
      name = models.charfield(max_length=200)
      path_file = models.charfield(max_length=200)
      published_date= models.charfield(max_length=200)
      source= models.charfield(max_length=200)
      published_location = models.charfield(max_length=20)

class Article(models.model):
      id=models.integerfield(default=0)
      file_id=models.integerfield(default=0)
      headline=models.charfield(max_length=300)
      content=models.textfield(max_length=10000,widget=forms.textarea)
      number=models.integerfield(default=0)
