from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson as Json
from django.conf import settings
from django.utils.importlib import import_module
from news_explorer.models import File, Person, Organization, Location, Article, ArticlebyLocation, ArticlebyPerson\
    ,ArticlebyOrganization, PersonManager,OrganizationManager,LocationManager

def index(request):
    context = {}
    return render(request, 'news_explorer/index.html', context)

def news_articles_by_selection(request):
    context = {}
    return render(request, 'news_explorer/news_articles_by_selection.html', context)

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

'''def initiate(request,location,person,organization):
    if request.method == 'GET':
        if request.GET["location"]:
            L = Location.objects.values('name').distinct()
            response = HttpResponse(Json.dum
            ps(str(L), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        if request.GET["person"]:
            P = Person.objects.values('name').distinct()
            response = HttpResponse(Json.dumps(str(P), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        if request.GET["organization"]:
            O = Organization.objects.values('name').distinct()
            response = HttpResponse(Json.dumps(str(O), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response'''

def initiate_chosen(request, reqtype):
    if request.method == 'GET':
        if reqtype == "location":
            L = Location.objects.values('id','name')
            response = HttpResponse(L, content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)
        elif reqtype == "organization":
            L = Organization.objects.values('id','name')
            response = HttpResponse(L, content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)
        elif reqtype == "person":
            L = Person.objects.values('id', 'name')
            response = HttpResponse(L, content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

def getJson(request):
    if request.method == 'GET':
        if request.GET["location_id"]:
            location = request.GET.get('location_id', '')
            L = ArticlebyLocation.object.articlesbylocation(location)
            response = HttpResponse(L, content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

        elif request.GET["person"]:
            P = ArticlebyPerson.objects.articlesbyperson(person).values()
            response = HttpResponse(P, content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

        elif request.GET["organization"]:
            O = ArticlebyOrganization.objects.articlebyorganization(organization).values()
            response = HttpResponse(O, content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

    if request.GET["location"] and request.GET["person"] and request.GET["organization"]:
        f = Article.objects.articlesbypersonlocationorganization(person, location, organization).values()
        response = HttpResponse(f, content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)

    elif request.GET["person"] and request.GET["location"]:
        PL = ArticlebyPerson.objects.articlesbypersonlocation(person,location).values()
        response = HttpResponse(PL, content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)

    elif request.GET["organization"] and request.GET["location"]:
        OL = ArticlebyLocation.objects.articlesbylocationorganization(location,organization).values()
        response = HttpResponse(OL, content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)

    elif request.GET["organization"] and request.GET["person"]:
        OP = ArticlebyOrganization.objects.articlesbypersonorganization(person,organization)
        response = HttpResponse(OP, content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)
    else:
        A = Article.objects.values('id', 'headline')
        response = HttpResponse(A, content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)

def click_article(request):
	if request.method == 'GET':
		articleid = request.GET['articleid']
        	article = Article.objects.get(id = articleid)
        	if article:
	                article.clicks = article.clicks + 1
	        	article.save()
			return HttpResponse(article.clicks)
