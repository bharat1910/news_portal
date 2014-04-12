from django.db import models, connection
# create your models here
class PersonManager(models.Manager):
    def articlesbyperson(self, personid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in "
                       "(select article_id from news_explorer_articlebyperson where person_id = %s) order by clicks", [personid])
        rows = cursor.fetchall()
        return rows

class LocationManager(models.Manager):
    def articlesbylocation(self, locationid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in "
                       "(select article_id from news_explorer_articlebylocation where location_id = %s) order by clicks", [locationid])
        rows = cursor.fetchall()
        return rows

class OrganizationManager(models.Manager):
    def articlebyorganization(self,organizationid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in "
                       "(select article_id from news_explorer_articlebyorganization where organization_id = %s) order by clicks", [organizationid])
        rows = cursor.fetchall()
        return rows

class PersonLocationManager(models.Manager):
    def articlesbypersonlocation(self,personid,locationid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in (select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l where person_id = %s and location_id = %s and p.article_id = l.article_id) order by clicks", [personid, locationid])
        rows = cursor.fetchall()
        return rows

class PersonOrganizationManager(models.Manager):
    def articlesbypersonorganization(self,personid,organizationid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in (select p.article_id from news_explorer_articlebyperson p, news_explorer_articlebyorganization o where person_id = %s and organization_id = %s and p.article_id = o.article_id) order by clicks", [personid, organizationid])
        rows = cursor.fetchall()
        return rows

class LocationOrganizationManager(models.Manager):
    def articlesbylocationorganization(self, locationid, organizationid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in (select p.article_id from news_explorer_articlebylocation p,news_explorer_articlebyorganization o where location_id = %s and organization_id = %s and p.article_id = o.article_id) order by clicks", [locationid, organizationid])
        rows = cursor.fetchall()
        return rows

class PersonLocationOrganizationManager(models.Manager):
    def articlesbypersonlocationorganization(self,personid,locationid,organizationid):
        cursor = connection.cursor()
        cursor.execute("select id,headline from news_explorer_article where id in (select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l, news_explorer_articlebyorganization o where person_id = %s and location_id = %s and organization_id = %s and p.article_id = l.article_id = o.article_id) order by clicks", [personid, locationid, organizationid])
        rows = cursor.fetchall()
        return rows

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
      clicks = models.IntegerField(default=0)
      objects = PersonLocationOrganizationManager()

class Location(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    
class Person(models.Model):
     #article = models.ForeignKey(Article)
     name = models.CharField(max_length=200)

class Organization(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)

class ArticlebyLocation(models.Model):
    location = models.ForeignKey(Location)
    article = models.ForeignKey(Article)
    count = models.IntegerField(default=0)
    object = LocationManager()
    objects = LocationOrganizationManager()

class ArticlebyPerson(models.Model):
    person = models.ForeignKey(Person)
    article = models.ForeignKey(Article)
    count = models.IntegerField(default=0)
    object = PersonManager()
    objects = PersonLocationManager()

class ArticlebyOrganization(models.Model):
    organization = models.ForeignKey(Organization)
    article = models.ForeignKey(Article)
    count = models.IntegerField(default=0)
    object = OrganizationManager()
    objects = PersonOrganizationManager()
