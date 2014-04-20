from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson as Json
from django.conf import settings
from django.utils.importlib import import_module
from django.db.models import Count
from news_explorer.models import File, Person, Organization, Location, Article, ArticlebyLocation, ArticlebyPerson \
    , ArticlebyOrganization, PersonManager,OrganizationManager,LocationManager

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

def initiate_chosen(request, reqtype):
    if request.method == 'GET':
        if reqtype == "location":
            L = Location.objects.uniqueLocation()
            print L
            response = HttpResponse(Json.dumps(convertSelectAttributesToMap(L), default=jdefault,indent=4), content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

        elif reqtype == "organization":
            L = Organization.objects.uniqueOrganization()
            response = HttpResponse(Json.dumps(convertSelectAttributesToMap(L), default=jdefault,indent=4), content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

        elif reqtype == "person":
            L = Person.objects.uniquePerson()
            response = HttpResponse(Json.dumps(convertSelectAttributesToMap(L), default=jdefault,indent=4), content_type="application/json", mimetype="application/json").content
            return HttpResponse(response)

def getJson(request):
    try:
        if request.method == 'GET':
            if 'location_id' in request.GET and 'person_id' in request.GET and 'organization_id'in request.GET and 'pid' in request.GET:
                person = request.GET.get('person_id', '')
                location = request.GET.get('location_id', '')
                organization = request.GET.get('organization_id', '')
                pid = request.GET.get('pid', '')
                f = Article.objects.articlesbypersonlocationorganization(person, location, organization, pid)
                response = HttpResponse(Json.dumps(convertListToMap(f), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

            elif 'person_id' in request.GET and 'location_id' in request.GET and 'pid' in request.GET:
                person = request.GET.get('person_id', '')
                location = request.GET.get('location_id', '')
                pid = request.GET.get('pid', '')
                PL = ArticlebyPerson.objects.articlesbypersonlocation(person, location, pid)
                response = HttpResponse(Json.dumps(convertListToMap(PL), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

            elif 'organization_id' in request.GET and 'location_id' in request.GET and 'pid' in request.GET:
                organization = request.GET.get('organization_id', '')
                location = request.GET.get('location_id', '')
                pid =  request.GET.get('pid', '')
                OL = ArticlebyLocation.objects.articlesbylocationorganization(location,organization,pid)
                response = HttpResponse(Json.dumps(convertListToMap(OL), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

            elif 'organization_id' in request.GET and 'person_id' in request.GET and 'pid' in request.GET:
                person = request.GET.get('person_id', '')
                organization = request.GET.get('organization_id', '')
                pid = request.GET.get('pid', '')
                OP = ArticlebyOrganization.objects.articlesbypersonorganization(person,organization,pid)
                response = HttpResponse(Json.dumps(convertListToMap(OP), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

            elif 'location_id' in request.GET and 'pid' in request.GET:
                location = request.GET.get('location_id', '')
                pid = request.GET.get('pid', '')
                L = ArticlebyLocation.object.articlesbylocation(location, pid)
		response = HttpResponse(Json.dumps(convertListToMap(L), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

            elif 'person_id' in request.GET and 'pid' in request.GET:
                person = request.GET.get('person_id', '')
                pid = request.GET.get('pid', '')
                P = ArticlebyPerson.object.articlesbyperson(person,pid)
                response = HttpResponse(Json.dumps(convertListToMap(P), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

            elif 'organization_id' in request.GET and 'pid' in request.GET:
                organization = request.GET.get('organization_id', '')
                pid = request.GET.get('pid', '')
                O = ArticlebyOrganization.object.articlebyorganization(organization, pid)
                response = HttpResponse(Json.dumps(convertListToMap(O), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)
            else:
                A = Article.objects.values('id', 'headline', 'clicks', 'file__published_date')
		#response = HttpResponse(A).content
                response = HttpResponse(Json.dumps(convertValuesToMap(A), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
                return HttpResponse(response)

    except:
        print "Error"

def click_article(request):
    if request.method == 'GET':
        articleid = request.GET['article_id']
        article = Article.objects.get(id = articleid)
        if article:
            article.clicks = article.clicks + 1
            article.save()
            response = HttpResponse(article.clicks).content
        return HttpResponse(response)

def article_content(request):
    if request.method == 'GET':
        articleid = request.GET['article_id']
        article = Article.objects.get(id = articleid)
        if article:
            response = HttpResponse(article.content).content
            return HttpResponse(response)

def count_by_location(request):
    if request.method == 'GET':
	A = ArticlebyLocation.objects.values('location', 'location__name').annotate(Count('article')).order_by()
	response = HttpResponse(Json.dumps(convertLocationListToMap(A), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)

def convertListToMap(lists):
    result = []
    for list in lists:
        result.append(convertEachListToMap(list))
    return result

def convertEachListToMap(list):
    result = {}
    result['id'] = list[0]
    result['headline'] = list[1]
    result['clicks'] = list[2]
    result['published_date'] = list[3]
    return result

def convertValuesToMap(lists):
    result = []
    for list in lists:
        result.append(convertEachValueToMap(list))
    return result

def convertEachValueToMap(list):
    result = {}
    result['id'] = list['id']
    result['headline'] = list['headline']
    result['clicks'] = list['clicks']
    result['published_date'] = list['file__published_date']
    return result

def convertLocationListToMap(lists):
    result = []
    for list in lists:
        result.append(convertEachLocationListToMap(list))
    return result

def convertEachLocationListToMap(list):
    result = {}
    result['location_id'] = list['location']
    result['location_name'] = list['location__name']
    result['article_count'] = list['article__count']
    return result

def convertSelectAttributesToMap(lists):
    result1 = []
    for list in lists:
        result1.append(convertToMap(list))
    return result1

def convertToMap(list):
    result1 = {}
    result1['id'] = list[0]
    result1['name'] = list[1]
    return result1
