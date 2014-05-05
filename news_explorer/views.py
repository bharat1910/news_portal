from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from datetime import date
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson as Json
from django.conf import settings
from django.utils.importlib import import_module
from django.db.models import Count
from news_explorer.models import File, Person, Organization, Location, Article, ArticlebyLocation, ArticlebyPerson \
    , ArticlebyOrganization, PersonManager,OrganizationManager,LocationManager

def index(request):
    context = {}
    getCountry("Delhi")
    return render(request, 'news_explorer/index.html', context)

def wordcloud(request):
    context = {}
    return render(request, 'news_explorer/wordcloud.html', context)

def news_articles_by_selection(request):
    context = {}
    return render(request, 'news_explorer/news_articles_by_selection.html', context)

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

def getCoordinates(location):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&sensor=true'
	r = requests.get(url, auth=('user', 'pass'))
	res = r.json()
	res = convert(res)
	lat = res['results'][0]['geometry']['location']['lat']
	lng = res['results'][0]['geometry']['location']['lng']
	return (lat,lng)

def getCountry(location):
    try:
        (lat,lng) = getCoordinates(location)
        url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lng)+'&sensor=false'
        r = requests.get(url, auth=('user', 'pass'))
        res = r.json()
        res = convert(res)
        rows = res['results'][0]['address_components']
        count = len(rows)
        country = location
        for x in range(0,count):
            type_of_attr = str(rows[x]['types'])
            if 'country' in type_of_attr:
                country = rows[x]['long_name']
        return country
    except:
        return location

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def filterByDate(option,day,month,year,jsonObj):
	dateA = date(year, month, day)
	if(option == "week"):
		dateB = dateA + datetime.timedelta(days=-7)
	elif(option == "year"):
		dateB = dateA + datetime.timedelta(days=-365)
	elif(option == "month"):
		dateB = dateA + datetime.timedelta(days=-30)
	jsonObj = jsonObj.filter(file__published_date__range=[dateB,dateA])
	jsonObj = Json.dumps(convertValuesToMap(jsonObj), default=jdefault, indent=4)	
	return jsonObj

def initiate_chosen(request, reqtype):
    if request.method == 'GET':
        if reqtype == "location":
            L = Location.objects.uniqueLocation()
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
            a = [];

            if 'content' in request.GET:
                a = Article.objects.values('id', 'headline', 'content', 'clicks', 'file__published_date')
            else:
                a = Article.objects.values('id', 'headline', 'clicks', 'file__published_date')

            if 'location_id' in request.GET:
                a = a.filter(articlebylocation__location_id = request.GET.get('location_id', ''))
            if 'person_id' in request.GET:
                a = a.filter(articlebyperson__person_id = request.GET.get('person_id', ''))
            if 'organization_id' in request.GET:
                a = a.filter(articlebyorganization__organization_id = request.GET.get('organization_id', ''))

            if 'fdate' in request.GET:
                print(2)
                toDate = datetime(2005, 05, 24)
                fdate = request.GET.get('fdate', '')
                if fdate == "week":
                    fromDate = toDate + timedelta(days=-7)
                elif fdate == "month":
                    fromDate = toDate + timedelta(days=-31)
                else:
                    fromDate = toDate + timedelta(days=-366)

                a = a.filter(file__published_date__gte = fromDate)\
                     .filter(file__published_date__lte = toDate)

            if 'pid' in request.GET:
                pid = int(request.GET.get('pid', ''))
                if pid == 1:
                    a = a.order_by('clicks')
                elif pid == 2:
                    a = a.order_by('-clicks')
                else:
                    a = a.order_by('-file__published_date')

            if 'content' in request.GET:
                response = HttpResponse(Json.dumps(convertToList(a,"true"), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
            else:
                response = HttpResponse(Json.dumps(convertToList(a,"false"), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content

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
	parentlocationid = request.GET['parentlocation_id']
	A = ArticlebyLocation.objects.filter(location__parentlocation_id=parentlocationid).values('location', 'location__name').annotate(Count('article')).order_by()
	response = HttpResponse(Json.dumps(convertLocationListToMap(A), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
        return HttpResponse(response)

def count_by_parentlocation(request):
    if request.method == 'GET':
       A = ArticlebyLocation.obj.countbyparentlocation()
       response = HttpResponse(Json.dumps(convertParentLocationListToMap(A), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
       return HttpResponse(response)

def search_results(request):
    url = 'http://localhost:8983/solr/cs410/clustering?&q=' + request.GET['q'] + '&wt=json'
    r = requests.get(url, auth=('user', 'pass'))
    response = HttpResponse(Json.dumps(convertSearchListToMap(r), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
    return HttpResponse(response)

def convertToList(lists,content):
    result = []
    for list in lists:
        result.append(convertEachEntityToMap(list,content))
    return result

def convertSearchListToMap(r):
    lists = convert(r.json())['response']['docs']
    result = []
    for list in lists:
        result.append(convertEachSearchResultToMap(list))
    return result

def convertEachSearchResultToMap(sr):
    result = {}
    result['id'] = sr['id']
    result['headline'] = sr['title'][0]
    result['content'] = sr['content'][0]
    result['clicks'] = Article.objects.get(id = sr['id']).clicks
    return result

def convertEachEntityToMap(list,content):
    result = {}
    result['id'] = list['id']
    result['headline'] = list['headline']
    result['clicks'] = list['clicks']
    if content == "true":
    	result['content'] = list['content']
    result['published_date'] = list['file__published_date'].strftime("%Y-%m-%d")
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

def convertParentLocationListToMap(lists):
    result = []
    for list in lists:
        result.append(convertEachParentLocationListToMap(list))
    return result

def convertEachParentLocationListToMap(list):
    result = {}
    result['parentlocation_id'] = list[0]
    result['parentlocation_name'] = list[1]
    result['article_count'] = list[2]
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
