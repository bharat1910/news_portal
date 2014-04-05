from django.db import models

# create your models here
class File(models.Model):
    name = models.CharField(max_length=200)
    path_file = models.CharField(max_length=200)
    published_date= models.CharField(max_length=200)
    source= models.CharField(max_length=200)
    published_location = models.CharField(max_length=20)

class Article(models.Model):
      file = models.ForeignKey(File)
      headline = models.CharField(max_length=300)
      content = models.CharField(max_length=10000)
      number = models.IntegerField(default=0)

class Location(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

class Person(models.Model):
     #article = models.ForeignKey(Article)
     name = models.CharField(max_length=200)
     count = models.IntegerField(default=0)

class Organization(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

class ArticlebyLocation(models.Model):
    location = models.ForeignKey(Location)
    article = models.ForeignKey(Article)

class ArticlebyPerson(models.Model):
    person = models.ForeignKey(Person)
    article = models.ForeignKey(Article)

class ArticlebyOrganization(models.Model):
    organization = models.ForeignKey(Organization)
    article = models.ForeignKey(Article)




