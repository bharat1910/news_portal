from django.shortcuts import render
import requests
import datetime
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

def getJson_new(request):
	try:
		if request.method == 'GET':
			if 'location_id' in request.GET and 'person_id' in request.GET and 'organization_id'in request.GET and 'pid' in request.GET:
				person = request.GET.get('person_id', '')
				location = request.GET.get('location_id', '')
				organization = request.GET.get('organization_id', '')
				pid = request.GET.get('pid', '')
				f = Article.objects.articlesbypersonlocationorganization(person, location, organization, pid)
			elif 'person_id' in request.GET and 'location_id' in request.GET and 'pid' in request.GET:
				person = request.GET.get('person_id', '')
				location = request.GET.get('location_id', '')
				pid = request.GET.get('pid', '')
				f = ArticlebyPerson.objects.articlesbypersonlocation(person, location, pid)
			elif 'organization_id' in request.GET and 'location_id' in request.GET and 'pid' in request.GET:
				organization = request.GET.get('organization_id', '')
				location = request.GET.get('location_id', '')
				pid =  request.GET.get('pid', '')
				f = ArticlebyLocation.objects.articlesbylocationorganization(location,organization,pid)
			elif 'organization_id' in request.GET and 'person_id' in request.GET and 'pid' in request.GET:
				person = request.GET.get('person_id', '')
				organization = request.GET.get('organization_id', '')
				pid = request.GET.get('pid', '')
				f = ArticlebyOrganization.objects.articlesbypersonorganization(person,organization,pid)
			elif 'location_id' in request.GET and 'pid' in request.GET:
				location = request.GET.get('location_id', '')
				pid = request.GET.get('pid', '')
				f = ArticlebyLocation.object.articlesbylocation(location, pid)
			elif 'person_id' in request.GET and 'pid' in request.GET:
				person = request.GET.get('person_id', '')
				pid = request.GET.get('pid', '')
				f = ArticlebyPerson.object.articlesbyperson(person,pid)
			elif 'organization_id' in request.GET and 'pid' in request.GET:
				organization = request.GET.get('organization_id', '')
				pid = request.GET.get('pid', '')
				f = ArticlebyOrganization.object.articlebyorganization(organization, pid)
			else:
				if 'pid' in request.GET:
  					pid = request.GET.get('pid', '')
 					if pid == '1':
						f = Article.objects.values('id', 'headline', 'clicks', 'file__published_date').order_by('clicks')
					elif pid == '2':
						f = Article.objects.values('id', 'headline', 'clicks', 'file__published_date').order_by('-clicks')
			if 'fdate' in request.GET:
				fdate = request.GET.get('fdate', '')
				x = filterByDate(fdate,23,04,2005,f)
				response = HttpResponse(x, content_type="application/json", mimetype="application/json").content
 				return HttpResponse(response)
			else:
				response = HttpResponse(Json.dumps(convertValuesToMap(f), default=jdefault, indent=4), content_type="application/json", mimetype="application/json").content
				return HttpResponse(response)
	except:
		print "Error"

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
                if 'pid' in request.GET:
                    pid = request.GET.get('pid', '')
                    if pid == '1':
			A = Article.objects.values('id', 'headline', 'clicks', 'file__published_date').order_by('clicks')
			x = filterByDate("month",23,04,2005,A)
			response = HttpResponse(x, content_type="application/json", mimetype="application/json").content
                	return HttpResponse(response)
                    elif pid == '2':
                        A = Article.objects.values('id', 'headline', 'clicks', 'file__published_date').order_by('-clicks')
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

def convertListToMap(lists):
    result = []
    for list in lists:
        result.append(convertEachListToMap(list))
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
