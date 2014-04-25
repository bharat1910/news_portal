from django.db import models, connection
# create your models here
class PersonLookup(models.Manager):
    def uniquePerson(self):
        cursor = connection.cursor()
        cursor.execute("select id,name from news_explorer_person")
        rows = cursor.fetchall()
        return rows

class LocationLookup(models.Manager):
    def uniqueLocation(self):
        cursor = connection.cursor()
        cursor.execute("select id,name from news_explorer_location")
        rows = cursor.fetchall()
        return rows

class OrganizationLookup(models.Manager):
    def uniqueOrganization(self):
        cursor = connection.cursor()
        cursor.execute("select id,name from news_explorer_organization")
        rows = cursor.fetchall()
        return rows

class PersonManager(models.Manager):
    def articlesbyperson(self, personid, pid):
        cursor = connection.cursor()
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebyperson where person_id = %s) order by clicks desc;", [personid])
        elif pid == '1':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebyperson where person_id = %s) order by clicks;", [personid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebyperson where person_id = %s) order by published_date desc;", [personid])

        rows = cursor.fetchall()
        return rows

class LocationManager(models.Manager):
    def articlesbylocation(self, locationid, pid):
        cursor = connection.cursor()
        print pid
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where a.file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebylocation where location_id = %s) order by a.clicks desc;", [locationid])
        elif pid == '1':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where a.file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebylocation where location_id = %s) order by a.clicks asc;", [locationid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                   " (select article_id from news_explorer_articlebylocation where location_id = %s) order by published_date desc;", [locationid])
        rows = cursor.fetchall()
        return rows

class OrganizationManager(models.Manager):
    def articlebyorganization(self,organizationid,pid):
        cursor = connection.cursor()
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebyorganization where organization_id = %s) order by clicks desc;", [organizationid])
        elif pid == '1':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select article_id from news_explorer_articlebyorganization where organization_id = %s) order by clicks;", [organizationid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                   "(select article_id from news_explorer_articlebyorganization where organization_id = %s) order by published_date desc;", [organizationid])
        rows = cursor.fetchall()
        return rows

class PersonLocationManager(models.Manager):
    def articlesbypersonlocation(self,personid,locationid,pid):
        cursor = connection.cursor()
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l where person_id = %s and location_id = %s and p.article_id = l.article_id) order by clicks desc;", [personid, locationid])
        elif pid == '1':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l where person_id = %s and location_id = %s and p.article_id = l.article_id) order by clicks;", [personid, locationid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                   "(select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l where person_id = %s and location_id = %s and p.article_id = l.article_id) order by published_date desc;", [personid, locationid])
        rows = cursor.fetchall()
        return rows

class PersonOrganizationManager(models.Manager):
    def articlesbypersonorganization(self,personid,organizationid,pid):
        cursor = connection.cursor()
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebyperson p, news_explorer_articlebyorganization o where person_id = %s and organization_id = %s and p.article_id = o.article_id) order by clicks desc;", [personid,organizationid])
        elif pid == '1':
                        cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebyperson p, news_explorer_articlebyorganization o where person_id = %s and organization_id = %s and p.article_id = o.article_id) order by clicks;", [personid,organizationid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                   "(select p.article_id from news_explorer_articlebyperson p, news_explorer_articlebyorganization o where person_id = %s and organization_id = %s and p.article_id = o.article_id) order by published_date desc;", [personid,organizationid])
        rows = cursor.fetchall()
        return rows

class LocationOrganizationManager(models.Manager):
    def articlesbylocationorganization(self, locationid, organizationid,pid):
        cursor = connection.cursor()
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebylocation p,news_explorer_articlebyorganization o where location_id = %s and organization_id = %s and p.article_id = o.article_id) order by clicks desc;", [locationid,organizationid])
        elif pid == '1':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebylocation p,news_explorer_articlebyorganization o where location_id = %s and organization_id = %s and p.article_id = o.article_id) order by clicks;", [locationid,organizationid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                   "(select p.article_id from news_explorer_articlebylocation p,news_explorer_articlebyorganization o where location_id = %s and organization_id = %s and p.article_id = o.article_id) order by published_date desc;", [locationid, organizationid])
        rows = cursor.fetchall()
        return rows

class PersonLocationOrganizationManager(models.Manager):
    def articlesbypersonlocationorganization(self,personid,locationid,organizationid,pid):
        cursor = connection.cursor()
        if pid == '2':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l, news_explorer_articlebyorganization o where person_id = %s and location_id = %s and organization_id = %s and p.article_id = l.article_id = o.article_id) order by clicks desc;", [personid,locationid,organizationid])
        elif pid == '1':
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                           " (select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l, news_explorer_articlebyorganization o where person_id = %s and location_id = %s and organization_id = %s and p.article_id = l.article_id = o.article_id) order by clicks;", [personid,locationid,organizationid])
        else:
            cursor.execute("select a.id, a.headline, a.clicks, f.published_date from news_explorer_article a, news_explorer_file f where file_id = f.id and a.id in"
                   "(select p.article_id from news_explorer_articlebyperson p,news_explorer_articlebylocation l, news_explorer_articlebyorganization o where person_id = %s and location_id = %s and organization_id = %s and p.article_id = l.article_id = o.article_id) order by published_date desc;", [personid, locationid, organizationid])
        rows = cursor.fetchall()
        return rows

class ParentLocationManager(models.Manager):
    def countbyparentlocation(self):
	cursor = connection.cursor()
	cursor.execute("select l.parentlocation_id, p.name, count(a.article_id) from news_explorer_parentlocation p, news_explorer_location l, news_explorer_articlebylocation a where p.id = l.parentlocation_id and l.id = a.location_id group by l.parentlocation_id;")
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
    category = models.CharField(max_length=200)
    objects = PersonLocationOrganizationManager()

class ParentLocation(models.Model):
    name = models.CharField(max_length=200)

class Location(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    parentlocation_id = models.IntegerField(default=0)
    objects = LocationLookup()

class Person(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    objects = PersonLookup()

class Organization(models.Model):
    #article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    objects = OrganizationLookup()

class ArticlebyLocation(models.Model):
    location = models.ForeignKey(Location)
    article = models.ForeignKey(Article)
    count = models.IntegerField(default=0)
    obj = ParentLocationManager()
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
